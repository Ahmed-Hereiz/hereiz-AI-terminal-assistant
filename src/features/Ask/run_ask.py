from langchain_core.output_parsers import StrOutputParser
from langchain.prompts.prompt import PromptTemplate
from utils import load_config, load_template, parse_safety_settings, get_arguments
from model_ask import ModelAsk


def handle_ask():
    config = load_config('../../config/config.json')
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
    
    model_ask._generate_stream(model_input=args.ask)


if __name__ == "__main__":
    handle_ask()

    

