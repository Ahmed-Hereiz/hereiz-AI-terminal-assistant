import requests
from bs4 import BeautifulSoup
from typing import Any
from agent_tools import BaseTool


class LinkedinProfileScrapeTool(BaseTool):
    def execute_func(self, profile_url) -> Any:
        profile_data = self._get_profile_data(profile_url)
        md_content = "# LinkedIn Profile\n\n"
        md_content += f"## {profile_data['name']}\n"
        md_content += f"**Headline:** {profile_data['headline']}\n\n"
        md_content += f"**Summary:** {profile_data['summary']}\n\n"
        return md_content

    def _get_profile_data(self, profile_url):
        page = requests.get(profile_url)
        src = page.text
        soup = BeautifulSoup(src, "html.parser")

        name_tag = soup.find("li", {"class": "inline t-24 t-black t-normal break-words"})
        name = name_tag.get_text(strip=True) if name_tag else "N/A"

        headline_tag = soup.find("h2", {"class": "mt1 t-18 t-black t-normal break-words"})
        headline = headline_tag.get_text(strip=True) if headline_tag else "N/A"

        summary_section = soup.find("section", {"id": "summary"})
        summary = summary_section.find("p").get_text(strip=True) if summary_section else "N/A"

        profile_data = {
            "name": name,
            "headline": headline,
            "summary": summary
        }
        return profile_data

class LinkedinProfileScrapeSaveTool(LinkedinProfileScrapeTool):
    def execute_func(self, profile_url, output_file) -> Any:
        profile_data = self._get_profile_data(profile_url)
        with open(output_file, "w") as f:
            f.write("# LinkedIn Profile\n\n")
            f.write(f"## {profile_data['name']}\n")
            f.write(f"**Headline:** {profile_data['headline']}\n\n")
            f.write(f"**Summary:** {profile_data['summary']}\n\n")

