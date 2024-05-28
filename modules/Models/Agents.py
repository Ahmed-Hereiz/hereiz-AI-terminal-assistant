# from langchain_google_genai import ChatGoogleGenerativeAI
# from typing import Any

# from utils import add_root_to_path
# hereiz_root = add_root_to_path()
# from common.utils import load_config, parse_safety_settings

# config = load_config('../../../config/llm.json')
# safety_settings = parse_safety_settings(config['safety_settings'])

# class SimpleAgent:
#     def __init__(self, prompt_template):
#         """
#         Initializes the SimpleAgent with the specified configuration and safety settings.
#         """
#         self._llm = ChatGoogleGenerativeAI(
#             config['api_key'],
#             config['model'],
#             config['search_model_temperature'],
#             safety_settings
#         )

#         self._prompt_template = prompt_template
#         self._chain = self._prompt_template | self._llm 

#     def generate_stream(self, query: str):
#         """
#         Generates a search summary based on the provided input and description.

#         :param input: The search input.
#         :param description: The description to guide the summary.
#         :return: The generated summary.
#         """

#         for chunk in self._chain.stream({"input":{query}}):
#             print(chunk,end='',flush=True)
