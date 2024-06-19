from langchain_core.output_parsers import StrOutputParser
from utils import add_root_to_path
root = add_root_to_path()

from common.utils import load_config, parse_safety_settings
from base_llm import BaseLLM
from base_tools import BaseTool
from base_prompt import BasePrompt
from base_runtime import BaseRuntime

config = load_config(f"{root}/config/llm.json")
safety_settings = parse_safety_settings(config['safety_settings'])

llm = BaseLLM(config['api_key'],config['model'],0.7,safety_settings,initialize_verbose=True)
tools = BaseTool({})
prompt = BasePrompt(prompt_string="tell me 10 linux commands")
agent = BaseRuntime(llm=llm,prompt=prompt,tools=tools)

r = agent.loop(n_steps=3)

# prompt = """tell me 20 linux commands """

# print(llm.llm_generate(input=prompt))
# print(llm.parser)

# def tool1(x):
#     """returns 0 function"""
#     x = 0
#     return x

# def tool2(x):
#     """returns x squared"""
#     x = x**2
#     return x

# tools = {"tool1":tool1,"tool2":tool2}
# tool = BaseTool(tools)

# print(tool.format_tool_instructions())

# print(tool.execute_func("tool2",10))

# prompt1 = BasePrompt(template_file='../templates/ask_template.txt',prompt_string="this is ahmed")
# prompt2 = BasePrompt(template_file=None,prompt_string="wow let's add to prompts")

# print(prompt1+prompt2)

