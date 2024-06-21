from agent_prompt import ChatPrompt


class HumanLoopChatPrompt(ChatPrompt):
    def __init__(self, prompt_string: str = "", user_input: str = "", memory_string: str = None):
        super().__init__(prompt_string, user_input, memory_string)

        self.user_input = user_input
        self.memory_string = memory_string
        #self.aditional_instructions = "### Instructions\n1. Output your response.\n2. Wait for human feedback.\n3. If feedback is given, revise your response based on the feedback and attempt the task again."
        #self.prompt = self._generate_prompt()

    # def _generate_prompt(self):
        
    #     prompt = super()._generate_prompt()

    #     return prompt.replace("{aditional}",self.aditional_instructions)
    