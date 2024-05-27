from utils import add_root_to_path
from typing import Any

hereiz_root = add_root_to_path()
from fonts import CustomizeOutputTerminal
from shared import ChainBasicModel 

class ModelAsk(ChainBasicModel):
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings: Any, prompt_template: Any, parser: Any):

        super().__init__(api_key, model, temperature, safety_settings, prompt_template, parser)

    def generate_stream(self, model_input):

        print(CustomizeOutputTerminal(hereiz_root).customize_output("Hereiz : "))

        for chunk in self.chain.stream({"input":{model_input}}):
            print(chunk, end='', flush=True)
 
        CustomizeOutputTerminal(hereiz_root).reset_all()