"""Simple local test to call the echo tool function directly."""
from mcp_server import echo

# The decorator returns a FunctionTool object; the underlying callable is available
# on the `fn` attribute. Call it directly for a quick local test.
result = echo.fn("Hello, MCP echo test!")
print("Echo function returned:", result)
