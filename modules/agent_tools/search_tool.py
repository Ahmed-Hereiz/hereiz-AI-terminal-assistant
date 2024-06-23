import requests
from bs4 import BeautifulSoup # type: ignore
from typing import Any
from agent_tools import ScrapeLinkTool


class SearchTool(ScrapeLinkTool):
    def __init__(self, description: str, tool_name: str = None, max_num_chars: int = 5000, num_top_results: int = 3):
        
        self.num_top_results = num_top_results
        
        super().__init__(description, tool_name, max_num_chars)


    def execute_func(self, query: str) -> str:
        
        search_results = self._make_search(query=query)
        summarized_results = []
        
        for result in search_results[:self.num_top_results]:  
            content = self._fetch_url_content(url=result["link"])
            summarized_results.append({"title": result["title"], "link": result["link"], "content": content})
        
        return summarized_results


    def _fetch_url_content(self, url: str) -> Any:
        return super().execute_func(url)
    

    def _make_search(self, query: str) -> Any:

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