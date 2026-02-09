"""FastMCP server using the `@mcp.tool` decorator to register tools.

This demonstrates the preferred decorator pattern supported by FastMCP:

- @mcp.tool  # register a tool using the function name
- @mcp.tool("custom_name")  # register tool with explicit name
- @mcp.tool(name="custom_name")  # keyword form

The ASGI app is exposed as `app` and uses a streamable HTTP path at `/stream`.
"""
from typing import Annotated
from pydantic import Field
from fastmcp import FastMCP
from fastmcp.server.http import create_streamable_http_app

# Create FastMCP instance first
mcp = FastMCP(
    name="mcp-echo-decorator",
    instructions="A minimal FastMCP server exposing an echo tool via decorator",
)

# Use the server decorator to register the tool
@mcp.tool
def echo(message: Annotated[str, Field(description="The specific text message you want to echo back to the user.")]) -> dict:
    """Echo the user's message back unchanged."""
    return {"message": message}

# Create an ASGI app to serve the MCP server (streamable / SSE-ready)
app = create_streamable_http_app(mcp, "/stream")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)
