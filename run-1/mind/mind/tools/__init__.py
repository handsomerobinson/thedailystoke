from .base import Tool, ToolContext, ToolRegistry, ToolResult, validate_args
from .builtin import (Calculator, DeleteNote, ListNotes, ReadNote, Recall, RememberFact, RunPython, ScheduleTask,
                      SendMessage, WriteNote, safe_eval)
from .web import HttpFetch, WebSearch


def default_tools() -> list[Tool]:
    return [Calculator(), RememberFact(), Recall(), WriteNote(), ReadNote(), ListNotes(), DeleteNote(),
            RunPython(), SendMessage(), ScheduleTask(), WebSearch(), HttpFetch()]


__all__ = ["Tool", "ToolContext", "ToolRegistry", "ToolResult", "validate_args", "default_tools", "safe_eval",
           "Calculator", "RememberFact", "Recall", "WriteNote", "ReadNote", "ListNotes", "DeleteNote", "RunPython",
           "SendMessage", "ScheduleTask", "WebSearch", "HttpFetch"]
