from utils import add_root_to_path
hereiz_root = add_root_to_path()

from modules.Tools import SearchSummerizer
from modules.Tools import SearchManager

s = SearchManager(4000,3)
summerizer = SearchSummerizer()

query = "Latest AI advancements in 2024"

results = s.integrated_search(query)

for result in results:
    print(result['title'],'\n\n')
    print(result['content'])
    print("-"*100)
# summary = summerizer.make_search_summary(result[0]['content'],"summerize this is the form of 10 key points ")
# print(summary)
# print("-"*100)


class SearcherAgent:
    def __init__(self, SearchManager, SearchSummerizer):

        self.SearchManager = SearchManager()
        self.SearchSummerizer = SearchSummerizer()

    



prompt = """

You are an agent designed to perform searches
You run in a loop of Thought, Action, PAUSE, Action_Response.
At the end of the loop you output an Answer.

Use Thought to understand the question you have been asked.
Use Action to run of the actions available to you - then return PAUSE.
Action_Response will be the result of running those actions.

Your available actions are:

{
    "function_name": "integrated_search",
    "function_params": [
        "query"
    ],
    "function_description": "Performs an integrated search: searches for the query, fetches content from the top results, and returns a summary of the results. :param query: The search query. :return: A list of dictionaries containing the title, link, and content of the top search results."
}


Example session :

Query: tell me what is latest AI advancements and write in a form of 10 points.

Thought: I should first search for Latest AI advancements in 2024.

Action :
{
    "function_name": "integrated_search",
    "function_parms": "Latest AI advancements in 2024"
}

PAUSE

you will be called again with this :

Action_response: "the large text came from the web"

Thought: Now I have the full text I need now to summarize output as user wanted to make it in the form of 10 key points.

You then output :

10 Import points about Latest Developments of AI :

1. Chatbots will become more user-friendly and customizable in 2024.
2. Multimodal AI models will unlock new applications, such as real estate listing descriptions.
3. Text-to-video AI is rapidly improving and will revolutionize content creation.
4. Deepfake technology is being used for marketing and training purposes.
5. AI-generated election disinformation and deepfakes are a growing concern.
6. Techniques to track and mitigate AI-generated fake news are still in development.
7. Roboticists are using generative AI techniques to build more general-purpose robots.
8. Generative AI requires vast amounts of data, which is a challenge for robots.
9. Researchers are developing techniques to help robots learn from limited data.
10. AI will continue to dominate and shape the agenda for researchers, regulators, and the public in the coming years.1. Chatbots will become more user-friendly and customizable in 2024.
2. Multimodal AI models will unlock new applications, such as real estate listing descriptions.
3. Text-to-video AI is rapidly improving and will revolutionize content creation.
4. Deepfake technology is being used for marketing and training purposes.
5. AI-generated election disinformation and deepfakes are a growing concern.
6. Techniques to track and mitigate AI-generated fake news are still in development.
7. Roboticists are using generative AI techniques to build more general-purpose robots.
8. Generative AI requires vast amounts of data, which is a challenge for robots.
9. Researchers are developing techniques to help robots learn from limited data.
10. AI will continue to dominate and shape the agenda for researchers, regulators, and the public in the coming years.

Query: {Query}
"""
