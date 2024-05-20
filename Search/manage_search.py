import requests
from bs4 import BeautifulSoup

class SearchManager:
    def __init__(self, max_num_chars=2000, num_top_results=3):
        self.max_num_chars = max_num_chars
        self.num_top_results = num_top_results

    def make_search(self, query):
        url = f"https://duckduckgo.com/html/?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"}
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
    
    def integrated_search_and_summarize(self, query):
        search_results = self.make_search(query)
        summarized_results = []
        
        for result in search_results[:self.num_top_results]:  
            content = self.fetch_content_from_url(result["link"])
            summarized_results.append({"title": result["title"], "link": result["link"], "content": content})
        
        return summarized_results
    
    def fetch_content_from_url(self, url):
        headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        paragraphs = soup.find_all('p')
        content = " ".join([para.get_text() for para in paragraphs])
        return content[:self.max_num_chars]
