"""Quick test for decorator-based server: directly calls the registered tool object."""
from mcp_server_decorator import echo

# echo is a FunctionTool instance; the underlying callable is on `fn`
result = echo.fn("Hello from decorator test!")
print("Echo returned:", result)
