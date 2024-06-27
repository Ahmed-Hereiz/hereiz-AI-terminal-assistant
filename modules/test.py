from agent_llm import SimpleLLM, SimpleInvokeLLM, SimpleStreamLLM
from agent_prompt import SimplePrompt, PlaceHoldersPrompt
from agent_runtime import SimpleRuntime, BaseRuntime, HumanLoopRuntime
from agent_tools import ToolKit, SearchTool
from utils import add_root_to_path

root_path = add_root_to_path()
from common.utils import load_config, parse_safety_settings, load_template, load_memory_buffer


config = load_config(f"{root_path}/config/llm.json")
safety_settings = parse_safety_settings(config['safety_settings'])
prompt_string = load_template(f"{root_path}/templates/chat_template.txt")
memory_string = load_memory_buffer(f"{root_path}/data/history/memory/chat_memory_buffer")

simple_llm = SimpleStreamLLM(
    config['api_key'],
    config['model'],
    0.7,
    safety_settings
)


placeholders = {
        "{additional}":"### Instructions\n1. Output your response.\n2. Wait for human feedback.\n3. If feedback is given, revise your response based on the feedback and attempt the task again.",
        "{history}":memory_string,
        "{input}":"tell me 10 linux commands"
    }

loop_prompt = PlaceHoldersPrompt(prompt_string=prompt_string,placeholders=placeholders)
tool = SearchTool(description="search tool",tool_name="tool1")
toolkit = ToolKit(tools=[tool])
runtime = BaseRuntime(llm=simple_llm,prompt=loop_prompt,tools=toolkit)
runtime.loop()
