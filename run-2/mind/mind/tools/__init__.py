from .base import Tool, ToolResult
from .code_exec import CodeExecTool
from .notes import NotesTool
from .web_search import WebSearchTool

__all__ = ["Tool", "ToolResult", "CodeExecTool", "NotesTool", "WebSearchTool"]


def default_toolset() -> dict:
    tools = [CodeExecTool(), NotesTool(), WebSearchTool()]
    return {t.name: t for t in tools}
