from langchain_google_genai import ChatGoogleGenerativeAI
from colorama import Fore

from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain

class ModelChat:
    def __init__(self, api_key, model, temperature, safety_settings, prompt_template, parser, memory_buffer):
        self.initialize_agent(api_key, model, temperature, safety_settings, prompt_template, parser, memory_buffer)

    def initialize_agent(self, api_key, model, temperature, safety_settings, prompt_template, parser, memory_buffer):

        self.llm = ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model=model,
            temperature=temperature,
            safety_settings=safety_settings
        )

        self.prompt_template = prompt_template

        self.parser = parser

        self.memory_buffer = memory_buffer

        self.chain = self.prompt_template | self.llm | self.parser

    def _generate_stream(self, model_input):

        for chunk in self.chain.stream({"input":{model_input}}):
            print(chunk, end='', flush=True)
 
        print(Fore.WHITE,"\n")

def model_chat(api_key, template, input_text, memory_buffer, model, temperature, safety_settings):

    llm = ChatGoogleGenerativeAI(google_api_key=api_key,
                                 model=model,
                                 temperature=temperature,
                                 safety_settings=safety_settings
                                )
    
    prompt_template = PromptTemplate(input_variables=["history", "input"], template=template)

    memory = ConversationSummaryMemory(llm=llm, max_token_limit=1000,buffer=memory_buffer)

    conversation = ConversationChain(
        prompt=prompt_template,
        llm=llm, 
        verbose=False,
        memory=memory
    )
    
    response = conversation.predict(input=input_text)

    return response, memory.buffer
