from langchain_google_genai import ChatGoogleGenerativeAI
from colorama import Fore

class ModelAsk:
    def __init__(self, api_key, model, temperature, safety_settings, prompt_template, parser):
        self.initialize_agent(api_key, model, temperature, safety_settings, prompt_template, parser)

    def initialize_agent(self, api_key, model, temperature, safety_settings, prompt_template, parser):

        self.llm = ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model=model,
            temperature=temperature,
            safety_settings=safety_settings
        )

        self.prompt_template = prompt_template

        self.parser = parser

        self.chain = self.prompt_template | self.llm | self.parser

    def _generate_stream(self, model_input):

        print(Fore.CYAN+"Hereiz : ")

        for chunk in self.chain.stream({"input":{model_input}}):
            print(chunk, end='', flush=True)
 
        print(Fore.WHITE,"\n")