from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from utils import add_root_to_path
hereiz_root = add_root_to_path()

from modules.Tools import SearchManager, SearchSummarizer
from common.utils import load_config

class ParseOutSearch(BaseModel):
    search: str = Field(description="return better search query keywords")
    description: str = Field(description="return a description about how to make better results for the user using the search results")


class RedirectSearchTools:
    def __init__(self, max_num_chars: int = None, num_top_results: int = None):
        self.settings_config = self._load_default_settings()

        self.max_num_chars = max_num_chars or self.settings_config['max_num_chars_search_agent']
        self.num_top_results = num_top_results or self.settings_config['num_top_results_search_agent']

        self._load_default_settings()

        self.search_manger = SearchManager(
            max_num_chars=self.max_num_chars,
            num_top_results=self.num_top_results
        )

        self.summarizer = SearchSummarizer()

        self.parser = self._initialize_parser()
        self.tools = [self.search_manger, self.summarizer]

    def _load_default_settings(self) -> dict:

        settings_config_path = f'{hereiz_root}/config/settings.json'
        settings_config = load_config(settings_config_path)
        return settings_config

    @staticmethod
    def _initialize_parser() -> JsonOutputParser:
        return JsonOutputParser(pydantic_object=ParseOutSearch)