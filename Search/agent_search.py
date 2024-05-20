import warnings
from contextlib import contextmanager
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain.agents import initialize_agent, Tool

from manage_search import SearchManager

@contextmanager
def suppress_warnings():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="The function `initialize_agent` was deprecated.*")
        warnings.filterwarnings("ignore", message="The method `Chain.run` was deprecated.*")
        yield

with suppress_warnings():
    manage_search = SearchManager(max_num_chars=2000,num_top_results=1)

    api_key = "AIzaSyCNO3Gwe7Hi32-DDo0yEhzElrTe6fNlOE4"


    llm = ChatGoogleGenerativeAI(google_api_key=api_key,
                                    model="gemini-pro",
                                    temperature=0.7,
                                    safety_settings={
                                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                                    },
                                    )
       

    integrated_tool = Tool(
        name="IntegratedSearchAndSummarize",
        func=manage_search.integrated_search_and_summarize,
        description="Perform a web search and summarize the top results, where I want from you to make the output in the form of points"
    )

    agent = initialize_agent(
        llm=llm,
        tools=[integrated_tool],
        agent_type="zero-shot-react-description",
        verbose=False
    )

    response = agent.run("who is elon musk")
    #print(response['output'])
    print(response)