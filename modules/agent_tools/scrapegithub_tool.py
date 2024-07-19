import requests
from bs4 import BeautifulSoup # type: ignore
from typing import Any
from modules.agent_tools import BaseTool


class GithubAccScrapeTool(BaseTool):
    def execute_func(self, username) -> Any:
        
        all_repos = self._get_all_repos(username=username)
        md_content = "# Resume\n\n"
        md_content += "## Projects\n"
        for repo in all_repos:
            repo_name = repo['name']
            repo_url = repo['url']
            language = repo['language']
            
            md_content += f"### [{repo_name}]({repo_url})\n"
            md_content += f"**Language:** {language}\n\n"
        
        return md_content


    def _get_all_repos(self, username):
        page_url = f"https://github.com/{username}?tab=repositories"
        page = requests.get(page_url)
        src = page.text
        soup = BeautifulSoup(src, "lxml")
        all_repos = []
        repos = soup.find_all("div", {"class": "col-10 col-lg-9 d-inline-block"})
        
        for repo in repos:
            name = repo.find("h3").get_text(strip=True)[0:-6]
            url = f"https://github.com{repo.find('a')['href']}"
            language_tag = repo.find('span', itemprop='programmingLanguage')
            language = language_tag.get_text(strip=True) if language_tag else "N/A"

            all_repos.append({
                "name": name,
                "url": url,
                "language": language
            })
        
        return all_repos
    

class GithubAccScrapeSaveTool(GithubAccScrapeTool):
    def execute_func(self, username, output_file) -> Any:
        
        all_repos = super()._get_all_repos(username)
        with open(output_file, "w") as f:
            f.write("# Resume\n\n")
            f.write("## Projects\n")
            for repo in all_repos:
                repo_name = repo['name']
                repo_url = repo['url']
                language = repo['language']
                
                f.write(f"### [{repo_name}]({repo_url})\n")
                f.write(f"**Language:** {language}\n\n")

