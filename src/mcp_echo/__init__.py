from . import mcp_server_decorator_initparam as _core

__all__ = ["build_app", "mcp", "app", "main"]

build_app = _core.build_app
mcp = _core.mcp
app = _core.app

def main() -> None:
    """Run the packaged module's main entrypoint."""
    _core.main()
