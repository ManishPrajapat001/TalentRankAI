"""Filesystem MCP server exposed through JSON-RPC 2.0."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.mcp.config import DEFAULT_CONFIG, MCPServerConfig
from app.mcp.exceptions import (
    InvalidParamsError,
    InvalidRequestError,
    MCPError,
    ParseError,
    ResourceNotFoundError,
)
from app.mcp.resource_registry import ResourceRegistry
from app.mcp.rpc_models import JSONRPCRequest, error_response, success_response
from app.utils.config import ensure_data_dirs


class FilesystemMCPServer:
    """JSON-RPC server for resume and job-description filesystem resources."""

    def __init__(self, config: MCPServerConfig | None = None) -> None:
        ensure_data_dirs()
        self.config = config or DEFAULT_CONFIG
        self.registry = ResourceRegistry()
        self._watch_snapshots: dict[Path, set[str]] = {}
        self._register_resources()

    def _register_resources(self) -> None:
        self.registry.register("list_resumes", self.list_resumes)
        self.registry.register("load_resume", self.load_resume)
        self.registry.register("load_all_resumes", self.load_all_resumes)
        self.registry.register("list_jds", self.list_jds)
        self.registry.register("load_jd", self.load_jd)
        self.registry.register("load_all_jds", self.load_all_jds)
        self.registry.register("watch_directory", self.watch_directory)
        self.registry.register("batch_process", self.batch_process)
        self.registry.register("discover_resources", self.discover_resources)

    def handle_json(self, raw_payload: str) -> dict[str, Any]:
        """Handle one JSON-RPC request encoded as a JSON string."""
        request_id: str | int | None = None
        try:
            payload = json.loads(raw_payload)
            if not isinstance(payload, dict):
                raise InvalidRequestError()
            request_id = payload.get("id")
            return self.handle_request(payload)
        except json.JSONDecodeError as exc:
            return error_response(request_id, ParseError(str(exc)))
        except MCPError as exc:
            return error_response(request_id, exc)
        except Exception as exc:
            return error_response(request_id, MCPError(str(exc)))

    def handle_request(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Handle one JSON-RPC request dictionary."""
        request = JSONRPCRequest.from_dict(payload)
        handler = self.registry.get(request.method)
        params = request.params or {}

        try:
            if isinstance(params, list):
                result = handler(*params)
            elif isinstance(params, dict):
                result = handler(**params)
            else:
                raise InvalidParamsError()
        except TypeError as exc:
            raise InvalidParamsError(str(exc)) from exc

        return success_response(request.id, result)

    def discover_resources(self) -> dict[str, list[str]]:
        """Return available filesystem resources and tools."""
        return {
            "resources": [
                resource
                for resource in self.registry.discover()
                if resource != "discover_resources"
            ]
        }

    def list_resumes(self) -> list[str]:
        """List available resume resource names."""
        return self._list_files(self.config.resume_dir)

    def load_resume(self, path: str) -> dict[str, str]:
        """Load a single resume by filename or safe path."""
        return self._load_document(path, self.config.resume_dir, "resume")

    def load_all_resumes(self) -> list[dict[str, str]]:
        """Load every readable resume."""
        return [self.load_resume(path) for path in self.list_resumes()]

    def list_jds(self) -> list[str]:
        """List available job description resource names."""
        return self._list_files(self.config.jd_dir)

    def load_jd(self, path: str) -> dict[str, str]:
        """Load a single job description by filename or safe path."""
        return self._load_document(path, self.config.jd_dir, "jd")

    def load_all_jds(self) -> list[dict[str, str]]:
        """Load every readable job description."""
        return [self.load_jd(path) for path in self.list_jds()]

    def watch_directory(self, path: str | None = None) -> dict[str, Any]:
        """Poll a directory and return files that appeared since the last poll."""
        directory = self._resolve_directory(path, default=self.config.resume_dir)
        current = set(self._list_files(directory))
        previous = self._watch_snapshots.get(directory)
        self._watch_snapshots[directory] = current
        discovered = [] if previous is None else sorted(current - previous)
        if self.config.polling_interval_seconds > 0:
            time.sleep(min(self.config.polling_interval_seconds, 1.0))
        return {"path": str(directory), "new_files": discovered, "count": len(discovered)}

    def batch_process(self, paths: list[str]) -> dict[str, Any]:
        """Load many filesystem resources and return processing summary."""
        if not isinstance(paths, list):
            raise InvalidParamsError("paths must be a list")

        successful = 0
        failures: list[dict[str, str]] = []
        for path in paths:
            try:
                document = self._load_document(str(path), self.config.resume_dir, "resume")
                if document.get("text"):
                    successful += 1
                else:
                    failures.append({"path": str(path), "error": "No readable text found"})
            except MCPError as exc:
                failures.append({"path": str(path), "error": exc.message})

        processed = len(paths)
        return {
            "processed": processed,
            "successful": successful,
            "failed": processed - successful,
            "failures": failures,
        }

    def _list_files(self, directory: Path) -> list[str]:
        if not directory.exists():
            return []
        return sorted(
            path.name
            for path in directory.iterdir()
            if path.is_file() and path.suffix.lower() in self.config.supported_extensions
        )

    def _load_document(self, path: str, base_dir: Path, kind: str) -> dict[str, str]:
        resolved = self._resolve_file(path, base_dir)
        if resolved.suffix.lower() == ".pdf":
            text = self._load_pdf(resolved)
        else:
            text = resolved.read_text(encoding="utf-8", errors="ignore").strip()
        return {
            "id": resolved.stem,
            "filename": resolved.name,
            "source": str(resolved),
            "type": kind,
            "text": text,
        }

    def _resolve_directory(self, path: str | None, default: Path) -> Path:
        if not path:
            return default.resolve()
        candidate = Path(path)
        if not candidate.is_absolute():
            repo_relative = Path.cwd() / candidate
            candidate = repo_relative if repo_relative.exists() else default / candidate
        resolved = candidate.resolve()
        if not resolved.exists() or not resolved.is_dir():
            raise ResourceNotFoundError(f"Directory not found: {path}")
        return resolved

    def _resolve_file(self, path: str, base_dir: Path) -> Path:
        if not path:
            raise InvalidParamsError("path is required")
        candidate = Path(path)
        if not candidate.is_absolute():
            repo_relative = Path.cwd() / candidate
            candidate = repo_relative if repo_relative.exists() else base_dir / candidate
        resolved = candidate.resolve()
        base = base_dir.resolve()
        if base not in (resolved, *resolved.parents):
            raise InvalidParamsError("path must stay within configured resource directory")
        if not resolved.exists() or not resolved.is_file():
            raise ResourceNotFoundError(f"File not found: {path}")
        if resolved.suffix.lower() not in self.config.supported_extensions:
            raise InvalidParamsError(f"Unsupported file extension: {resolved.suffix}")
        return resolved

    @staticmethod
    def _load_pdf(path: Path) -> str:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages).strip()


def serve_stdio() -> None:
    """Run a simple JSON-lines JSON-RPC server over stdin/stdout."""
    server = FilesystemMCPServer()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        print(json.dumps(server.handle_json(line)), flush=True)


if __name__ == "__main__":
    serve_stdio()
