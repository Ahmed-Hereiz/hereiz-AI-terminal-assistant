from typing import Any
from customAgents.agent_llm import BaseMultiModal


class SimpleMultiModal(BaseMultiModal):
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings: Any = None):
        """Uses default BaseMultiModal generate method"""

        super().__init__(api_key, model, temperature, safety_settings)
