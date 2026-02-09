"""Tests for PREFIX initialization sources.

This script demonstrates three cases:
1. Environment variable (PREFIX)
2. Server startup parameter (--prefix / build_app(prefix=...))
3. HTTP header (per-request) via setting the internal context var

These are simple demonstrations and not full unit tests.
"""
import os
from types import SimpleNamespace
import fastmcp.server.dependencies as dep

from mcp_server_decorator_initparam import build_app


def test_env_prefix():
    os.environ["PREFIX"] = "ENV:"
    mcp, app = build_app()
    import asyncio
    echo_tool = asyncio.run(mcp.get_tool("echo"))
    print("env ->", echo_tool.fn("hello"))
    del os.environ["PREFIX"]


def test_startup_prefix():
    mcp, app = build_app(prefix="BOOT:")
    import asyncio
    echo_tool = asyncio.run(mcp.get_tool("echo"))
    print("startup ->", echo_tool.fn("world"))


def test_header_prefix():
    mcp, app = build_app()
    import asyncio
    echo_tool = asyncio.run(mcp.get_tool("echo"))

    # Create a fake request with headers and set it on the internal ContextVar
    req = SimpleNamespace(headers={"PREFIX": "HDR:"})
    token = dep._current_http_request.set(req)
    try:
        print("header ->", echo_tool.fn("from header"))
    finally:
        dep._current_http_request.reset(token)


if __name__ == "__main__":
    test_env_prefix()
    test_startup_prefix()
    test_header_prefix()
