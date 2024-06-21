from agent_prompt import BasePrompt


class PlaceHoldersPrompt(BasePrompt):
    def __init__(self, placeholders: dict = {}, prompt_string: str = ""):

        self.placeholders = placeholders

        super().__init__(prompt_string=prompt_string)

        self.prompt = self._generate_prompt()

    def _generate_prompt(self):

        prompt = self.prompt_string

        for replace in self.placeholders.keys():
            prompt = prompt.replace(replace,self.placeholders[replace])

        return prompt
