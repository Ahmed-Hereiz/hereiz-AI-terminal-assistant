from agent_prompt import BasePrompt


class SimplePrompt(BasePrompt):
    def __init__(self, prompt_string: str = "", user_input: str= "", memory_string: str = None):
        super().__init__(prompt_string, placeholders={})

        self.user_input = user_input
        self.memory_string = memory_string
        self.prompt = self._generate_prompt()
