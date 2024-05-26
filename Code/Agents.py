from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
import time
import json

class Agent:
    def __init__(self, api_key, model, temperature, safety_settings, prompt_template, parser):
        self.initialize_agent(api_key, model, temperature, safety_settings, prompt_template, parser)

    def initialize_agent(self, api_key, model, temperature, safety_settings, prompt_template, parser):

        self.agent_llm = ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model=model,
            temperature=temperature,
            safety_settings=safety_settings
        )

        self.prompt_template = prompt_template

        self.parser = parser

    def _generate_stream(self, model_input, chain):

        chunks = []

        for chunk in chain.stream({"input":{model_input}}):
            print(chunk, end='', flush=True)
            chunks.append(chunk)

        return ''.join(chunks)

class Planner(Agent):
    def make_plan(self, user_input):

        chain = self.prompt_template | self.agent_llm | self.parser
        
        plan = self._generate_stream(user_input,chain)

        with open("tmp_plan", "w") as file:
            file.write(plan)

class Coder(Agent):
    def write_code(self):
        with open("tmp_plan","r") as file:
            plan = file.read()

        chain = self.prompt_template | self.agent_llm | self.parser
        
        code = self._generate_stream(plan,chain)

        with open("code_file.py", "w") as file:
            file.write(code)


class FileRunner(Agent):
    def run_file(self):
        with open("code_file.py","r") as file:
            code = file.read()
        
        chain = self.prompt_template | self.agent_llm | self.parser
        classsify = chain.invoke({
            "input":{code},
            "format_instructions":self.parser.get_format_instructions()
            })

        with open("classified_actions.json", "w") as file:
            json.dump(classsify, file, indent=4)
        

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

