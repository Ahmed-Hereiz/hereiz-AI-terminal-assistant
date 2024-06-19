from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Any


class BaseAgent:
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings: Any, template: Any, parser: Any):
        """
        Initializes the BaseAgent with the given parameters.

        :param api_key: The API key for Google Generative AI.
        :param model: The model to use.
        :param temperature: The temperature setting for the model.
        :param safety_settings: Safety settings for the model.
        :param prompt_template: The prompt template to use.
        :param parser: The parser to use.
        """
        self._initialize_agent(api_key, model, temperature, safety_settings, template, parser)

    def _initialize_agent(self, api_key: str, model: str, temperature: float, safety_settings: Any, template: Any, parser: Any):
        """
        Initializes the agent with the given parameters.

        :param api_key: The API key for Google Generative AI.
        :param model: The model to use.
        :param temperature: The temperature setting for the model.
        :param safety_settings: Safety settings for the model.
        :param prompt_template: The prompt template to use.
        :param parser: The parser to use.
        """
        self._llm = ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model=model,
            temperature=temperature,
            safety_settings=safety_settings
        )
        self._template = template
        self._parser = parser
    

