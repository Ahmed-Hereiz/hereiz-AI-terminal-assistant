from langchain.prompts.prompt import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel,Field

from utils import add_root_to_path

hereiz_root = add_root_to_path()
from modules.Models import BaseModel

class SearchKeywordExtractModel(BaseModel):
    """
    Initializes the SearchSummerizeModel with the given parameters by calling the parent class constructor.

    :param api_key: The API key for Google Generative AI.
    :param model: The model to use.
    :param temperature: The temperature setting for the model.
    :param safety_settings: Safety settings for the model.
    :param prompt_template: A PromptTemplate instance.
    """



    template = """
        you are a search keyword extractor model where you are given a description of what the user want to search for and your role is to output two things which are,
        - reformating the user search query to make it 
    
    """
