from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain


def model_ask(api_key, template, input_text, model, temperature, safety_settings):

    llm = ChatGoogleGenerativeAI(google_api_key=api_key,
                                 model=model,
                                 temperature=temperature,
                                 safety_settings=safety_settings
                                )
    
    prompt_template = PromptTemplate(input_variables=["history", "input"], template=template)


    conversation = ConversationChain(
        prompt=prompt_template,
        llm=llm, 
        verbose=False
    )
    
    response = conversation.predict(input=input_text)

    return response
