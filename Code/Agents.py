from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain

class Agent:
    def __init__(self, api_key, agent_template, model, temperature, safety_settings):
        
        self.agent_llm = ChatGoogleGenerativeAI(google_api_key=api_key,
                                            model=model,
                                            temperature=temperature,
                                            safety_settings=safety_settings
                                            )
        
        self.prompt_template = PromptTemplate(input_variables=["input"], template=agent_template)


    def make_plan(self, user_input):

        conversation = ConversationChain(prompt=self.prompt_template,llm=self.agent_llm, verbose=False)

        plan = conversation.predict(input=user_input)
        return plan
    
    def make_code(self, planner_input):

        conversation = ConversationChain(prompt=self.prompt_template,llm=self.agent_llm, verbose=False)

        code = conversation.predict(input=planner_input)
        return code
    
