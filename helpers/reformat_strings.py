import json

def replace_history_sentence(template, memory_buffer):
    return template.replace("{history}",memory_buffer)


def replace_instructions_sentence(template, instructions):
    return template.replace("{format_instructions}",instructions)

def replace_input_sentence(template, user_input):
    return template.replace("{input}",user_input)

def replace_placeholder(template, placeholder, value):
    return template.replace(placeholder, value)


def extract_json_from_string(text: str):
    json_objects = []
    brace_stack = []
    json_str = ""
    inside_json = False

    for _, char in enumerate(text):
        if char == '{':
            brace_stack.append(char)
            inside_json = True
        if inside_json:
            json_str += char
        if char == '}':
            brace_stack.pop()
            if not brace_stack:
                inside_json = False
                try:
                    json_object = json.loads(json_str)
                    json_objects.append(json_object)
                except json.JSONDecodeError:
                    pass
                json_str = ""

    return json_objects