from typing import Any
from agent_prompt import BasePrompt


class SimplePrompt(BasePrompt):
    def __init__(self, prompt_string: str = "", user_input: str = ""):
        super().__init__(prompt_string)

        self.user_input = user_input
        self.prompt = self._generate_prompt()
    
    def _generate_prompt(self):
        
        return self.prompt_string.replace("{input}",self.user_input)
        