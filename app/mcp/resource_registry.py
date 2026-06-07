"""Resource and tool registry for the filesystem MCP server."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from app.mcp.exceptions import MethodNotFoundError


Handler = Callable[..., Any]


class ResourceRegistry:
    """Register and resolve MCP resources/tools by method name."""

    def __init__(self) -> None:
        self._handlers: dict[str, Handler] = {}

    def register(self, name: str, handler: Handler) -> None:
        """Register a callable under a JSON-RPC method name."""
        self._handlers[name] = handler

    def get(self, name: str) -> Handler:
        """Return a handler or raise a JSON-RPC method error."""
        try:
            return self._handlers[name]
        except KeyError as exc:
            raise MethodNotFoundError() from exc

    def discover(self) -> list[str]:
        """Return registered resource/tool names in registration order."""
        return list(self._handlers)

