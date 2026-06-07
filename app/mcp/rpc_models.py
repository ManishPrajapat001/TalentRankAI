"""Lightweight JSON-RPC 2.0 request and response models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.mcp.exceptions import InvalidRequestError, MCPError


JSONRPC_VERSION = "2.0"


@dataclass(frozen=True)
class JSONRPCRequest:
    """A validated JSON-RPC 2.0 request."""

    id: str | int | None
    method: str
    params: dict[str, Any] | list[Any] | None
    jsonrpc: str = JSONRPC_VERSION

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "JSONRPCRequest":
        """Build a request from a raw dictionary."""
        if not isinstance(payload, dict):
            raise InvalidRequestError()
        if payload.get("jsonrpc") != JSONRPC_VERSION:
            raise InvalidRequestError("jsonrpc must be '2.0'")
        method = payload.get("method")
        if not isinstance(method, str) or not method:
            raise InvalidRequestError("method must be a non-empty string")
        params = payload.get("params", {})
        if params is not None and not isinstance(params, (dict, list)):
            raise InvalidRequestError("params must be an object, array, or null")
        return cls(id=payload.get("id"), method=method, params=params)


def success_response(request_id: str | int | None, result: Any) -> dict[str, Any]:
    """Return a JSON-RPC success response."""
    return {"jsonrpc": JSONRPC_VERSION, "id": request_id, "result": result}


def error_response(request_id: str | int | None, error: MCPError) -> dict[str, Any]:
    """Return a JSON-RPC error response."""
    return {
        "jsonrpc": JSONRPC_VERSION,
        "id": request_id,
        "error": {"code": error.code, "message": error.message},
    }

