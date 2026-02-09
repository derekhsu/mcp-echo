# mcp-echo ✅

A minimal FastMCP server that exposes an `echo` tool which returns the user's message verbatim.

## Quick start 🔧

1. Activate your virtualenv:

   ```bash
   source .venv/bin/activate
   ```

2. Run the server:

   ```bash
   python mcp_server.py
   # or with reload (if you have uvicorn installed):
   # uvicorn mcp_server:app --host 127.0.0.1 --port 8080 --reload
   ```

   The server runs an ASGI app and provides streamable endpoints under `/stream`.

3. Quick local test (no HTTP required):

   ```bash
   python scripts/test_echo.py
   ```

   Output example:

   ```
   Echo function returned: {'message': 'Hello, MCP echo test!'}
   ```


## Notes 💡

- The `echo` tool is implemented as a `FunctionTool` and returns structured JSON content: `{"message": "..."}`.
- To exercise the tool via a full MCP client, use an MCP-capable client and call the registered tool named `echo`.
