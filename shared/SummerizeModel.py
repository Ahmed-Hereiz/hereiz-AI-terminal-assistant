from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Any

class MemorySummarizerModel:
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings: Any):
        """
        Initializes the MemorySummarizerModel with the given parameters.

        :param api_key: The API key for Google Generative AI.
        :param model: The model to use.
        :param temperature: The temperature setting for the model.
        :param safety_settings: Safety settings for the model.
        """
        self._initialize_agent(api_key, model, temperature, safety_settings)

    def _initialize_agent(self, api_key: str, model: str, temperature: float, safety_settings: Any):
        """
        Initializes the agent with the given parameters.

        :param api_key: The API key for Google Generative AI.
        :param model: The model to use.
        :param temperature: The temperature setting for the model.
        :param safety_settings: Safety settings for the model.
        """
        self._llm = ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model=model,
            temperature=temperature,
            safety_settings=safety_settings
        )
        
        template = """
            Given the following conversation history and new input, provide a concise summary that captures the essential points:

            Conversation summary:
            {memory_buffer}

            New Input:
            {input}

            Model Response:
            {response}

            Summary:
        """
        
        self._prompt_template = PromptTemplate(input_variables=["memory_buffer", "input", "response"], template=template)
        self._parser = StrOutputParser()
        self._chain = self._prompt_template | self._llm | self._parser

    def __repr__(self) -> str:
        """
        Returns a string representation of the MemorySummarizerModel instance.
        """
        return (
            f"{self.__class__.__name__}(api_key=****, model={self._llm.model}, "
            f"temperature={self._llm.temperature}, safety_settings={self._llm.safety_settings})"
        )

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the MemorySummarizerModel instance.
        """
        return (
            f"MemorySummarizer using model '{self._llm.model}' with temperature "
            f"{self._llm.temperature} and specified safety settings."
        )

    def __eq__(self, other: Any) -> bool:
        """
        Checks equality between this instance and another MemorySummarizer instance.
        """
        if isinstance(other, MemorySummarizerModel):
            return (
                self._llm.model == other._llm.model and
                self._llm.temperature == other._llm.temperature and
                self._llm.safety_settings == other._llm.safety_settings
            )
        return False

    def add_memory(self, memory_buffer: str, input: str, response: str) -> str:
        """
        Adds a new memory to the conversation buffer and returns the updated buffer.

        :param memory_buffer: The existing conversation memory buffer.
        :param input: The new input to the model.
        :param response: The model's response to the new input.
        :return: The updated memory buffer.
        """
        new_buffer_memory = self._chain.invoke({
            "memory_buffer": memory_buffer,
            "input": input,
            "response": response
        })
        return new_buffer_memory

    @property
    def llm(self) -> ChatGoogleGenerativeAI:
        """
        Returns the language model instance.
        """
        return self._llm

    @property
    def prompt_template(self) -> PromptTemplate:
        """
        Returns the prompt template.
        """
        return self._prompt_template

    @property
    def parser(self) -> StrOutputParser:
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
