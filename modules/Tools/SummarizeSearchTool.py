from utils import add_root_to_path
hereiz_root = add_root_to_path()

from modules.Tools.ModelToolBase import ToolBase
from modules.Models import SearchSummarizeModel
from common.utils import load_config, parse_safety_settings

config = load_config(f'{hereiz_root}/config/llm.json')
safety_settings = parse_safety_settings(config['safety_settings'])


class SearchSummarizer(ToolBase):
    def __init__(self):
        """
        Initializes the SearchSummarizer with the specified configuration and safety settings.
        """
        super().__init__()
        self._llm = SearchSummarizeModel(
            config['api_key'],
            config['model'],
            config['search_model_temperature'],
            safety_settings
        )

    def make_search_summary(self, input: str, description: str) -> str:
        """
        Generates a search summary based on the provided input and description.

        :param input: The search input.
        :param description: The description to guide the summary.
        :return: The generated summary.
        """

        summary = self._llm.summarize_search(input=input,description=description)

        return summary
    
    def store_search_history(self, history_file_path: str, input: str, summary: str, source_titles: str, source_links: str):
        """
        Stores the search history in a specified file.

        :param history_file_path: The path to the file where the history will be stored.
        :param input: The search input.
        :param summary: The generated summary.
        :param source_title: The title of the source.
        :param source_link: The link to the source.
        """

        search_summary = f"input:\n{input}\n\nBased on : {source_titles} [{source_links}]\n summary:\n{summary}"

        with open(history_file_path, 'a') as file:
            file.write(search_summary)

