from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
import time

class Agent:
    def __init__(self, api_key, agent_template, model, temperature, safety_settings):
        self.initialize_agent(api_key, agent_template, model, temperature, safety_settings)

    def initialize_agent(self, api_key, agent_template, model, temperature, safety_settings):
        self.agent_llm = ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model=model,
            temperature=temperature,
            safety_settings=safety_settings
        )
        self.prompt_template = PromptTemplate(input_variables=["input"], template=agent_template)

class Planner(Agent):
    def make_plan(self, user_input):
        conversation = ConversationChain(prompt=self.prompt_template, llm=self.agent_llm, verbose=False)
        plan = conversation.predict(input=user_input)
        with open("tmp_plan", "w") as file:
            file.write(plan)

class Coder(Agent):
    def write_code(self):
        with open("tmp_plan","r") as file:
            plan = file.read()

        conversation = ConversationChain(prompt=self.prompt_template, llm=self.agent_llm, verbose=False)
        code = conversation.predict(input=plan)
        with open("code_file.py", "w") as file:
            file.write(code)

class Debuger(Agent):
    def debug_code(self):
        with open("code_file.py", "r") as file:
            code = file.read()

        conversation = ConversationChain(prompt=self.prompt_template, llm=self.agent_llm, verbose=False)
        debugged_code = conversation.predict(input=code)
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        debugged_filename = f"debugged_code_{timestamp}.py"

        with open(debugged_filename, "w") as debugged_file:
                debugged_file.write(debugged_code)

        print(f"Debugged code saved as {debugged_filename}")


class Tester(Agent):
    def test_script(self):
        pass


class Documenter(Agent):
    def document_file(self):
        pass

