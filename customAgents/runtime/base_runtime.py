import json
from typing import Union
from customAgents.agent_llm import BaseLLM, BaseMultiModal
from customAgents.agent_prompt import BasePrompt
from customAgents.agent_tools import ToolKit


class BaseRuntime:
    def __init__(self, llm: Union[BaseLLM, BaseMultiModal], prompt: BasePrompt, toolkit: ToolKit):
        """
        Initializes the BaseRuntime with the given LLM, prompt, and tools.

        :param llm: The language model to be used.
        :param prompt: The prompt for the agent.
        :param tools: Tools that assist the agent.
        """
        self.llm = llm
        self.prompt = prompt
        self.toolkit = toolkit


    def step(self) -> str:
        """
        Generates a response from the LLM using the current agent prompt.

        :raises ValueError: If the LLM or agent prompt is not properly initialized.
        :return: The generated response as a string.
        """
        if not self.llm or not self.prompt:
            raise ValueError("LLM or agent prompt is not properly initialized.")
        if isinstance(self.llm, BaseLLM):
            response = self.llm.llm_generate(input=self.prompt.prompt)
            return response
        elif isinstance(self.llm, BaseMultiModal):
            if self.prompt.img is None:
                response = self.llm.multimodal_generate(prompt=self.prompt.prompt)
            else:
                response = self.llm.multimodal_generate(prompt=self.prompt.prompt,img=self.prompt.img)
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
    

    def _extract_json_from_string(self, text: str):

        json_objects = []
        brace_stack = []
        json_str = ""
        inside_json = False

        for _, char in enumerate(text):
            if char == '{':
                brace_stack.append(char)
                inside_json = True
            if inside_json:
                json_str += char
            if char == '}':
                brace_stack.pop()
                if not brace_stack:
                    inside_json = False
                    try:
                        json_object = json.loads(json_str)
                        json_objects.append(json_object)
                    except json.JSONDecodeError:
                        pass
                    json_str = ""

        return json_objects