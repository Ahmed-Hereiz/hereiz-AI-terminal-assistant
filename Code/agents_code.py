import argparse
import json
from colorama import Fore
from langchain_google_genai import HarmBlockThreshold, HarmCategory

from Agents import Agent

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

plan_agent = Agent(config['api_key'],plan_template,config['model'],config['planner_agent_temperature'],safety_settings)
code_agent = Agent(config['api_key'],code_template,config['model'],config['coder_agent_temperature'],safety_settings)

user_input = "I have a images dir where inside it I have a dir named as dogs and one named as cats, I want you make full torch code to load this data from dir using dataloader then make the images shape 224,224 then make a cnn model on this data and fit the model "

print(f"the code the user needs is : {user_input}")
plan = plan_agent.make_plan(user_input=user_input)
print(plan)

print("now the coder model : ")
print("-"*100)
code = code_agent.make_code(planner_input=plan)
print(code)