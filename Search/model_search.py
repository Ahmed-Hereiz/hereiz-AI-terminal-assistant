import json
import argparse
from search_manage import SearchManager
from search_bot import SearchBot
from colorama import Fore
from langchain_google_genai import HarmBlockThreshold, HarmCategory

with open('../templates/search_template.txt', 'r') as template_file:
    template = template_file.read()

with open('../config.json', 'r') as f:
    config = json.load(f)

safety_settings = {
    HarmCategory[category]: HarmBlockThreshold[threshold]
    for category, threshold in config['safety_settings'].items()
}



def get_links(query):
    query = model_search.extract_keywords(query=query)[1:-1]
    print(Fore.CYAN + f"""Reforming your query from "{args.searchopen}" to "{query}" for better results""")
    response = manage_search.make_search(query=query)

    print("Some results found : \n\n")
    for index, dictionary in enumerate(response):
        print(Fore.WHITE + dictionary['title'] + " : " + Fore.LIGHTBLUE_EX + dictionary['link'] + Fore.WHITE)
        if index == 0:
            browse_link = dictionary['link']

    return browse_link

if __name__ == "__main__":

    manage_search = SearchManager()
    model_search = SearchBot(config['api_key'],template,manage_search.integrated_search_and_summarize,
                            config['model'],config['search_model_temperature'],safety_settings)
    
    parser = argparse.ArgumentParser(description="Terminal Search Model", allow_abbrev=True)
    parser.add_argument("--searchopen", "-so", type=str, help="Your query to search for with AI")
    args, unknown = parser.parse_known_args()

    if unknown:
        print(f"Ignoring unknown argument(s): {', '.join(unknown)}")

    if not args.searchopen:
        print("Usage: hereiz --searchopen 'your question'")

    else:
        print(Fore.CYAN + "Hereiz:")
        links = get_links(query=args.searchopen)

        with open('tmp_link', 'w') as f:
            f.write(links)

        print(Fore.CYAN + "\nOpening the top link on chrome...\n")
