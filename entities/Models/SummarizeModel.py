from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Any


class BaseSummarizerModel:
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings: Any, prompt_template: PromptTemplate):
        """
        Initializes the BaseSummarizerModel with the given parameters.

        :param api_key: The API key for Google Generative AI.
        :param model: The model to use.
        :param temperature: The temperature setting for the model.
        :param safety_settings: Safety settings for the model.
        :param prompt_template: A PromptTemplate instance.
        """
        self._initialize_llm(api_key, model, temperature, safety_settings, prompt_template)

    def _initialize_llm(self, api_key: str, model: str, temperature: float, safety_settings: Any, prompt_template: PromptTemplate):
        """
        Initializes the model with the given parameters.

        :param api_key: The API key for Google Generative AI.
        :param model: The model to use.
        :param temperature: The temperature setting for the model.
        :param safety_settings: Safety settings for the model.
        :param prompt_template: A PromptTemplate instance.
        """
        self._llm = ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model=model,
            temperature=temperature,
            safety_settings=safety_settings
        )
        
        self._prompt_template = prompt_template
        self._parser = StrOutputParser()
        self._chain = self._prompt_template | self._llm | self._parser

    def __repr__(self) -> str:
        """
        Returns a string representation of the BaseSummarizerModel instance.
        """
        return (
            f"{self.__class__.__name__}(api_key=****, model={self._llm.model}, "
            f"temperature={self._llm.temperature}, safety_settings={self._llm.safety_settings})"
        )

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the BaseSummarizerModel instance.
        """
        return (
            f"BaseSummarizerModel using model '{self._llm.model}' with temperature "
            f"{self._llm.temperature} and specified safety settings."
        )

    def __eq__(self, other: Any) -> bool:
        """
        Checks equality between this instance and another BaseSummarizerModel instance.
        """
        if isinstance(other, BaseSummarizerModel):
            return (
                self._llm.model == other._llm.model and
                self._llm.temperature == other._llm.temperature and
                self._llm.safety_settings == other._llm.safety_settings
            )
        return False



class MemorySummarizerModel(BaseSummarizerModel):
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings: Any):
        """
        Initializes the ModelAsk with the given parameters by calling the parent class constructor.

        :param api_key: The API key for Google Generative AI.
        :param model: The model to use.
        :param temperature: The temperature setting for the model.
        :param safety_settings: Safety settings for the model.
        :param prompt_template: A PromptTemplate instance.
        """
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
        
        prompt_template = PromptTemplate(input_variables=["memory_buffer", "input", "response"], template=template)

        super().__init__(api_key, model, temperature, safety_settings, prompt_template)


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
    

class SearchSummarizeModel(BaseSummarizerModel):
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings: Any):
        """
        Initializes the SearchSummerizeModel with the given parameters by calling the parent class constructor.

        :param api_key: The API key for Google Generative AI.
        :param model: The model to use.
        :param temperature: The temperature setting for the model.
        :param safety_settings: Safety settings for the model.
        :param prompt_template: A PromptTemplate instance.
        """
        template = """
            Given the following search result and the user description you have to summerize the search result based on the user description:

            Search Result:
            {input}

            User description:
            {description}

            Summary:
        """
        
        prompt_template = PromptTemplate(input_variables=["input", "description"], template=template)

        super().__init__(api_key, model, temperature, safety_settings, prompt_template)


    def summarize_search(self, input: str, description: str) -> str:
        """
        summarize search results and returns the summerized search.

        :param input: The new input to the model.
        :param description: user description for how to summerize.
        :return: the summerizeed search.
        """
    
        chunks = []

        for chunk in self._chain.stream({"input":{input},"description":{description}}):
            print(chunk, end='', flush=True)
            chunks.append(chunk)

        return ''.join(chunks)