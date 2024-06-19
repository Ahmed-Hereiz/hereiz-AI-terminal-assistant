from utils import add_root_to_path
hereiz_root = add_root_to_path()

from modules.Tools import SearchManager

url="https://synapseanalytics.recruitee.com/o/senior-machine-learning-engineer-computer-vision"
s = SearchManager()
r = s.fetch_content_from_url(url=url)
print(r)

