import argparse
import os
import json
from colorama import Fore
import sys
from langchain_google_genai import HarmBlockThreshold, HarmCategory

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from memory.manage_memory import MemoryManager
from chat import model_chat

with open('../config.json', 'r') as f:
    config = json.load(f)

with open('../templates/chat_template.txt', 'r') as template_file:
    template = template_file.read()

memory_manager = MemoryManager('../memory/memory_buffer')

safety_settings = {
    HarmCategory[category]: HarmBlockThreshold[threshold]
    for category, threshold in config['safety_settings'].items()
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Terminal Chatbot", allow_abbrev=False)
    parser.add_argument("--chat","-c", type=str, help="Your question to the model")
    args, unknown = parser.parse_known_args()
    
    
    if unknown:
        print(f"Ignoring unknown argument(s): {', '.join(unknown)}")

    if not args.chat:
        print("Usage: hereiz --chat 'your question'")
    else:
        buffer = memory_manager.load_memory()
        response, new_buffer = model_chat(config['api_key'], template, args.chat,buffer,
                                          config['model'], config['chat_model_temperature'],
                                          safety_settings)
        print(Fore.CYAN + "Hereiz:")
        print(Fore.CYAN + response + "\n")

        memory_manager.save_buffer(new_buffer)
    

