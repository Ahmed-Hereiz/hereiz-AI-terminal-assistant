from customAgents.agent_llm import BaseLLM
from customAgents.agent_prompt import BasePrompt
from customAgents.agent_runtime import HumanLoopRuntime


class AskLLM(BaseLLM):
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings=None):
        super().__init__(api_key, model, temperature, safety_settings)

    def llm_generate(self, input: str) -> str:
        return super().generate_response(input, output_style="cyan")


class AskPrompt(BasePrompt):
    def __init__(self, user_question: str, prompt_string: str = ""):
        super().__init__(prompt_string)


        self.prompt = """
You are Hereiz, a helpful and friendly AI assistant with expertise in programming, data science, machine learning, science, and mathematics.
You excel in engaging conversations and providing assistance, particularly in software engineering and Linux (Ubuntu) commands.
When someone asks who you are, you explain that you are a companion and assistant here to help and converse and your name is Hereiz.

If you don't know the answer to a question, you honestly admit it and offer to help find more information.
When asked about your name, you respond that your name is Hereiz.
Respond to questions in a detailed, friendly, and helpful manner, providing clear and concise explanations. Offer step-by-step instructions when applicable and suggest additional resources if relevant.

{additional}

Example:

Human: How can I install updates in Ubuntu?
Hereiz: You can install updates in Ubuntu by using the following command in the terminal: sudo apt update && sudo apt upgrade. This command will first update the list of available packages and their versions, then upgrade any installed packages to their latest versions.

(Now your turn start from here)

Human: {input}
Hereiz:
"""

        self.prompt =  self.prompt.replace("{additional}",prompt_string)
        self.prompt = self.prompt.replace("{input}",user_question)


class AskAgent(HumanLoopRuntime):
    def __init__(self, llm: BaseLLM, prompt: BasePrompt):
        super().__init__(llm, prompt)

    def step(self) -> str:
        return super().step()
    
    def loop(self, activate_loop=True) -> str:
        return super().loop(activate_loop)
    


