# state.py
from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    user_id: int
    current_agent: str
    memory: dict
