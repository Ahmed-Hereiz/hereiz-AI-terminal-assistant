from typing import Any
from colorama import Fore, Style
from customAgents.agent_llm.type_utils import agent_llm_type
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


@agent_llm_type
class BaseLLM:
    def __init__(
            self,
            api_key: str,
            model: str,
            temperature: float,
            safety_settings: Any = None,
            parser: Any = StrOutputParser(),
            initialize_verbose: bool = False
        ):
        
        """
        Initializes the BaseLLM with the given parameters.

        :param api_key: The API key for the model.
        :param model: The model to use (e.g., "gemini-pro").
        :param temperature: The temperature setting for the model, controlling the randomness of the output.
        :param safety_settings: Safety settings for the model to ensure appropriate responses.
        :param parser: The parser to process model outputs. Defaults to StrOutputParser.
        :param initialize_verbose: If True, displays warnings during initialization if there are issues.
        :param json_response: If True, the model will return a JSON response instead of a string.
        :param max_tokens: The maximum number of tokens to generate in a single response.
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
        Initializes the language model (LLM) used inside the BaseLLM.

        :raises ValueError: If an unsupported model is specified.
        :return: The initialized LLM.
        """

        if self._model.startswith("gemini"): # Google models
            return ChatGoogleGenerativeAI(
                google_api_key=self._api_key,
                model=self._model,
                temperature=self._temperature,
                safety_settings=self._safety_settings
            )
        
        elif self._model.startswith("gpt"): # OpenAI models
            return ChatOpenAI(
                api_key=self._api_key,
                model=self._model,
                temperature = self._temperature,
            )
        
        elif self._model.startswith("claude"): # Anthropic models
            return ChatAnthropic(
                api_key=self._api_key,
                model=self._model,
                temperature=self._temperature,
            )
        else:
            self._llm = None
            raise ValueError('Model not supported, currently supported models are gemini, gpt, claude')


    def _initialize_chain(self, initialize_verbose: bool = False):
        """
        Initializes the chain used inside the BaseLLM.

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


    def generate_response(self, input: str, output_style: str = 'default') -> str:
        """
        Generates a response from the chain using the given input.

        :param input: The input string to generate a response for.
        :param output_style: style the color of the response (can be one of this : 'default', 'green', 'blue', 'yellow', 'cyan', 'red', 'magenta').
        :raises ValueError: If the llm chain is not initialized.
        :return: The generated response as a string.
        """
        
        if self._chain is None:
            raise ValueError("LLM chain is not initialized.")

        chunks = []
        for chunk in self._chain.stream(input=input):
            if output_style is not None:
                self._print_colorized_output(chunk=chunk,output_style=output_style)
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
        return self._llm.invoke(input=input).content


    def llm_generate(self, input: str) -> str:
        """
        method for interfacing with runtime (used inside the runtime class), setting default to use invoke,
        but this needs to overwritten inside every inherited class for being customizable for the use case.

        :param input: The input string to generate a response for.
        """

        return self.invoke_response(input=input)
    

    def _print_colorized_output(self, chunk: str, output_style: str) -> None:
        """
        method for customizing output color

        :param chunk: the output that needs to be printed.
        :param output_style: the color of the output.
        """

        allowed_styles = ['default', 'green', 'blue', 'yellow', 'cyan', 'red', 'magenta']

        if output_style not in allowed_styles:
            raise ValueError(f"Invalid output style. Choose from {allowed_styles}")

        if output_style == "default":
            print(chunk, end='', flush=True)
        elif output_style == "green":
            print(Fore.LIGHTGREEN_EX + chunk + Style.RESET_ALL, end='', flush=True)
        elif output_style == "blue":
            print(Fore.LIGHTBLUE_EX + chunk + Style.RESET_ALL, end='', flush=True)
        elif output_style == "yellow":
            print(Fore.LIGHTYELLOW_EX + chunk + Style.RESET_ALL, end='', flush=True)
        elif output_style == "cyan":
            print(Fore.LIGHTCYAN_EX + chunk + Style.RESET_ALL, end='', flush=True)
        elif output_style == "red":
            print(Fore.LIGHTRED_EX + chunk + Style.RESET_ALL, end='', flush=True)
        elif output_style == "magenta":
            print(Fore.LIGHTMAGENTA_EX + chunk + Style.RESET_ALL, end='', flush=True)

        return None        


    def __repr__(self) -> str:
        """
        Returns a string representation of the BaseLLM instance, useful for debugging.

        :return: A string representation of the instance.
        """

        llm_initialized = self._llm is not None
        chain_initialized = self._chain is not None
        return f"Model used: {self._model}, with temperature: {self._temperature}, llm_initialized: {llm_initialized}, chain_initialized: {chain_initialized}"


    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the BaseLLM instance.

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
    def available_text_colors(self):
        return ['default', 'green', 'blue', 'yellow', 'cyan', 'red', 'magenta']
    
    