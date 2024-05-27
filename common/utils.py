import json
from langchain_google_genai import HarmBlockThreshold, HarmCategory

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def load_template(template_path):
    with open(template_path, 'r') as template_file:
        return template_file.read()
    
def load_memory_buffer(memory_buffer_path):
    with open(memory_buffer_path, 'r') as memory_buffer:
        return memory_buffer.read()

def parse_safety_settings(settings):
    return {
        HarmCategory[category]: HarmBlockThreshold[threshold]
        for category, threshold in settings.items()
    }