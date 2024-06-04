from utils import add_root_to_path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
hereiz_root = add_root_to_path()

from common.utils import load_config, parse_safety_settings

config = load_config(f'{hereiz_root}/config/llm.json')
safety_settings = parse_safety_settings(config['safety_settings'])

llm = ChatGoogleGenerativeAI(
    google_api_key=config['api_key'],
    model=config['model'],
    temperature=0.7,
    safety_settings=safety_settings
)


def generate_prompt(task_description, input_data, feedback=None):
    prompt = f"""
### Task Description
You are an AI language model. Your task is to {task_description}.

### Input
{input_data}

### Instructions
1. Attempt the task based on the input provided.
2. Output your response.
3. Wait for human feedback.
4. If feedback is given, revise your response based on the feedback and attempt the task again.

"""
    if feedback:
        prompt += f"### Feedback\n{feedback}\n"
        
    prompt += "### Current Input\n" + input_data
    return prompt

def llm_generate(task_description, input_data, feedback=None):
    prompt = generate_prompt(task_description, input_data, feedback)
    print(prompt)
    llm_response = llm.predict(prompt)
    return llm_response

def human_in_the_loop(task_description, initial_input):
    input_data = initial_input
    feedback = None
    loop_active = True
    iteration = 0
    
    while loop_active:
        llm_response = llm_generate(task_description, input_data, feedback)
        
        print("LLM Response:", llm_response)
        
        human_feedback = input("Enter feedback (or 'exit' to end loop): ")
        
        if human_feedback.lower() == 'exit':
            loop_active = False
        else:
            feedback = human_feedback
        
        iteration += 1
        print(f"Iteration {iteration} completed.")
    
    print("Loop terminated.")


task_description = "translate the following text to French"
initial_input = "Translate the following text to French: 'Hello, world!'"
human_in_the_loop(task_description, initial_input)

