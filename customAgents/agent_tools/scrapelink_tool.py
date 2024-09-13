import requests
from bs4 import BeautifulSoup # type: ignore
from typing import Any
from customAgents.agent_tools import BaseTool


class ScrapeLinkTool(BaseTool):
    def __init__(self, description: str, tool_name: str = None, max_num_chars: int = 5000):

        self.max_num_chars = max_num_chars

        super().__init__(description, tool_name)


    def execute_func(self, url: str) -> Any:

        headers = {
          "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
           }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all('p')
        content = " ".join([para.get_text() for para in paragraphs])

        return content[:self.max_num_chars]