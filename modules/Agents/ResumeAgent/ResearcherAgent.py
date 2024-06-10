from utils import add_root_to_path
hereiz_root = add_root_to_path()

from modules.Agents import BaseAgent

class RedirectSearchResearch(BaseAgent):
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings: Any, parser: Any, template=None):
        super().__init__(api_key, model, temperature, safety_settings, template, parser)
        
        self._chain = self._llm | self._parser

    def generate_response(self, input: str) -> str:

        return self._chain.invoke(input=input)
