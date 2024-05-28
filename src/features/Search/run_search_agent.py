import json
import warnings
import argparse
from contextlib import contextmanager
from colorama import Fore

from search_manage import SearchManager
from search_bot import SearchBot
from langchain_google_genai import HarmBlockThreshold, HarmCategory

with open('../templates/search_template.txt', 'r') as template_file:
    template = template_file.read()

with open('../config.json', 'r') as f:
    config = json.load(f)

safety_settings = {
    HarmCategory[category]: HarmBlockThreshold[threshold]
    for category, threshold in config['safety_settings'].items()
}



@contextmanager
def suppress_warnings():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="The function `initialize_agent` was deprecated.*")
        warnings.filterwarnings("ignore", message="The method `Chain.run` was deprecated.*")
        yield


def search_answer(query):

    manage_search = SearchManager(
        max_num_chars=config['max_num_chars_search_agent'],
        num_top_results=config['num_top_results_search_agent']
        )

    search_bot = SearchBot(config['api_key'],template,manage_search.integrated_search_and_summarize,
                           config['model'],config['search_agent_temperature'],
                           safety_settings)

    return search_bot.use_search_agent(query=query)

with suppress_warnings():
    
    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Terminal Search agent", allow_abbrev=True)
        parser.add_argument("--search", "-s", type=str, help="Your query to search for with AI")
        args, unknown = parser.parse_known_args()

        if unknown:
            print(f"Ignoring unknown argument(s): {', '.join(unknown)}")

        if not args.search:
            print("Usage: hereiz --search 'your question'")

        else:
            print(Fore.CYAN + "Hereiz:")
            answer = search_answer(query=args.search)
            print(Fore.CYAN + answer)