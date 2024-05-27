from langchain_core.output_parsers import StrOutputParser
from langchain.prompts.prompt import PromptTemplate
from utils import get_arguments, add_root_to_path
from model_ask import ModelAsk

hereiz_root = add_root_to_path()
from common import load_config, load_template, parse_safety_settings

def handle_ask():
    config = load_config('../../config/llm.json')
    template = load_template('../../templates/ask_template.txt')
    safety_settings = parse_safety_settings(config['safety_settings'])

    prompt_template = PromptTemplate(input_variables=["input"], template=template)

    model_ask = ModelAsk(config['api_key'],
                         config['model'],
                         config['ask_model_temperature'],
                         safety_settings,
                         prompt_template,
                         StrOutputParser()
                         )

    args = get_arguments()
    if not args.ask:
        print("Usage: hereiz --ask 'your question'")
        return
    
    model_ask.generate_stream(model_input=args.ask)
