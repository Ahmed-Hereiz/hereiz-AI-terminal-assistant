from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain


def model_chat(api_key, template, input_text, memory_buffer, model, temperature, safety_settings):

    llm = ChatGoogleGenerativeAI(google_api_key=api_key,
                                 model=model,
                                 temperature=temperature,
                                 safety_settings=safety_settings
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
