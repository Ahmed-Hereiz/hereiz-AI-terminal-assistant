from utils import add_root_to_path
hereiz_root = add_root_to_path()

import requests
from bs4 import BeautifulSoup # type: ignore
from typing import List, Dict
from modules.Tools.ModelToolBase import ToolBase

class SearchManager(ToolBase):
    def __init__(self, max_num_chars: int = 2000, num_top_results: int = 3):
        """
        Initializes the SearchManager with specified maximum number of characters for content
        and number of top search results to consider.

        :param max_num_chars: The maximum number of characters to fetch from a URL.
        :param num_top_results: The number of top search results to consider.
        """
        super().__init__()
        self.max_num_chars = max_num_chars
        self.num_top_results = num_top_results


    def make_search(self, query: str) -> List[Dict[str, str]]:
        """
        Performs a search using DuckDuckGo and returns the search results.

        :param query: The search query.
        :return: A list of search results with titles and links.
        """

        url = f"https://duckduckgo.com/html/?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
            }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        for result in soup.find_all("a", {"class": "result__a"}):
            title = result.get_text()
            link = result['href']
            if link.startswith('/'):
                link = 'https://duckduckgo.com' + link
            results.append({"title": title, "link": link})
            
        return results
    
    
    def fetch_content_from_url(self, url: str) -> str:
        """
        Fetches content from a URL.

        :param url: The URL to fetch content from.
        :return: A string containing the content fetched from the URL.
        """

        headers = {
          "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
           }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        paragraphs = soup.find_all('p')
        content = " ".join([para.get_text() for para in paragraphs])
        return content[:self.max_num_chars]


    def integrated_search(self, query):
        """
        Performs an integrated search: searches for the query, fetches content from the top results,
        and returns a summary of the results.

        :param query: The search query.
        :return: A list of dictionaries containing the title, link, and content of the top search results.
        """

        search_results = self.make_search(query)
        summarized_results = []
        
        for result in search_results[:self.num_top_results]:  
            content = self.fetch_content_from_url(result["link"])
            summarized_results.append({"title": result["title"], "link": result["link"], "content": content})
        
        return summarized_results
    
