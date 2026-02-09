from typing import Annotated
from pydantic import Field
from fastmcp import FastMCP
from fastmcp.tools import FunctionTool
from fastmcp.server.http import create_streamable_http_app

def echo_fn(message: Annotated[str, 
    Field(
        description="The specific text message you want to echo back to the user.")]
    ) -> dict:
    """Echo the user's message."""
    # Return structured content so the MCP client receives it verbatim
    return {"message": message}

# Wrap the function as a FastMCP FunctionTool
echo = FunctionTool.from_function(
    echo_fn, name="echo", title="Echo Tool", description="Echoes back the provided message unchanged."
)

# Create FastMCP app with the echo tool
mcp = FastMCP(
    name="mcp-echo",
    instructions="A minimal FastMCP server exposing an echo tool",
    tools=[echo],
)

# Create an ASGI app to serve the MCP server (streamable / SSE-ready)
# `streamable_http_path` is the base path for streamable HTTP endpoints (SSE, etc.)
app = create_streamable_http_app(mcp, "/stream")

if __name__ == "__main__":
    import uvicorn

    # Run the ASGI app for local testing (http://127.0.0.1:8080)
    uvicorn.run(app, host="127.0.0.1", port=8080)
