import argparse
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory, ConversationBufferWindowMemory
from langchain.prompts.prompt import PromptTemplate
from colorama import Fore


os.environ['API_KEY'] = "AIzaSyCNO3Gwe7Hi32-DDo0yEhzElrTe6fNlOE4"

with open('template.txt', 'r') as template_file:
    template = template_file.read()

def main(api_key, template, input_text):

    llm = ChatGoogleGenerativeAI(google_api_key=api_key,model="gemini-pro",temperature=0.7)
    
    prompt_template = PromptTemplate(input_variables=["input"], template=template)
    
    # memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=500)

    # memory = ConversationBufferWindowMemory(k=7)

    conversation = ConversationChain(
        prompt=prompt_template,
        llm=llm, 
        verbose=False
    )
    
    response = conversation.predict(input=input_text)

    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Terminal Chatbot", allow_abbrev=False)
    parser.add_argument("--ask", type=str, help="Your question to the model")
    args, unknown = parser.parse_known_args()
    
    

    if unknown:
        print(f"Ignoring unknown argument(s): {', '.join(unknown)}")

    if not args.ask:
        print("Usage: hereiz --ask 'your question'")
    else:
        response = main(os.getenv('API_KEY'), template, args.ask)
        print(Fore.CYAN + "Hereiz:")
        print(Fore.CYAN + response)
    

