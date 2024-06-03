import requests
from bs4 import BeautifulSoup # type: ignore
from utils import add_root_to_path
hereiz_root = add_root_to_path()

from modules.Tools import ToolBase


class GithubAccountScraper(ToolBase):
    def __init__(self, username):

        self.username = username
        self.page_url = f"https://github.com/{username}?tab=repositories"
        self.page = requests.get(self.page_url)

    
    def get_all_repos(self):
        src = self.page.text
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
    

    def save_data_md(self, all_repos, output_file):
        with open(output_file, "w") as f:
            f.write("# Resume\n\n")
            f.write("## Projects\n")
            for repo in all_repos:
                repo_name = repo['name']
                repo_url = repo['url']
                language = repo['language']
                
                f.write(f"### [{repo_name}]({repo_url})\n")
                f.write(f"**Language:** {language}\n\n")

