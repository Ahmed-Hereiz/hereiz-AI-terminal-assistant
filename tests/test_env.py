from customAgents.agent_llm import SimpleStreamLLM
from customAgents.agent_prompt import SimplePrompt
from customAgents.agent_routers import ToolExecRouter
from customAgents.agent_tools import SearchTool
from customAgents.agent_runtime import SimpleRuntime
from customAgents.agent_env import SequentialEnv


from common.utils import load_config, parse_safety_settings
config = load_config(f"../config/llm.json")
safety_settings = parse_safety_settings(config['safety_settings'])


query_prompt_string = """
You are search Assistant llm, your task is to help user where you reformat his query, you have to ouput only one sentence to the user.
so that your sentence will go for other code that will execute this directly.
NOTE THAT YOU JUST OUTPUT THE SINGLE SHORT QUERY THAT WILL MAKE BETTER SEARCH WITHOUT ANY FURTHER EXPLAINATION

example :  
user_query : I want to learn python while iam beginner and I have no experience in it.
output : Best online courses or tutorials for learning Python

user_query :
"""

summarize_prompt_string = """
You are search Assistant llm, your task is to help user where you summarize some text that comes from web and you summarize it in the form of only ten points.
and you explain every point so the user understand everything.

text_data :
"""

query = input("Enter your query : ")
query_llm = SimpleStreamLLM(api_key=config['api_key'],model='gemini-1.5-flash',temperature=0.7,safety_settings=safety_settings)
query_prompt = SimplePrompt(prompt_string=query_prompt_string)
query_agent = SimpleRuntime(llm=query_llm,prompt=query_prompt)
# output_query = query_agent.loop()

search_tool = SearchTool()
tool_exec = ToolExecRouter(tool=search_tool)
# text_output = tool_exec.exec_router(output_query)

summary_llm = SimpleStreamLLM(api_key=config['api_key'],model='gemini-1.5-flash',temperature=0.7,safety_settings=safety_settings)
summary_prompt = SimplePrompt(prompt_string=summarize_prompt_string)
summary_agent = SimpleRuntime(llm=summary_llm,prompt=summary_prompt)
#final_summary = summary_agent.loop()

print(">"*100)
print("Equivlent with the env : \n\n")
env = SequentialEnv(env_items=[query_agent,tool_exec,summary_agent])
print(env.run(initial_input=query))