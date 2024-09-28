from utils import get_arguments, add_root_to_path

root_dir = add_root_to_path()
from common import MemoryManager, load_config
from modules.chat_agents import ChatLLM, ChatPrompt, ChatAgent
from modules.memory_agents import MemoryLLM, MemoryPrompt, MemoryAgent, MemoryReflectionEnv

def hande_chat():
    config = load_config(f'{root_dir}/config/llm.json')

    manage_memory = MemoryManager(f'{root_dir}/data/history/memory/chat_memory_buffer.txt')
    memory = manage_memory.load_memory()
    
    args = get_arguments()
    if not args.chat:
        print("Usage: hereiz --chat 'your question'")
        return 
    
    chat_llm = ChatLLM(api_key=config['api_key'],model=config['model'],temperature=0.7)
    chat_prompt = ChatPrompt(user_question=args.chat,memory=memory,prompt_string="")
    chat_agent = ChatAgent(llm=chat_llm,prompt=chat_prompt)

    chat_summary_llm = MemoryLLM(api_key=config['api_key'],model=config['model'],temperature=0.5)
    chat_summary_prompt = MemoryPrompt(user_question=args.chat,memory=memory)
    chat_summary_agent = MemoryAgent(llm=chat_summary_llm,prompt=chat_summary_prompt)

    
    chat_env = MemoryReflectionEnv(agents=[chat_agent,chat_summary_agent])
    _, new_memory = chat_env.run()

    manage_memory.save_buffer(new_memory)
