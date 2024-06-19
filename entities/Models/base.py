from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Any

class BaseModel:
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings: Any, prompt_template: Any, parser: Any):
        """
        Initializes the BaseModel with the given parameters.

        :param api_key: The API key for Google Generative AI.
        :param model: The model to use.
        :param temperature: The temperature setting for the model.
        :param safety_settings: Safety settings for the model.
        :param prompt_template: The prompt template to use.
        :param parser: The parser to use.
        """
        self._initialize_agent(api_key, model, temperature, safety_settings, prompt_template, parser)

    def _initialize_agent(self, api_key: str, model: str, temperature: float, safety_settings: Any, prompt_template: Any, parser: Any):
        """
        Initializes the BaseModel with the given parameters.

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
        self._prompt_template = prompt_template
        self._parser = parser
        self._chain = self._prompt_template | self._llm | self._parser

    def __repr__(self) -> str:
        """
        Returns a string representation of the BaseModel instance.
        """
        return (
            f"{self.__class__.__name__}(api_key=****, model={self._llm.model}, "
            f"temperature={self._llm.temperature}, safety_settings={self._llm.safety_settings}, "
            f"prompt_template={self._prompt_template}, parser={self._parser})"
        )

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the BaseModel instance.
        """
        return (
            f"Using model '{self._llm.model}' with temperature "
            f"{self._llm.temperature} and specified safety settings."
        )

    def __eq__(self, other: Any) -> bool:
        """
        Checks equality between this instance and another ChainBasicModel instance.
        """
        if isinstance(other, BaseModel):
            return (
                self._llm.model == other._llm.model and
                self._llm.temperature == other._llm.temperature and
                self._llm.safety_settings == other._llm.safety_settings and
                self._prompt_template == other._prompt_template and
                self._parser == other._parser
            )
        return False

    def update_settings(self, temperature: float = None, safety_settings: Any = None):
        """
        Updates the temperature and safety settings of the language model.

        :param temperature: New temperature setting.
        :param safety_settings: New safety settings.
        """
        if temperature is not None:
            self._llm.temperature = temperature
        if safety_settings is not None:
            self._llm.safety_settings = safety_settings

    @property
    def llm(self) -> ChatGoogleGenerativeAI:
        """
        Returns the language model instance.
        """
        return self._llm

    @property
    def prompt_template(self) -> Any:
        """
        Returns the prompt template.
        """
        return self._prompt_template

    @property
    def parser(self) -> Any:
        """
        Returns the parser.
        """
        return self._parser

    @property
    def chain(self) -> Any:
        """
        Returns the chain.
        """
        return self._chain
