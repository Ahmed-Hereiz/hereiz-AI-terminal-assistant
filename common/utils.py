import json

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)


def load_template(template_path):
    with open(template_path, 'r') as template_file:
        return template_file.read()

    
def load_memory_buffer(memory_buffer_path):
    with open(memory_buffer_path, 'r') as memory_buffer:
        return memory_buffer.read()
