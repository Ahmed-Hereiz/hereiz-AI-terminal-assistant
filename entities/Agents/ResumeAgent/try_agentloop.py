from utils import add_root_to_path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
hereiz_root = add_root_to_path()

from common.utils import load_config, parse_safety_settings
from helpers import extract_json_from_string

config = load_config(f'{hereiz_root}/config/llm.json')
safety_settings = parse_safety_settings(config['safety_settings'])

llm = ChatGoogleGenerativeAI(
    google_api_key=config['api_key'],
    model=config['model'],
    temperature=0.7,
    safety_settings=safety_settings
)


def get_response_time(url):
    if url == "learnwithhereiz.com":
        return 0.5
    if url == "google.com":
        return 0.3
    if url == "openai.com":
        return 0.4


prompt = """
You run in a loop of Thought, Action, PAUSE, Action_Response.
At the end of the loop you output an Answer.
Use Thought to understand the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Action_Response will be the result of running those actions.
Your available actions are:
get_response_time:
e.g. get_response_time: learnwithhereiz.com
Returns the response time of a website
Example session:
Question: what is the response time for learnwithhereiz.com?
Thought: I should check the response time for the web page first.
Action: 
{
  "function_name": "get_response_time",
  "function_parms": {
    "url": "learnwithhereiz.com"
  }
}
PAUSE
You will be called again with this:
Action_Response: 0.5
You then output:
Answer: The response time for learnwithhereiz.com is 0.5 seconds.

Question: 
"""


available_actions = {
    "get_response_time": get_response_time
}


query = "what is the response time for google.com?"
query += "\n"

prompt += query


for step in range(4):
    print(f"step : {step}")
    print("-"*100)

    llm_response = llm.predict(prompt)
    print(llm_response)
    prompt += f"\n{llm_response}"
    extracted_json = extract_json_from_string(llm_response)

    if len(extracted_json) > 0:
        function_name = extracted_json[0]['function_name']
        function_parms = extracted_json[0]['function_parms']
        if function_name not in available_actions:
            raise Exception(f"Unknown action: {function_name}")
        
        print(f" -- running {function_name} {function_parms}")
        action_function = available_actions[function_name]
        result = f"\nAction_Response: {action_function(*function_parms.values())}"
        prompt += result
    else:
        break
