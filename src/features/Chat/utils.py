import json
import argparse
from langchain_google_genai import HarmBlockThreshold, HarmCategory

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def load_template(template_path):
    with open(template_path, 'r') as template_file:
        return template_file.read()

def parse_safety_settings(settings):
    return {
        HarmCategory[category]: HarmBlockThreshold[threshold]
        for category, threshold in settings.items()
    }

def get_arguments():
    parser = argparse.ArgumentParser(description="Terminal Chatbot", allow_abbrev=False)
    parser.add_argument("--chat","-c", type=str, help="Your question to the model")
    args, unknown = parser.parse_known_args()

    if unknown:
        print(f"Ignoring unknown argument(s): {', '.join(unknown)}")

    return args