from agent_llm import SimpleLLM, SimpleInvokeLLM, SimpleStreamLLM
from agent_prompt import SimplePrompt, PlaceHoldersPrompt, ReActPrompt
from agent_runtime import SimpleRuntime, BaseRuntime, HumanLoopRuntime, ReActRuntime
from agent_tools import ToolKit, SearchTool, LinkedinProfileScrapeTool, PythonRuntimeTool
#from agent_env import ReflectionEnv, SequentialEnv
from utils import add_root_to_path

root_path = add_root_to_path()
from common.utils import load_config, parse_safety_settings, load_template, load_memory_buffer


config = load_config(f"{root_path}/config/llm.json")
safety_settings = parse_safety_settings(config['safety_settings'])
prompt_string = load_template(f"{root_path}/templates/chat_template.txt")
memory_string = load_memory_buffer(f"{root_path}/data/history/memory/chat_memory_buffer")


prompt1 = """
you are a code agent and your task is to :
Write a python code to train a nn using pytorch for image classification task of dogs and cats images
you have 2 dirs one named as dogs and other named as cats begin from the beginning and write the full code that can load this data, with data loaders then write the model class

"""
prompt2 = """
you are a critic agent your task is to see the user query to an AI llm and see how this AI llm responded and tell the ai model if there something he may do to make the code better.
Don't write any code or make better version of the code just give 3 to 5 line of concise comments about how to make the code better or if something to change or no (don't write any code )
You have to get a carefull look at the other agent code and make sure it doesn't hullicinate.
and if the code is fine you just output : 0


user : {prompt1}
AI model : 
"""


simple_llm = SimpleStreamLLM(
    config['api_key'],
    config['model'],
    0.7,
    safety_settings
)

critic_llm = SimpleStreamLLM(
    config['api_key'],
    config['model'],
    0.7,
    safety_settings
)

agent1_prompt = SimplePrompt(prompt_string=prompt1)
agent2_prompt = PlaceHoldersPrompt(prompt_string=prompt2,placeholders={"{prompt1}":prompt1})


agent1 = SimpleRuntime(llm=simple_llm,prompt=agent1_prompt)
agent2 = HumanLoopRuntime(llm=critic_llm,prompt=agent2_prompt)

# agent_env = ReflectionEnv(agents=[agent1,agent2])
# agent_env.run(num_max_iters=5)


      
