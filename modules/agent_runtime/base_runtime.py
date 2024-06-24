from typing import Any


class BaseRuntime:
    def __init__(self, llm: Any, prompt: Any, tools: Any):
        """
        Initializes the BaseRuntime with the given LLM, prompt, and tools.

        :param llm: The language model to be used.
        :param prompt: The prompt for the agent.
        :param tools: Tools that assist the agent.
        """
        self.llm = llm
        self.prompt = prompt
        self.tools = tools


    def step(self) -> str:
        """
        Generates a response from the LLM using the current agent prompt.

        :raises ValueError: If the LLM or agent prompt is not properly initialized.
        :return: The generated response as a string.
        """
        if not self.llm or not self.prompt:
            raise ValueError("LLM or agent prompt is not properly initialized.")
        response = self.llm.llm_generate(input=self.prompt.prompt)
        return response


    def loop(self, n_steps: int = 1) -> str:
        """
        Continuously generates responses for a specified number of steps.

        :param n_steps: The number of steps to generate responses for.
        :return: The final response generated after the specified number of steps.
        """
        for _ in range(n_steps):
            response = self.step()
            self.prompt.prompt += f"\n{response}"

        return response