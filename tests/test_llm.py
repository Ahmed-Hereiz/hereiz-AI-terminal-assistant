from utils import add_root_to_path
root_path = add_root_to_path()

from modules.agent_llm import SimpleInvokeLLM, SimpleStreamLLM
from common.utils import load_config, parse_safety_settings, load_template, load_memory_buffer

config = load_config(f"{root_path}/config/llm.json")
safety_settings = parse_safety_settings(config['safety_settings'])

invoke_llm = SimpleInvokeLLM(api_key=config['api_key'],model=config['model'],temperature=0.7)
response = invoke_llm.llm_generate(input="tell me 10 linux commands ")
print(response)
print("="*100)

invoke_llm = SimpleStreamLLM(api_key=config['api_key'],model=config['model'],temperature=0.7)
response = invoke_llm.llm_generate(input="tell me 10 linux commands ")
print("\n")