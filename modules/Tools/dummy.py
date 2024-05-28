from utils import add_root_to_path

hereiz_root = add_root_to_path()
from modules.Tools import SearchSummerizer
from MakeSearchTool import SearchManager

s = SearchManager(10000,1)
summerizer = SearchSummerizer()

query = "neural network in AI"

# result = s.integrated_search(query)
# print(result)
# print("-"*100)
# summary = summerizer.make_search_summary(result[0]['content'],"summerize this is the form of 30 key points ")
# print(summary)
# print("-"*100)

print(s)
logs = s.call_and_log("integrated_search","query")
print(logs)

print(summerizer)
logs = summerizer.call_and_log("make_search_summary","A","B")
print(logs)