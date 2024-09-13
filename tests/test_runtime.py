from customAgents.agent_runtime import HumanLoopRuntime, ChooseToolRuntime
from customAgents.agent_llm import SimpleStreamLLM
from customAgents.agent_prompt import SimplePrompt, ChooseToolsPrompt
from common.utils import load_config, parse_safety_settings

from utils import add_root_to_path
root_path = add_root_to_path()

print(root_path)
config = load_config(f"{root_path}/config/llm.json")
safety_settings = parse_safety_settings(config['safety_settings'])


stream_llm = SimpleStreamLLM(api_key=config['api_key'],model=config['model'],temperature=0.7)
prompt = SimplePrompt("tell me 10 linux commands ")
agent = HumanLoopRuntime(llm=stream_llm,prompt=prompt)

agent.loop()
