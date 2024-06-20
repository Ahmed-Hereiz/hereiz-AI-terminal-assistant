from typing import Any
from langchain_core.output_parsers import StrOutputParser
from agent_llm import BaseLLM

class SimpleLLM(BaseLLM):
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings: Any):
        """Uses default BaseLLM generate method"""

        parser = StrOutputParser()
        initialize_verbose = False

        super().__init__(api_key, model, temperature, safety_settings, parser=parser, initialize_verbose=initialize_verbose)



class SimpleInvokeLLM(SimpleLLM):
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings: Any):
        super().__init__(api_key, model, temperature, safety_settings)


    def llm_generate(self, input: str) -> str:
        
        return self.invoke_response(input=input)



class SimpleStreamLLM(SimpleLLM):
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings: Any):
        super().__init__(api_key, model, temperature, safety_settings)


    def llm_generate(self, input: str) -> str:
        
        return self.generate_response(input=input)