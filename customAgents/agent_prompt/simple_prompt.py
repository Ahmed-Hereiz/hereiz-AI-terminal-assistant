from customAgents.agent_prompt import BasePrompt


class SimplePrompt(BasePrompt):
    def __init__(self, prompt_string: str = ""):

        super().__init__(prompt_string)

        