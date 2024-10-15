import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup # type: ignore
from typing import Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from customAgents.agent_tools import BaseTool


class ScrapeLinkTool(BaseTool):
    def __init__(
            self,
            description: str,
            tool_name: str = None,
            max_num_chars: int = 5000
        ):

        self.max_num_chars = max_num_chars
        self.description = description
        self.tool_names = tool_name
        self.max_num_chars = max_num_chars
        self.headers = {
          "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
           }

        super().__init__(description, tool_name)


    def execute_func(self, url: str) -> str:

        return requests.get(url, headers=self.headers)
    

class ScrapeStaticLinkTool(ScrapeLinkTool):
    def __init__(self, description: str, tool_name: str = None, max_num_chars: int = 5000):
        super().__init__(description, tool_name, max_num_chars)

    def execute_func(self, url: str) -> str:
        
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all('p')
        content = " ".join([para.get_text() for para in paragraphs])

        return content[:self.max_num_chars]
    

class ScrapeDynamicLinkTool(ScrapeLinkTool):
    def __init__(self, description: str, service: str="/usr/bin/chromedriver", tool_name: str = None, max_num_chars: int = 5000):
        self.service = service
        super().__init__(description, tool_name, max_num_chars)

    def execute_func(self, url: str) -> str:

        service = Service(self.service)
        driver = webdriver.Chrome(service=service)

        driver.get(url)
        time.sleep(5)  
        page_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page_source, 'html.parser')
        tags_to_extract = ['p', 'h1', 'h2', 'h3', 'li', 'div']
        elements = soup.find_all(tags_to_extract)

        markdown_content = []

        for element in elements:
            if element.name == 'h1':
                markdown_content.append(f"# {element.get_text()}\n")
            elif element.name == 'h2':
                markdown_content.append(f"## {element.get_text()}\n")
            elif element.name == 'h3':
                markdown_content.append(f"### {element.get_text()}\n")
            elif element.name == 'p':
                markdown_content.append(f"{element.get_text()}\n\n")
            elif element.name == 'li':
                markdown_content.append(f"- {element.get_text()}")
            elif element.name == 'div':
                text = element.get_text(strip=True)
                if text:
                    markdown_content.append(f"{text}\n")

        content = "\n".join(markdown_content)
        return content[:self.max_num_chars]