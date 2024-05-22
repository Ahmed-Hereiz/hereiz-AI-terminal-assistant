import argparse
import json
from colorama import Fore
from langchain_google_genai import HarmBlockThreshold, HarmCategory

from Agents import Agent, Planner, Coder

with open('../config.json', 'r') as f:
    config = json.load(f)

with open('../templates/planner_agent.txt', 'r') as template_file:
    plan_template = template_file.read()

with open('../templates/coder_agent.txt', 'r') as template_file:
    code_template = template_file.read()

safety_settings = {
    HarmCategory[category]: HarmBlockThreshold[threshold]
    for category, threshold in config['safety_settings'].items()
}

plan_agent = Planner(config['api_key'],plan_template,config['model'],config['planner_agent_temperature'],safety_settings)
code_agent = Coder(config['api_key'],code_template,config['model'],config['coder_agent_temperature'],safety_settings)

user_input = """
write pytorch code to train a neural net on image dir named as Images, it's sub dir contains 2 dirs one named cats and one named dogs
train a cnn on this data where the task is to make dataloaders to load from Images/ dir then make a cnn class and make the training loop
then save the torch model.
"""

plan_agent.make_plan(user_input=user_input)

code_agent.write_code()
