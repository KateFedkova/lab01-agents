from dataclasses import dataclass, field
from typing import Any
 
 
@dataclass
class AgentState:
    """A snapshot of the agent's execution state at the current step."""
 
    goal: str
    observations: list[str] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)
    step: int = 0
    llm_calls: int = 0
    finished: bool = False
    final_answer: str | None = None
    stop_reason: str | None = None
