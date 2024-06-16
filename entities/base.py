from typing import Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

class BaseAgent:
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings: Any, parser: Any = StrOutputParser(), initialize_verbose: bool = False):
        """
        Initializes the BaseAgent with the given parameters.

        :param api_key: The API key for the model.
        :param model: The model to use.
        :param temperature: The temperature setting for the model.
        :param safety_settings: Safety settings for the model.
        :param parser: The parser to use.
        :param initialize_verbose: shows warnings while initializing the agent.
        """

        self._api_key = api_key
        self._model = model
        self._temperature = temperature
        self._safety_settings = safety_settings
        self._parser = parser
        self._initialize_verbose = initialize_verbose
        self._llm = self._initialize_llm() 
        self._chain = self._initialize_chain(self._initialize_verbose)


    def _initialize_llm(self):
        """
        Initializes the llm used inside the BaseAgent
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
        Initializes the chain used inside the BaseAgent
        """

        if self._llm is not None:
            try:
                return self._llm | self._parser
            except Exception as e:
                if initialize_verbose:
                    print(f"Warning ! Error initializing chain with {self._parser} : \n\n{e}")
                    print(f"Initializing the chain using a default langchain StrOutputParser parser instead !! ")
                return self._llm | StrOutputParser()
        return None


    def generate_response(self, input: str) -> str:
         
        if self._chain is None:
            raise ValueError("Agent chain is not initialized.")

        chunks = []

        for chunk in self._chain.stream(input=input):
            print(chunk, end='', flush=True)
            chunks.append(chunk)

        return ''.join(chunks)
    

    def invoke_response(self, input: str) -> str:
        
        if self._llm is None:
            raise ValueError("LLM is not initialized.")

        return self._llm.invoke(input=input)
    

    def __repr__(self) -> str:
        """
        Returns a string representation of the BaseModel instance.
        """
        
        llm_initialized = True if self._llm is not None else False
        chain_initialized = True if self._chain is not None else False

        return f"Model used {self._model}, with temperature : {self._temperature}, llm initialized = {llm_initialized}, chain_initialized = {chain_initialized}"


    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the BaseModel instance.
        """

        llm_initialized = True if self._llm is not None else False
        chain_initialized = True if self._chain is not None else False

        return f"Model used {self._model}, with temperature : {self._temperature}, llm initialized = {llm_initialized}, chain_initialized = {chain_initialized}"


    @property
    def llm(self) -> Any:
        """
        Returns the language model instance.
        """
        return self._llm


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

