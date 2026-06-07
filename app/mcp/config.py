"""MCP filesystem server configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from app.utils import config as app_config


@dataclass(frozen=True)
class MCPServerConfig:
    """Filesystem MCP server settings."""

    resume_dir: Path = app_config.RESUME_DIR
    jd_dir: Path = app_config.JD_DIR
    polling_interval_seconds: float = float(os.getenv("MCP_POLL_INTERVAL_SECONDS", "1.0"))
    host: str = os.getenv("MCP_SERVER_HOST", "127.0.0.1")
    port: int = int(os.getenv("MCP_SERVER_PORT", "8765"))
    server_name: str = os.getenv("MCP_SERVER_NAME", "talentrankai-filesystem")
    supported_extensions: tuple[str, ...] = (".pdf", ".txt", ".md")


DEFAULT_CONFIG = MCPServerConfig()

