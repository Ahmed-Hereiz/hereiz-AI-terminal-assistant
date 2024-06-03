from langchain_core.output_parsers import StrOutputParser
from langchain.prompts.prompt import PromptTemplate
from utils import get_arguments, add_root_to_path
from model_chat import ModelChat

hereiz_root = add_root_to_path()
from common import MemoryManager, load_config, load_template, parse_safety_settings
from helpers import replace_history_sentence
from modules.Models import MemorySummarizerModel


def hande_chat():
    config = load_config('../../config/llm.json')
    template = load_template('../../templates/chat_template.txt')
    safety_settings = parse_safety_settings(config['safety_settings'])

    manage_memory = MemoryManager('../../data/history/memory/chat_memory_buffer')
    memory_buffer = manage_memory.load_memory()

    template_with_history = replace_history_sentence(template,memory_buffer)

    prompt_template = PromptTemplate(input_variables=["input"], template=template_with_history)

    model_chat = ModelChat(config['api_key'],
                           config['model'],
                           config['chat_model_temperature'],
                           safety_settings,
                           prompt_template,
                           StrOutputParser(),
                           )
    
    
    memory_summerizer = MemorySummarizerModel(config['api_key'],
                                            config['model'],
                                            config['chat_model_temperature'],
                                            safety_settings)
    
    args = get_arguments()
    if not args.chat:
        print("Usage: hereiz --chat 'your question'")
        return 
    
    response = model_chat.generate_stream(model_input=args.chat)

    new_buffer = memory_summerizer.add_memory(memory_buffer,args.chat,response)

    manage_memory.save_buffer(new_buffer)
