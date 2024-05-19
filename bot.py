import argparse
import os
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from colorama import Fore
from memory.manage_memory import MemoryManager
from langchain.chains import ConversationChain

os.environ['API_KEY'] = "AIzaSyCNO3Gwe7Hi32-DDo0yEhzElrTe6fNlOE4"

with open('template.txt', 'r') as template_file:
    template = template_file.read()

memory_manager = MemoryManager('memory/memory_buffer')

def main(api_key, template, input_text, memory_buffer):

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Terminal Chatbot", allow_abbrev=False)
    parser.add_argument("--ask", type=str, help="Your question to the model")
    args, unknown = parser.parse_known_args()
    
    

    if unknown:
        print(f"Ignoring unknown argument(s): {', '.join(unknown)}")

    if not args.ask:
        print("Usage: hereiz --ask 'your question'")
    else:
        buffer = memory_manager.load_memory()
        response, new_buffer = main(os.getenv('API_KEY'), template, args.ask, buffer)
        print(Fore.CYAN + "Hereiz:")
        print(Fore.CYAN + response + "\n")

        memory_manager.save_buffer(new_buffer)
    

