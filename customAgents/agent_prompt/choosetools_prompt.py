from customAgents.agent_prompt import BasePrompt


class ChooseToolsPrompt(BasePrompt):
    def __init__(self, task: str, prompt_string: str = ""):

        self.task = task

        super().__init__(prompt_string)

        self.prompt = self._generate_prompt()


    def _generate_prompt(self):
        choose_tools_prompt = """
{prompt_string}
You are an LLM tool user expert your task is to choose the most usefull tools to solve this task :
{task}

The available tools you have :
{tools}
"""

        choose_tools_prompt = choose_tools_prompt.replace("{task}",self.task)
        choose_tools_prompt = choose_tools_prompt.replace("{prompt_strina}",self.prompt_string)

        return choose_tools_prompt
