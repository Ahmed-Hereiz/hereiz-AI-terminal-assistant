from utils import get_arguments, add_root_to_path

root_dir = add_root_to_path()
from common import load_config
from modules.generate_agents import GenerativeAILLM, GenerativeAIPrompt, GenerativeAIAgent


def handle_generate():
    config = load_config(f'{root_dir}/config/llm.json')
    
    args = get_arguments()
    if not args.generate:
        print("Usage: hereiz --generate 'your query'")
        return
    
    generate_llm = GenerativeAILLM(api_key=config['api_key'],model=config['model'],temperature=0.7)
    generate_prompt = GenerativeAIPrompt(question=args.generate)
    generate_agent = GenerativeAIAgent(llm=generate_llm,prompt=generate_prompt)

    generate_agent.loop(verbose_tools=True)