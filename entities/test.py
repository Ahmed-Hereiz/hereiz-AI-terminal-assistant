from langchain_core.output_parsers import StrOutputParser
from utils import add_root_to_path
root = add_root_to_path()

from common.utils import load_config, parse_safety_settings
from base import BaseAgent


config = load_config(f"{root}/config/llm.json")
safety_settings = parse_safety_settings(config['safety_settings'])

agent = BaseAgent(config['api_key'],config['model'],0.7,safety_settings,initialize_verbose=True)

print(agent)

prompt = """tell me 10 linux commands """

print(agent.parser)