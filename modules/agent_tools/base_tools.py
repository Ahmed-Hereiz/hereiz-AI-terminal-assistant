from typing import Any, Dict, Callable


class BaseTool:
    def __init__(self, tools: Dict[str, Callable] = {}):
        """
        Initializes the BaseTool with the given tools.

        :param tools: A dictionary where keys are tool names and values are callable functions.
        """
        self.tools = tools
        self.tools_names = list(tools.keys())
        self.tools_executes = list(tools.values())
        self.tool_instructions = self._format_tool_instructions()


    def _format_tool_instructions(self) -> str:
        """
        Formats the tool instructions into a string with function names and their docstrings.

        :return: A formatted string with function names and descriptions.
        """
        instructions = ""
        for name, func in self.tools.items():
            instructions += f"({name}): {func.__doc__}\n"
        return instructions


    def execute_func(self, func_name: str, *params: Any) -> Any:
        """
        Executes the given function with provided parameters.

        :param func_name: The name of the function to execute.
        :param params: Parameters to pass to the function.
        :return: The result of the function execution.
        :raises ValueError: If the function is not found in the tools.
        """
        if func_name in self.tools and callable(self.tools[func_name]):
            return self.tools[func_name](*params)
        else:
            raise ValueError(f"Function '{func_name}' is not found or is not callable.")


    def clean_docstring(self, docstring: str) -> str:
        """
        Cleans a docstring by removing leading/trailing whitespace and extra spaces.

        :param docstring: The docstring to clean.
        :return: The cleaned docstring.
        """
        if not docstring:
            return ""
        lines = [line.strip() for line in docstring.strip().split('\n')]
        return ' '.join(line for line in lines if line)


    def __repr__(self) -> str:
        """
        Returns a string representation of the BaseTool instance.

        :return: A string representation of the BaseTool instance.
        """
        return f"BaseTool(tools={self.tools})"


    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the BaseTool instance.

        :return: A string representation of the BaseTool instance.
        """
        return f"BaseTool with tools: {self.tools_names}"
