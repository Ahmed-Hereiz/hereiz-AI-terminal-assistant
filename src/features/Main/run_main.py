from colorama import Fore, Style
from utils import get_arguments, add_root_to_path

root_dir = add_root_to_path()
from common import MemoryManager, load_config
from modules.main_agents import MainLLM, MainPrompt, MainAgent
from modules.memory_agents import MemoryLLM, MemoryPrompt, MemoryAgent, MemoryReflectionEnv


def handle_main():
    config = load_config(f'{root_dir}/config/llm.json')

    manage_memory = MemoryManager(f'{root_dir}/data/history/memory/chat_memory_buffer.txt')
    memory = manage_memory.load_memory()

    args = get_arguments()
    if not args.main:
        print("Usage: hereiz --main 'your question'")
        return 
    
    main_llm = MainLLM(api_key=config['api_key'],model=config['model'],temperature=0.7)
    main_prompt = MainPrompt(question=args.main,memory=memory)
    main_agent = MainAgent(llm=main_llm,prompt=main_prompt)

    chat_summary_llm = MemoryLLM(api_key=config['api_key'],model=config['model'],temperature=0.5)
    chat_summary_prompt = MemoryPrompt(user_question=args.main,memory=memory)
    chat_summary_agent = MemoryAgent(llm=chat_summary_llm,prompt=chat_summary_prompt)
    
    chat_env = MemoryReflectionEnv(agents=[main_agent,chat_summary_agent])
    chat_response, new_memory = chat_env.run()

    manage_memory.save_buffer(new_memory)

    print(Fore.CYAN + chat_response + Style.RESET_ALL)