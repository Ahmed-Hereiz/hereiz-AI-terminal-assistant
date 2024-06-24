from typing import Any
from agent_runtime import BaseRuntime


class ReActRuntime(BaseRuntime):
    def __init__(self, llm: Any, prompt: Any, tools: Any):
        super().__init__(llm, prompt, tools)


        