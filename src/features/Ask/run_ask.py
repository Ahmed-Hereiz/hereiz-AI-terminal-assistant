from utils import get_arguments, add_root_to_path

root_dir = add_root_to_path()
from common import load_config
from modules.ask_agents import AskLLM, AskPrompt, AskAgent

def handle_ask():
    config = load_config(f'{root_dir}/config/llm.json')

    args = get_arguments()
    if not args.ask:
        print("Usage: hereiz --ask 'your question' --human-feedback 'bool for feedback' ")
        return

    llm = AskLLM(api_key=config['api_key'],model=config['model'],temperature=0.7)
    prompt = AskPrompt(user_question=args.ask,prompt_string="")
    ask_agent = AskAgent(llm=llm,prompt=prompt)
    ask_agent.loop(activate_loop=args.human_feedback)
    
