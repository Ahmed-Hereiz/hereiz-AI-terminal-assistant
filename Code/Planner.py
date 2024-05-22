from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
import json

with open('../config.json', 'r') as f:
    config = json.load(f)

with open('../templates/planner_agent.txt', 'r') as template_file:
    template = template_file.read()

api_key = config['api_key']

class Planner:
    def __init__(self,api_key,template):
        
        self.llm = ChatGoogleGenerativeAI(google_api_key=api_key,
                                          model="gemini-pro",
                                          temperature=0.7,
                                          safety_settings=
                                          {
                                            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                                            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                                            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                          },
                                          )
        
        self.prompt_template = PromptTemplate(input_variables=["input"], template=template)


    def make_plan(self, user_input):

        conversation = ConversationChain(prompt=self.prompt_template,llm=self.llm, verbose=False)

        plan = conversation.predict(input=user_input)
        return plan
    

p = Planner(api_key=api_key,template=template)
plan = p.make_plan(user_input="I want to make code to make a neural network in pytorch")

print(plan)