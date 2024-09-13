from typing import Any
from customAgents.agent_llm.type_utils import agent_multimodal_type
from PIL import Image
import google.generativeai as genai


@agent_multimodal_type
class BaseMultiModal:
    def __init__(
            self,
            api_key: str,
            model: str,
            temperature: float,
            safety_settings: Any = None
        ):
        
        self._api_key = api_key
        self._model = model
        self._temperature = temperature
        self._safety_settings = safety_settings
        self._multi_modal = self._initialize_multimodal()


    def _initialize_multimodal(self):
        if self._model.startswith("gemini"): # Google models
            return genai.GenerativeModel(
                model_name=self._model,
                safety_settings=self._safety_settings
            )
        else:
            self._multi_modal = None
            raise ValueError('Model not supported. currently supported models is gemini')


    def multimodal_generate(self, prompt: str, img: Image, stream=False):
        
        response = self._multi_modal.generate_content([prompt, img], stream=stream)
        response.resolve()

        return response.text


    def __str__(self) -> str:
    
        multimodal_initialized = self._multi_modal is not None

        return f"Model used: {self.model}, wth temperature: {self._temperature}, multimodal initialized: {multimodal_initialized}"


    def __str__(self) -> str:
    
        multimodal_initialized = self._multi_modal is not None

        return f"Model used: {self.model}, wth temperature: {self._temperature}, multimodal initialized: {multimodal_initialized}"


    @property
    def multimodal(self) -> Any:
        
        return self._multi_modal