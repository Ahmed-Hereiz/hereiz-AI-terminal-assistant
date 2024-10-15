from typing import Any, List
from customAgents.agent_tools.type_utils import agent_tools_type


@agent_tools_type
class BaseTool:
    def __init__(self, description: str, tool_name: str = None):
        """
        Base class for individual tools.

        :param tool_name: name for the tool to be excuted in runtime with.
        :param description: A description of the tool.
        """
        self.description = description
        self.tool_name = self.__class__.__name__ if tool_name is None else tool_name

    def execute_func(self, *params: Any) -> Any:
        """
        Method to be implemented by each tool. This method should define the tool's functionality.

        :param params: Parameters to pass to the function.
        :return: The result of the function execution.
        """
        raise NotImplementedError(f"Each tool must implement its own execute_func method.\n used params {params}")


class ToolKit:
    def __init__(self, tools: List[BaseTool] = []):
        """
        Initializes the ToolKit with the given tools.

        :param tools: A list of tool objects. Each tool must have 'execute_func', 'tool_name', and 'description'.
        """
        self.tools = {tool.tool_name: tool for tool in tools}
        self.tool_names = [tool.tool_name for tool in tools]
        self.tool_descriptions = {tool.tool_name: tool.description for tool in tools}
        self.tool_instructions = self._format_tool_instructions()

    def _format_tool_instructions(self) -> str:
        """
        Formats the tool instructions into a string with function names and their descriptions.

        :return: A formatted string with function names and descriptions.
        """
        instructions = ""
        for name, description in self.tool_descriptions.items():
            instructions += f"({name}): {description}\n"
        return instructions

    def execute_tool(self, tool_name: str, *params: Any) -> Any:
        """
        Executes the specified tool's execute_func method with the given parameters.

        :param tool_name: The name of the tool to execute.
        :param params: Parameters to pass to the tool's execute_func method.
        :return: The result of the tool's execute_func method.
        :raises ValueError: If the tool is not found in the toolkit.
        """
        if tool_name in self.tools:
            tool = self.tools[tool_name]
            return tool.execute_func(*params)
        else:
            raise ValueError(f"Tool '{tool_name}' is not found in the toolkit.")

    def __repr__(self) -> str:
        """
        Returns a string representation of the ToolKit instance.

        :return: A string representation of the ToolKit instance.
        """
        return f"ToolKit(tools={self.tool_names})"

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the ToolKit instance.

        :return: A string representation of the ToolKit instance.
        """
        return f"ToolKit with tools: {self.tool_names}"
    

    def __len__(self) -> int:
        """
        Returns the number of tools in the toolkit.

        :return: The number of tools.
        """
        return len(self.tools)