import warnings
from contextlib import contextmanager

from search_manage import SearchManager
from search_bot import SearchBot

with open('../templates/search_template.txt', 'r') as template_file:
    template = template_file.read()

@contextmanager
def suppress_warnings():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="The function `initialize_agent` was deprecated.*")
        warnings.filterwarnings("ignore", message="The method `Chain.run` was deprecated.*")
        yield

with suppress_warnings():
    manage_search = SearchManager(max_num_chars=2000,num_top_results=1)

    api_key = "AIzaSyCNO3Gwe7Hi32-DDo0yEhzElrTe6fNlOE4"

    search_bot = SearchBot(api_key=api_key,template=template,tool_function=manage_search.integrated_search_and_summarize)

    query = "top-cited artificial intelligence papers with high impact factor"

    print(search_bot.extract_keywords(query=query))

    print(search_bot.use_search_agent(query=query))

