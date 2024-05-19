import argparse
import os
from colorama import Fore

from memory.manage_memory import MemoryManager
from ask.ask import model_ask

os.environ['API_KEY'] = "AIzaSyCNO3Gwe7Hi32-DDo0yEhzElrTe6fNlOE4"

with open('templates/template.txt', 'r') as template_file:
    template = template_file.read()

memory_manager = MemoryManager('memory/memory_buffer')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Terminal Chatbot", allow_abbrev=False)
    parser.add_argument("--ask", type=str, help="Your question to the model")
    args, unknown = parser.parse_known_args()
    
    
    if unknown:
        print(f"Ignoring unknown argument(s): {', '.join(unknown)}")

    if not args.ask:
        print("Usage: hereiz --ask 'your question'")
    else:
        buffer = memory_manager.load_memory()
        response, new_buffer = model_ask(os.getenv('API_KEY'), template, args.ask, buffer)
        print(Fore.CYAN + "Hereiz:")
        print(Fore.CYAN + response + "\n")

        memory_manager.save_buffer(new_buffer)
    

