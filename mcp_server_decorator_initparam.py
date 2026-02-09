"""FastMCP server with initialization parameter support for PREFIX.

Supports reading PREFIX from (priority order):
1. HTTP Header `PREFIX` (per-request)
2. Server startup parameter passed to `build_app(prefix=...)`
3. Environment variable `PREFIX`

The PREFIX value (if present) is prepended to the echoed message in the `echo` tool.

The module exposes:
- build_app(prefix: str | None = None) -> tuple[FastMCP, ASGI app]
- mcp, app: default instances using environment variable at import time

Run as a script to start a dev server that accepts --prefix.
"""
from __future__ import annotations

import os
from typing import Tuple
from pydantic import Field
from fastmcp import FastMCP
from fastmcp.server.http import create_streamable_http_app
from fastmcp.server.dependencies import get_http_request, get_context
from fastmcp.server import Context


def _compute_prefix_from_request() -> str | None:
    """Try to read PREFIX from an active HTTP request (if any).

    Uses FastMCP's request helper which checks both the MCP request
    context and a fallback HTTP context var used by middleware.
    """
    try:
        request = get_http_request()
        # Headers are case-insensitive mapping — try direct lookup then lowercase
        return request.headers.get("PREFIX") or request.headers.get("prefix")
    except RuntimeError:
        return None


def _compute_prefix_from_server() -> str | None:
    """Get server startup prefix from the active FastMCP instance if available."""
    try:
        ctx = get_context()
        fastmcp = ctx.fastmcp
        return getattr(fastmcp, "startup_prefix", None)
    except RuntimeError:
        return None


def build_app(prefix: str | None = None) -> Tuple[FastMCP, object]:
    """Build and return a (FastMCP, ASGI app) tuple.

    If `prefix` is provided it is used as the server startup prefix. Otherwise
    the environment variable `PREFIX` is used as a fallback.
    """
    startup_prefix = prefix if prefix is not None else os.getenv("PREFIX")

    mcp = FastMCP(
        name="mcp-echo-initparam",
        instructions="Echo tool demonstrating PREFIX from header/env/startup param",
    )

    # Keep the startup prefix on the server instance for access from tools
    mcp.startup_prefix = startup_prefix

    # Register the echo tool via decorator on this server instance.
    @mcp.tool
    def echo(message: str, ctx: Context | None = None) -> dict:
        """Echo the user's message, prefixed if PREFIX is found."""
        # Priority: HTTP header > server startup param > env var
        header_prefix = _compute_prefix_from_request()
        if header_prefix:
            prefix_val = header_prefix
        else:
            server_prefix = getattr(mcp, "startup_prefix", None) or _compute_prefix_from_server()
            prefix_val = server_prefix or os.getenv("PREFIX")

        if prefix_val:
            return {"message": f"{prefix_val}{message}"}
        return {"message": message}

    # Expose app with streamable HTTP path
    app = create_streamable_http_app(mcp, "/stream")

    return mcp, app


# Module-level default using environment variable at import time
mcp, app = build_app()


def main() -> None:
    import argparse
    import uvicorn

    parser = argparse.ArgumentParser(description="Run mcp_server_decorator_initparam")
    parser.add_argument("--prefix", help="Startup PREFIX to prepend (overrides env)", default=None)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    server_mcp, server_app = build_app(prefix=args.prefix)

    uvicorn.run(server_app, host=args.host, port=args.port, reload=True)


if __name__ == "__main__":
    main()
