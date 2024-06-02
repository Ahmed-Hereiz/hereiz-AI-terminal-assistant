from utils import get_arguments_searchopen, add_root_to_path
hereiz_root = add_root_to_path()

from common.utils import load_config, load_template, parse_safety_settings
from modules.Agents.SearchAgent import (
    RedirectSearchAgent,
    RedirectedLinksRuntime,
    RedirectSearchTools
)


def handle_searchopen():
    json_root = f'{hereiz_root}/config/llm.json'
    template_root = f'{hereiz_root}/templates/search_template.txt'
    tmp_link_path = f'{hereiz_root}/data/tmp/tmp_link'

    config = load_config(json_root)
    prompt = load_template(template_root)
    safety_settings = parse_safety_settings(config['safety_settings'])

    search_tools = RedirectSearchTools()    
    parser = search_tools.parser
    agent = RedirectSearchAgent(config['api_key'],config['model'],config['search_model_temperature'],safety_settings,parser)
    
    runtime = RedirectedLinksRuntime(
        agent=agent,
        search_manager=search_tools.tools[0],
        prompt=prompt,
        parser=parser
    )

    args = get_arguments_searchopen()
    if not args.searchopen:
        print("Usage: hereiz --searchopen 'your search query'")
        return
    
    browse_link = runtime.agent_loop(query=args.searchopen)
    with open(tmp_link_path, 'w') as file:
        file.write(browse_link)
