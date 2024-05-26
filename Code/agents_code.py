import argparse
import json
from colorama import Fore
from langchain_google_genai import HarmBlockThreshold, HarmCategory
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

from Agents import Planner, Coder, FileRunner
from Parsers import ParseOutFileRunner


with open('../config.json', 'r') as f:
    config = json.load(f)

with open('../templates/planner_agent.txt', 'r') as template_file:
    plan_template = template_file.read()

with open('../templates/coder_agent.txt', 'r') as template_file:
    code_template = template_file.read()

with open('../templates/filerunner_agent.txt', 'r') as template_file:
    filerunner_template = template_file.read()

safety_settings = {
    HarmCategory[category]: HarmBlockThreshold[threshold]
    for category, threshold in config['safety_settings'].items()
}



parser = JsonOutputParser(pydantic_object=ParseOutFileRunner)

planner_template = PromptTemplate(input_variables=["input"], template=plan_template)
coder_template = PromptTemplate(input_variables=["input"], template=code_template)
filerunner_template = PromptTemplate(input_variables=["input"],
                                     template=filerunner_template,
                                     partial_variables={"format_instructions":parser.get_format_instructions()}
                                     )

plan_agent = Planner(config['api_key'],config['model'],config['planner_agent_temperature'],safety_settings,planner_template,StrOutputParser())
code_agent = Coder(config['api_key'],config['model'],config['coder_agent_temperature'],safety_settings,coder_template,StrOutputParser())
runner_agent = FileRunner(config['api_key'],config['model'],config['coder_agent_temperature'],safety_settings,filerunner_template,parser)

user_input = """
write pytorch code to train a neural net on image dir named as Images, it's sub dir contains 2 dirs one named cats and one named dogs
train a cnn on this data where the task is to make dataloaders to load from Images/ dir then make a cnn class and make the training loop
then save the torch model.
"""

plan_agent.make_plan(user_input=user_input)

code = code_agent.write_code()

runner_agent.run_file()

