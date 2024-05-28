import json
from typing import Any, Dict, Callable

class ToolBase:
    def __init__(self):
        """
        Initializes the BaseModel.
        """
        pass

    def __repr__(self) -> str:
        """
        Returns a string representation of the BaseModel instance.
        """
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the BaseModel instance.
        """
        return f"Instance of {self.__class__.__name__}"

    def __eq__(self, other: Any) -> bool:
        """
        Checks equality between this instance and another BaseModel instance.
        """
        return isinstance(other, self.__class__)

    def clean_docstring(self, docstring: str) -> str:
        """
        Cleans and formats a docstring by removing leading and trailing whitespace and unnecessary newlines.

        :param docstring: The docstring to clean.
        :return: The cleaned docstring.
        """
        if not docstring:
            return ""
        lines = [line.strip() for line in docstring.strip().split('\n')]
        return ' '.join(line for line in lines if line)

    def log_method_call(self, function_name: str, function_params: Dict[str, Any], function_description: str = "") -> str:
        """
        Logs the method call with its name, parameters, and description in JSON format.

        :param function_name: Name of the function being called.
        :param function_params: Parameters passed to the function.
        :param function_description: Description of the function.
        :return: JSON string of the logged method call.
        """
        log_entry = {
            "function_name": function_name,
            "function_params": function_params,
            "function_description": self.clean_docstring(function_description)
        }
        return json.dumps(log_entry, indent=4)

    def call_and_log(self, method_name: str, *args: Any, **kwargs: Any) -> str:
        """
        Calls the specified method with the given arguments and returns the log of the function call.

        :param method_name: The name of the method to call.
        :param args: Positional arguments to pass to the method.
        :param kwargs: Keyword arguments to pass to the method.
        :return: JSON string of the logged method call.
        """
        method: Callable[..., Any] = getattr(self, method_name)
        result = method(*args, **kwargs)
        # function_params = {"args": args, "kwargs": kwargs}
        log = self.log_method_call(method_name, args, method.__doc__ or "")
        return log
    
    