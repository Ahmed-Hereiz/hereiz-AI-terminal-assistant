import requests
from bs4 import BeautifulSoup  # type: ignore

def fetch_github_profile(username):
    url = f"https://github.com/{username}?tab=repositories"
    response = requests.get(url)
    return response.text

def extract_repositories(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    repos = []
    repo_elements = soup.find_all('li', class_='Box-row')
    
    for repo_element in repo_elements:
        name = repo_element.find('h3').get_text(strip=True)
        description_tag = repo_element.find('p', class_='col-9 color-text-secondary my-1 pr-4')
        description = description_tag.get_text(strip=True) if description_tag else "No description provided"
        url = 'https://github.com' + repo_element.find('a', class_='v-align-middle')['href']
        language = repo_element.find('span', class_='d-inline-block ml-0 mr-3').get_text(strip=True)
        stars = repo_element.find('a', class_='Link--muted').get_text(strip=True)
        forks = repo_element.find('a', class_='Link--muted').next_sibling.get_text(strip=True)

        repos.append({
            "name": name,
            "description": description,
            "url": url,
            "stars": stars,
            "forks": forks,
            "language": language
        })
    return repos

def fetch_readme_content(username, repo_name):
    url = f"https://raw.githubusercontent.com/{username}/{repo_name}/main/README.md"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return "No README file found."

def generate_resume(repo_info):
    with open("resume.md", "w") as f:
        f.write("# Resume\n\n")
        f.write("## Projects\n")
        for info in repo_info:
            readme_content = fetch_readme_content(username, info['name'])
            f.write(f"### [{info['name']}]({info['url']})\n")
            f.write(f"**README:**\n{readme_content}\n\n")
            f.write(f"**Stars:** {info['stars']} | **Forks:** {info['forks']} | **Language:** {info['language']}\n\n")
    print("Resume generated in resume.md")

username = "Ahmed-Hereiz"
page_content = fetch_github_profile(username)
print(page_content)
repo_info = extract_repositories(page_content)
print(repo_info)
generate_resume(repo_info)
