from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
from langchain.agents import initialize_agent, Tool

class SearchBot:
    def __init__(self,api_key,template,tool_function):

        self.llm = ChatGoogleGenerativeAI(google_api_key=api_key,
                                        model="gemini-pro",
                                        temperature=0.7,
                                        safety_settings=
                                        {
                                            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                                        },
                                        )
        
        self.prompt_template = PromptTemplate(input_variables=["input"], template=template)

        self.integrated_tool = Tool(
                                name="IntegratedSearchAndSummarize",
                                func=tool_function,
                                description="Perform a web search and summarize the top results, where I want from you to make the output in the form of points"
                                )
        
        
    def extract_keywords(self, query):

        conversation = ConversationChain(prompt=self.prompt_template,llm=self.llm, verbose=False)

        response = conversation.predict(input=query)
        return response
    
    def use_search_agent(self, query):

        agent = initialize_agent(llm=self.llm,tools=[self.integrated_tool],agent_type="zero-shot-react-description",verbose=False)

        response = agent.run(query)
        return response