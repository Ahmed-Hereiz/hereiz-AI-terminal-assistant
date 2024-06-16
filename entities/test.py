from langchain_core.output_parsers import StrOutputParser
from utils import add_root_to_path
root = add_root_to_path()

from common.utils import load_config, parse_safety_settings
from base_agent import BaseAgent
from base_tools import BaseTool

# config = load_config(f"{root}/config/llm.json")
# safety_settings = parse_safety_settings(config['safety_settings'])

# agent = BaseAgent(config['api_key'],config['model'],0.7,safety_settings,initialize_verbose=True)

# print(agent)

# prompt = """tell me 10 linux commands """

# print(agent.parser)

def tool1(x):
    """returns 0 function"""
    x = 0
    return x

def tool2(x):
    """returns x squared"""
    x = x**2
    return x

tools = {"tool1":tool1,"tool2":tool2}
tool = BaseTool(tools)

print(tool.format_tool_instructions())

print(tool.execute_func("tool2",10))