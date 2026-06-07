"""Manual validation script for the filesystem MCP client abstraction.

Run:
    python tests/test_mcp_client.py
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.mcp.filesystem_mcp_client import FilesystemMCPClient  # noqa: E402


EXPECTED_RESOURCES = {
    "list_resumes",
    "load_resume",
    "load_all_resumes",
    "list_jds",
    "load_jd",
    "load_all_jds",
    "watch_directory",
    "batch_process",
}


def print_separator(title: str) -> None:
    """Print a readable console section separator."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_pass(message: str) -> None:
    """Print a PASS line."""
    print(f"PASS: {message}")


def print_fail(message: str) -> None:
    """Print a FAIL line."""
    print(f"FAIL: {message}")


def main() -> int:
    """Validate FilesystemMCPClient methods without exposing JSON-RPC to callers."""
    print_separator("Filesystem MCP Client Validation")

    try:
        client = FilesystemMCPClient()
    except Exception as exc:
        print_fail(f"Client startup failed: {exc}")
        return 0

    print_pass("Client started successfully.")

    print_separator("Resource Discovery")
    try:
        discovery = client.discover_resources()
        resources = set(discovery.get("resources", []))
        print(f"Resources: {discovery.get('resources', [])}")
        missing = EXPECTED_RESOURCES - resources
        extra = resources - EXPECTED_RESOURCES
        if missing:
            print_fail(f"Missing resources: {sorted(missing)}")
        elif extra:
            print_fail(f"Unexpected resources: {sorted(extra)}")
        else:
            print_pass("Client discovered the expected MCP resources.")
    except Exception as exc:
        print_fail(f"Client resource discovery failed: {exc}")

    print_separator("List Resumes")
    resumes: list[str] = []
    try:
        resumes = client.list_resumes()
        if isinstance(resumes, list):
            print_pass("client.list_resumes returned a list.")
        else:
            print_fail(f"client.list_resumes returned {type(resumes).__name__}, expected list.")
            resumes = []
        print(f"Resume count: {len(resumes)}")
        print(f"First few resumes: {resumes[:5]}")
    except Exception as exc:
        print_fail(f"Client resume listing failed: {exc}")

    print_separator("Load Resume")
    if not resumes:
        print("No resumes available. Skipping client.load_resume validation gracefully.")
    else:
        try:
            resume = client.load_resume(resumes[0])
            required_keys = {"id", "filename", "source", "type", "text"}
            missing_keys = required_keys - set(resume)
            if missing_keys:
                print_fail(f"Loaded resume missing keys: {sorted(missing_keys)}")
            else:
                print_pass("client.load_resume returned required fields.")
            print(f"ID: {resume.get('id')}")
            print(f"Filename: {resume.get('filename')}")
            print(f"Type: {resume.get('type')}")
            print(f"Text length: {len(resume.get('text', ''))}")
        except Exception as exc:
            print_fail(f"Client resume loading failed: {exc}")

    print_separator("Batch Process")
    if not resumes:
        print("No resumes available. Skipping client.batch_process validation gracefully.")
    else:
        try:
            result = client.batch_process(resumes[:2])
            required_keys = {"processed", "successful", "failed"}
            missing_keys = required_keys - set(result)
            if missing_keys:
                print_fail(f"Batch result missing keys: {sorted(missing_keys)}")
            else:
                print_pass("client.batch_process returned required summary fields.")
            print(f"Batch result: {result}")
        except Exception as exc:
            print_fail(f"Client batch processing failed: {exc}")

    print_separator("Watch Directory")
    try:
        result = client.watch_directory()
        if isinstance(result, dict):
            print_pass("client.watch_directory executed successfully.")
        else:
            print_fail(f"client.watch_directory returned {type(result).__name__}, expected dict.")
        print(f"Watch result: {result}")
    except Exception as exc:
        print_fail(f"Client watch_directory failed: {exc}")

    print_separator("MCP Client Validation Complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

