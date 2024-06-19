from .reformat_strings import (
    replace_history_sentence,
    replace_instructions_sentence,
    replace_input_sentence,
    extract_json_from_string,
    replace_placeholder
)

from .fetch_data import (
    extract_fetched_data,
    concat_fetched_content,
    concat_links_and_titles
)

__all__ = [
    'replace_history_sentence',
    'replace_instructions_sentence',
    'replace_input_sentence',
    'extract_json_from_string',
    'extract_fetched_data',
    'concat_fetched_content',
    'concat_links_and_titles',
    'replace_placeholder'
]