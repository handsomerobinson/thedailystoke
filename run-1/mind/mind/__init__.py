"""mind — the mind around the brain: a personal agent that rents its intelligence from an LLM API
and adds reflection, tools, memory, proactivity, permissions and cost control around it."""
from .config import Config, SandboxPolicy
from .evaluator import Contains, ExactMatch, LLMJudge, PythonTests, TaskSpec
from .permissions import ConsoleApprover, DenyAll, ScriptedApprover, Tier
from .runtime import Mind, Session

__version__ = "0.1.0"
__all__ = ["Mind", "Session", "Config", "SandboxPolicy", "TaskSpec", "PythonTests", "ExactMatch", "Contains",
           "LLMJudge", "ConsoleApprover", "ScriptedApprover", "DenyAll", "Tier"]
