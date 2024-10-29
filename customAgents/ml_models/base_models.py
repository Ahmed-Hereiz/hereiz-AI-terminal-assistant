from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseModels(ABC):
    def __init__(self, model_type: Optional[str] = None, model_params: Optional[Dict[str, Any]] = None):
        self.model_type = model_type
        self.model_params = model_params or {}
        self.model = None

    @abstractmethod
    def load_model(self) -> None:
        """Load the model. This method should be implemented by subclasses."""
        pass

    @abstractmethod
    def inference(self, input_data: Any) -> Any:
        """
        Implement the model inference logic here.
        
        Args:
            input_data: The input data for the model.

        Returns:
            The output of the model inference.
        """
        pass

    def preprocess(self, input_data: Any) -> Any:
        """
        Preprocess the input data before inference.
        
        Args:
            input_data: The raw input data.

        Returns:
            The preprocessed input data.
        """
        return input_data

    def postprocess(self, output: Any) -> Any:
        """
        Postprocess the model output.
        
        Args:
            output: The raw output from the model.

        Returns:
            The postprocessed output.
        """
        return output

    def __str__(self) -> str:
        return f"BaseModels(model_type={self.model_type}, model_params={self.model_params})"

    def __repr__(self) -> str:
        return self.__str__()