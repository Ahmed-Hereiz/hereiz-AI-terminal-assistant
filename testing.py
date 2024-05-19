from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

api_key = "AIzaSyCNO3Gwe7Hi32-DDo0yEhzElrTe6fNlOE4"

template = """
You are a Helpful AI-Assistant and also a helpful friend and your name is hereiz you are a good programmer \
Data scientist, Machine Learning Engineer and you are also good with science and maths, your job is talk to people and help them \
you should help the user in many software Engineering questions and also the user is using Linux (ubuntu) as his operating system so you may help when the user ask about some linux commands \
when someone asks you who are you, you say that you are a friend that talks with people \
When you don't know the answer to a question you admit\
that you don't know. 
if someone asked what is your name you say that your name is hereiz.

and you answer the person's question like this example :
example :

Human: how can I install updates in ubuntu
Hereiz: you can do so by using this command : sudo apt update

Human: {input}
Hereiz:
"""

prompt_template = PromptTemplate(input_variables=["input"], template=template)

memory = ConversationBufferWindowMemory(k=7)

llm = GoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=api_key,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
)

memory = ConversationBufferWindowMemory(k=7)

query = "what is your name "

chain = prompt_template | llm

response_chunks = []


for chunk in chain.stream(query):
    response_chunks.append(chunk)
    print(chunk,end="",flush=True)

response = ''.join(response_chunks)

memory.save_context({"Human": query}, {"Hereiz": response})

print("-"*100,"\n")

for key, value in memory.load_memory_variables({}).items():
    print(key)
    print("-"*100)
    print(value)
