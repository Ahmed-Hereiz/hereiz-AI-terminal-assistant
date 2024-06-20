from agent_prompt import BasePrompt


class ChatPrompt(BasePrompt):
    def __init__(self, prompt_string: str = "", user_input: str= "", memory_string: str = None):
        super().__init__(prompt_string)

        self.user_input = user_input
        self.memory_string = memory_string
        self.prompt = self._generate_prompt()


    def _generate_prompt(self):
        
        prompt = self.prompt_string.replace("{input}",self.user_input)

        if self.memory_string is None:
            return prompt.replace("{history}","")
        else:
            return prompt.replace("{history}",self.memory_string)
