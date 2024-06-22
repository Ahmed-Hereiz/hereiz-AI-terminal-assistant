from typing import Any, Dict, Callable
from agent_tools import BaseTool


class ScapeLinkTool(BaseTool):
    def __init__(self, tools: Dict[str, Callable] = {}):
        super().__init__(tools)