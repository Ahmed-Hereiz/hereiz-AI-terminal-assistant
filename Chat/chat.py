from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain


def model_chat(api_key, template, input_text, memory_buffer):

    llm = ChatGoogleGenerativeAI(google_api_key=api_key,
                                 model="gemini-pro",
                                 temperature=0.7,
                                 safety_settings={
                                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                                },
                                )
    
    prompt_template = PromptTemplate(input_variables=["history", "input"], template=template)

    memory = ConversationSummaryMemory(llm=llm, max_token_limit=1000,buffer=memory_buffer)

    conversation = ConversationChain(
        prompt=prompt_template,
        llm=llm, 
        verbose=False,
        memory=memory
    )
    
    response = conversation.predict(input=input_text)

    return response, memory.buffer
