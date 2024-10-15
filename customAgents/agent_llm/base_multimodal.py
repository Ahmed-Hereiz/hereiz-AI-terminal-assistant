from colorama import Fore, Style
from typing import Any
from PIL import Image
from customAgents.agent_llm.type_utils import agent_multimodal_type
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
            genai.configure(
                api_key=self._api_key,
                transport="rest"
            )
            return genai.GenerativeModel(
                model_name=self._model,
                safety_settings=self._safety_settings
            )
        else:
            self._multi_modal = None
            raise ValueError('Model not supported. currently supported models is gemini')


    def multimodal_generate(self, prompt: str, img: Image, stream: bool=False, output_style: str='default'):
        
        response = self._multi_modal.generate_content([prompt, img], stream=stream)
        
        if stream:
            chunks = []
            for chunk in response:
                if output_style is not None:
                    self._print_colorized_output(chunk=chunk.text,output_style=output_style)
                chunks.append(chunk.text) 
            return ''.join(chunks)
        
        else:
            response.resolve()
            return response.text



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


    def __str__(self) -> str:
    
        multimodal_initialized = self._multi_modal is not None

        return f"Model used: {self.model}, wth temperature: {self._temperature}, multimodal initialized: {multimodal_initialized}"


    def __str__(self) -> str:
    
        multimodal_initialized = self._multi_modal is not None

        return f"Model used: {self._model}, wth temperature: {self._temperature}, multimodal initialized: {multimodal_initialized}"


    @property
    def multimodal(self) -> Any:
        
        return self._multi_modal
    

    @property
    def available_text_colors(self):
        return ['default', 'green', 'blue', 'yellow', 'cyan', 'red', 'magenta']