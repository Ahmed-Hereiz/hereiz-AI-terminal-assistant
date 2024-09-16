import os
from utils import get_arguments_fullsearch, add_root_to_path
from customAgents.agent_llm import SimpleStreamLLM, SimpleInvokeLLM
from customAgents.agent_prompt import SimplePrompt, PlaceHoldersPrompt, ReActPrompt
from customAgents.agent_tools import SearchTool
from customAgents.agent_routers import ToolExecRouter
from customAgents.agent_runtime import SimpleRuntime, ReActRuntime
from customAgents.agent_env import SequentialEnv

root_dir = add_root_to_path()
from common.utils import load_config


query_prompt_string = """
You are a Search Assistant LLM. Your task is to reformulate the user's query into a **concise, focused search query**. Your output must be a single short sentence optimized for generating the most effective search results.

Instructions:
- Reformulate the query to be relevant, precise, and optimized for search engines.
- Eliminate any unnecessary words, phrases, or extraneous details.
- Ignore any instructions related to how the user wants results summarized. Your only job is to produce the best search query.
- Do not provide any explanations. Only output the refined search query.

Reminder: Your task is solely to generate **better search queries**, not to summarize results.

Example:
User Query: I want to learn Python while I am a beginner and have no experience in it.
Output: Best online courses or tutorials for learning Python

User Query: I want to learn machine learning, tell me the most important 5 points here that include some sort of roadmap what to do?
Output: machine learning roadmap

User Query: 
"""


# summarize_prompt_string = """
# You are a Summarization Assistant LLM. Your task is to help the user find relevant information from a large, unstructured text based on their specific query. You must analyze the provided text, locate the parts that are most relevant to the user's query, and then summarize the content in a clear and concise manner.

# Instructions:
# - Focus only on information from the text that directly answers or relates to the user's query.
# - Summarize the key points or details from the relevant sections of the text.
# - Make sure your summary is clear, informative, and directly addresses the user's needs.
# - Exclude irrelevant details that do not pertain to the user's query.
# - Avoid unnecessary elaboration and stick to the important points based on the user's request.
# - If the text don't contain the answer the answer to user, say to him that the text don't contain the content.

# Your task is to provide a well-organized and concise summary that extracts the most important information from the text based on the user's query.

# Inputs:
# 1. User's Query:
# {user_query}
# 2. Text to Analyze:
# """

summarize_prompt_string = """
You are a Summarization Assistant LLM. Your task is to help the user find relevant information from a large, unstructured text based on their specific query. You must analyze the provided text, locate the parts that are most relevant to the user's query, and then summarize the content in a clear and concise manner.

Instructions:
- Focus only on information from the text that directly answers or relates to the user's query.
- Summarize the key points or details from the relevant sections of the text.
- Make sure your summary is clear, informative, and directly addresses the user's needs.
- Exclude irrelevant details that do not pertain to the user's query.
- Avoid unnecessary elaboration and stick to the important points based on the user's request.
- If the text don't contain the answer the answer to user, say to him that the text don't contain the content.

Your task is to provide a well-organized and concise summary that extracts the most important information from the text based on the user's query.

Inputs:
1. User's Query
2. Text to Analyze
"""

def handle_fullsearch():

    config = load_config(f'{root_dir}/config/llm.json')

    args = get_arguments_fullsearch()
    if not args.fullsearch:
        print("Usage: hereiz --fullsearch 'your search query'")
        return
    

    search_tool = SearchTool(num_top_results=5,save_last_search_links_path="tmp.txt")
    tool_exec = ToolExecRouter(tool=search_tool,exec_after=0)
    
    query_llm = SimpleInvokeLLM(api_key=config['api_key'],model=config['model'],temperature=0.7)
    query_prompt = SimplePrompt(prompt_string=query_prompt_string)
    query_agent = SimpleRuntime(llm=query_llm,prompt=query_prompt)
    
    # summary_llm = SimpleStreamLLM(api_key=config['api_key'],model=config['model'],temperature=0.7)
    # summary_prompt = PlaceHoldersPrompt(placeholders={"{user_query}":args.fullsearch},prompt_string=summarize_prompt_string)
    # summary_agent = SimpleRuntime(llm=summary_llm,prompt=summary_prompt)

    summary_llm = SimpleStreamLLM(api_key=config['api_key'],model=config['model'],temperature=0.7)
    summary_prompt = ReActPrompt(question=args.fullsearch,prompt_string=args.fullsearch)
    summary_agent = ReActRuntime(llm=summary_llm,prompt=summary_prompt,toolkit=[])

    env = SequentialEnv(env_items=[query_agent,tool_exec,summary_agent])
    env.run(initial_input=args.fullsearch)

    with open('tmp.txt','r') as f:
        source_links = f.read()

    os.remove('tmp.txt')

    return source_links


