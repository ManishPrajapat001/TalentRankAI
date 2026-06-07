"""Client facade for the filesystem MCP server."""

from __future__ import annotations

import json
from typing import Any

from app.mcp.exceptions import MCPError
from app.mcp.filesystem_mcp_server import FilesystemMCPServer


class FilesystemMCPClient:
    """Hide JSON-RPC details behind clean filesystem resource methods."""

    def __init__(self, server: FilesystemMCPServer | None = None) -> None:
        self.server = server or FilesystemMCPServer()
        self._next_id = 1

    def discover_resources(self) -> dict[str, list[str]]:
        return self._call("discover_resources")

    def list_resumes(self) -> list[str]:
        return self._call("list_resumes")

    def load_resume(self, path: str) -> dict[str, str]:
        return self._call("load_resume", {"path": path})

    def load_all_resumes(self) -> list[dict[str, str]]:
        return self._call("load_all_resumes")

    def list_jds(self) -> list[str]:
        return self._call("list_jds")

    def load_jd(self, path: str) -> dict[str, str]:
        return self._call("load_jd", {"path": path})

    def load_all_jds(self) -> list[dict[str, str]]:
        return self._call("load_all_jds")

    def watch_directory(self, path: str | None = None) -> dict[str, Any]:
        params = {"path": path} if path is not None else {}
        return self._call("watch_directory", params)

    def batch_process(self, paths: list[str]) -> dict[str, Any]:
        return self._call("batch_process", {"paths": paths})

    def _call(self, method: str, params: dict[str, Any] | None = None) -> Any:
        request_id = self._next_id
        self._next_id += 1
        payload = {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params or {}}
        response = self.server.handle_json(json.dumps(payload))
        if "error" in response:
            error = response["error"]
            raise MCPError(error.get("message", "MCP request failed"), error.get("code", -32000))
        return response.get("result")
