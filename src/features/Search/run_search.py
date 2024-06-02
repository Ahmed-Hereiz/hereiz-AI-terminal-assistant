from utils import get_arguments_search, add_root_to_path
hereiz_root = add_root_to_path()

from common.utils import load_config, load_template, parse_safety_settings
from modules.Agents.SearchAgent import (
    RedirectSearchAgent,
    RedirectSearchRuntime,
    RedirectSearchTools
)

def handle_search():
    json_root = f'{hereiz_root}/config/llm.json'
    template_root = f'{hereiz_root}/templates/search_template.txt'
    search_history = f'{hereiz_root}/data/history/search_history.txt'

    config = load_config(json_root)
    prompt = load_template(template_root)
    safety_settings = parse_safety_settings(config['safety_settings'])

    search_tools = RedirectSearchTools()
    
    parser = search_tools.parser
    agent = RedirectSearchAgent(config['api_key'],config['model'],config['search_model_temperature'],safety_settings,parser)

    runtime = RedirectSearchRuntime(
        agent=agent,
        search_manager=search_tools.tools[0],
        summarizer=search_tools.tools[1],
        prompt=prompt,
        parser=parser,
        history_file_path=search_history
    )

    args = get_arguments_search()
    if not args.search:
        print("Usage: hereiz --search 'your search query'")
        return
    
    runtime.agent_loop(query=args.search)