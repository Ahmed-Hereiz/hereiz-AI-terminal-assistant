from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain


def model_ask(api_key, template, input_text):

    llm = ChatGoogleGenerativeAI(google_api_key=api_key,
                                 model="gemini-pro",
                                 temperature=0.7,
                                 safety_settings={
                                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                                },
                                )
    
    prompt_template = PromptTemplate(input_variables=["history", "input"], template=template)


    conversation = ConversationChain(
        prompt=prompt_template,
        llm=llm, 
        verbose=False
    )
    
    response = conversation.predict(input=input_text)

    return response
