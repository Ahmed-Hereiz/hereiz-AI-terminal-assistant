from type_utils import agent_models_type
## This is still dummy implementation for the BaseModels.. will be updated later !!


@agent_models_type
class BaseModels:
    def __init__(self, model_type=None):
        self.model_type = model_type

    def inference(self):
        """Implement the model inference logic here"""

        return 0
    
    def __str__(self) -> str:
        return f"initialized model {self.model_type}"

    def __repr__(self) -> str:
        return f"initialized model {self.model_type}"