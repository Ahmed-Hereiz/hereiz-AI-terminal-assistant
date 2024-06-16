from typing import Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

class BaseAgent:
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings: Any, parser: Any = StrOutputParser(), initialize_verbose: bool = False):
        """
        Initializes the BaseAgent with the given parameters.

        :param api_key: The API key for the model.
        :param model: The model to use (e.g., "gemini-pro").
        :param temperature: The temperature setting for the model, controlling the randomness of the output.
        :param safety_settings: Safety settings for the model to ensure appropriate responses.
        :param parser: The parser to process model outputs. Defaults to StrOutputParser.
        :param initialize_verbose: If True, displays warnings during initialization if there are issues.
        """
        self._api_key = api_key
        self._model = model
        self._temperature = temperature
        self._safety_settings = safety_settings
        self._parser = parser
        self._initialize_verbose = initialize_verbose
        self._llm = self._initialize_llm() 
        self._chain = self._initialize_chain(self._initialize_verbose)
        self.agent_name = None


    def _initialize_llm(self):
        """
        Initializes the language model (LLM) used inside the BaseAgent.

        :raises ValueError: If an unsupported model is specified.
        :return: The initialized LLM.
        """
        if self._model == "gemini-pro":
            return ChatGoogleGenerativeAI(
                google_api_key=self._api_key,
                model=self._model,
                temperature=self._temperature,
                safety_settings=self._safety_settings
            )
        else:
            self._llm = None
            raise ValueError('No other models implemented for the Agents yet')


    def _initialize_chain(self, initialize_verbose: bool = False):
        """
        Initializes the chain used inside the BaseAgent.

        :param initialize_verbose: If True, displays warnings during initialization.
        :return: The initialized chain, or None if initialization fails.
        """
        if self._llm is not None:
            try:
                return self._llm | self._parser
            except Exception as e:
                if initialize_verbose:
                    print(f"Warning! Error initializing chain with {self._parser}: {e}")
                    print("Initializing the chain using a default langchain StrOutputParser parser instead!")
                return self._llm | StrOutputParser()
        return None


    def generate_response(self, input: str) -> str:
        """
        Generates a response from the chain using the given input.

        :param input: The input string to generate a response for.
        :raises ValueError: If the agent chain is not initialized.
        :return: The generated response as a string.
        """
        if self._chain is None:
            raise ValueError("Agent chain is not initialized.")
        
        chunks = []
        for chunk in self._chain.stream(input=input):
            print(chunk, end='', flush=True)
            chunks.append(chunk)
        return ''.join(chunks)


    def invoke_response(self, input: str) -> str:
        """
        Directly invokes the LLM with the given input and returns the response.

        :param input: The input string to invoke the LLM with.
        :raises ValueError: If the LLM is not initialized.
        :return: The LLM's response as a string.
        """
        if self._llm is None:
            raise ValueError("LLM is not initialized.")
        return self._llm.invoke(input=input)


    def __repr__(self) -> str:
        """
        Returns a string representation of the BaseAgent instance, useful for debugging.

        :return: A string representation of the instance.
        """
        llm_initialized = self._llm is not None
        chain_initialized = self._chain is not None
        return f"Model used: {self._model}, with temperature: {self._temperature}, llm_initialized: {llm_initialized}, chain_initialized: {chain_initialized}"


    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the BaseAgent instance.

        :return: A string representation of the instance.
        """
        llm_initialized = self._llm is not None
        chain_initialized = self._chain is not None
        return f"Model used: {self._model}, with temperature: {self._temperature}, llm_initialized: {llm_initialized}, chain_initialized: {chain_initialized}"


    @property
    def llm(self) -> Any:
        """
        Returns the language model (LLM) instance.

        :return: The LLM instance.
        """
        return self._llm


    @property
    def parser(self) -> Any:
        """
        Returns the parser instance.

        :return: The parser instance.
        """
        return self._parser


    @property
    def chain(self) -> Any:
        """
        Returns the chain instance.

        :return: The chain instance.
        """
        return self._chain
    

    @property
    def agent_name(self):
        """
        Returns a name if specified for the agent 
        """
        return self.agent_name
    
    @agent_name.setter
    def agent_name(self, name):
        """
        setter for the agent to give it a name
        """
        self.agent_name = str(name)

