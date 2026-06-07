"""JSON-RPC/MCP exceptions."""

from __future__ import annotations


class MCPError(Exception):
    """Base JSON-RPC error with a standard code and message."""

    code = -32000
    message = "Server error"

    def __init__(self, message: str | None = None, code: int | None = None) -> None:
        self.message = message or self.message
        self.code = code if code is not None else self.code
        super().__init__(self.message)


class ParseError(MCPError):
    """Invalid JSON was received by the server."""

    code = -32700
    message = "Parse error"


class InvalidRequestError(MCPError):
    """The JSON sent is not a valid request object."""

    code = -32600
    message = "Invalid Request"


class MethodNotFoundError(MCPError):
    """The requested method is not registered."""

    code = -32601
    message = "Method not found"


class InvalidParamsError(MCPError):
    """The request parameters are invalid for the method."""

    code = -32602
    message = "Invalid params"


class ResourceNotFoundError(MCPError):
    """The requested filesystem resource does not exist."""

    code = -32004
    message = "Resource not found"

