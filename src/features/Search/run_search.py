from utils import get_arguments_search, add_root_to_path
root_dir = add_root_to_path()

from common.utils import load_config
from modules.search_agents import (
    SearchLLM,SearchPrompt,SearchAgent
)

def handle_search():

    config = load_config(f'{root_dir}/config/llm.json')

    args = get_arguments_search()
    if not args.search:
        print("Usage: hereiz --search 'your search query'")
        return
    
    search_llm = SearchLLM(api_key=config['api_key'],model=config['model'],temperature=0.7)
    search_prompt = SearchPrompt(question=args.search)
    search_agent = SearchAgent(llm=search_llm,prompt=search_prompt)
    search_agent.loop()