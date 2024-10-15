from customAgents.agent_models import BaseModels
from gradio_client import Client


class GradioClientModels(BaseModels):
    def __init__(self, gradio_client_id : str, api_name : str = None):
        
        self.gradio_client_id = gradio_client_id
        self.api_name = api_name

        super().__init__()

    def inference(self, input_prompt):

        client = Client(self.gradio_client_id)
        client_output = client.predict(
            input_prompt,
            api_name=self.api_name
        )

        return client_output