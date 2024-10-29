from typing import Any, Optional
from PIL import Image
from customAgents.agent_llm import BaseMultiModal


class SimpleMultiModal(BaseMultiModal):
    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float = 0.7,
        safety_settings: Any = None,
        max_output_tokens: Optional[int] = None
    ):
        """Uses default BaseMultiModal generate method"""

        super().__init__(
            api_key,
            model,
            temperature,
            safety_settings,
            max_output_tokens
        )

    def multimodal_generate(self, prompt: str, img: Image, stream: bool = False, output_style: str = 'default'):
        return super().multimodal_generate(prompt, img, stream, output_style)