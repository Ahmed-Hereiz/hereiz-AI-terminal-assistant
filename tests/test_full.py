from customAgents.agent_llm import SimpleStreamLLM
from customAgents.agent_prompt import PlaceHoldersPrompt
from customAgents.agent_tools import ToolKit, SearchTool
from customAgents.agent_runtime import SimpleRuntime
from customAgents.agent_routers import ToolExecRouter
from customAgents.agent_env import ReflectionEnv
from common.utils import load_config, parse_safety_settings

config = load_config(f"../config/llm.json")
safety_settings = parse_safety_settings(config['safety_settings'])


task_query = input("Enter your query : ")


##############################################################################################################################

plan_prompt_string = """
You are a planner agent your task to make a good plan for a task,
you help to get understand articles by instruncting other AI agents.
your task is to tell an AI model what to do based on the given query so that the AI model give the best result for the user.
you write the prompt for this AI and tell him what to explain to make the user easily read the article and understand it.
you also then tell the agent how to summarize the article.
Let's start.

the user query: {query}
AI:
"""

plan_llm = SimpleStreamLLM(api_key=config['api_key'],model="gemini-1.5-pro-001",safety_settings=safety_settings,temperature=0.7)
plan_prompt = PlaceHoldersPrompt(placeholders={"{query}":task_query},prompt_string=plan_prompt_string)
plan_tools = ToolKit(tools=[])
plan_agent = SimpleRuntime(llm=plan_llm,prompt=plan_prompt)
plan = plan_agent.loop()
print("="*100)

##############################################################################################################################

search_tool = SearchTool(description="tool used for search",tool_name="search_tool")
search_router = ToolExecRouter(tool=search_tool)
get_search = search_tool.execute_func(query="data science articles")


##############################################################################################################################

enhance_prompt_string = """
you are a helpfull AI assistand and your task is to provide usefull companion to person who is reading articles.
the user will give you two things the content and also instructions how to make him understand the content you have to read the instructions clearly

the instructions : 
{instructions}

content : 
{content}

AI :
"""

enhance_llm = SimpleStreamLLM(api_key=config['api_key'],model="gemini-1.5-pro-001",safety_settings=safety_settings,temperature=0.4)
enhance_prompt = PlaceHoldersPrompt(placeholders={"{instructions}":plan,"{content}":str(get_search)},prompt_string=enhance_prompt_string)
enhance_tools = ToolKit(tools=[])
enhance_agent = SimpleRuntime(llm=enhance_llm,prompt=enhance_prompt)
clarification = enhance_agent.loop()
print("="*100)

##############################################################################################################################

critic_prompt_string = """
You are a critic AI agent your task is to see other model generation and enhance it if needed.
the AI model will give you the task content and the description and it's generation and your task is to make it better for the user
who will read the content so you have to make better content and clarrifications to the user with examples and so on.

the instructions : 
{instructions}

content : 
{content}

model generation : 
{model_generation}

AI : 
"""

critic_llm = SimpleStreamLLM(api_key=config['api_key'],model="gemini-1.5-pro-001",safety_settings=safety_settings,temperature=0.8)
critic_prompt = PlaceHoldersPrompt(placeholders={"{instructions}":plan,"{content}":str(get_search),"{model_generation}":clarification},prompt_string=critic_prompt_string)
critic_tools = ToolKit(tools=[])
critic_agent = SimpleRuntime(llm=enhance_llm,prompt=enhance_prompt)
agent_output = critic_agent.loop()
print("="*100)


env = ReflectionEnv(agents=[enhance_agent,critic_agent])
env.run()