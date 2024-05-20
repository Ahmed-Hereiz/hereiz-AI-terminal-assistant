import argparse
import os
import json
from colorama import Fore
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ask import model_ask

with open('../config.json', 'r') as f:
    config = json.load(f)

with open('../templates/chat_template.txt', 'r') as template_file:
    template = template_file.read()

os.environ['API_KEY'] = config['api_key']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Terminal Chatbot", allow_abbrev=False)
    parser.add_argument("--ask","-a", type=str, help="Your question to the model")
    args, unknown = parser.parse_known_args()
    
    
    if unknown:
        print(f"Ignoring unknown argument(s): {', '.join(unknown)}")

    if not args.ask:
        print("Usage: hereiz --ask 'your question'")
    else:
        response = model_ask(os.getenv('API_KEY'), template, args.ask)
        print(Fore.CYAN + "Hereiz:")
        print(Fore.CYAN + response + "\n")

    

