from typing import Any


class BasePrompt:
    def __init__(
            self,
            template_file: Any = None,
            prompt_string: str = ""
        ):

        """
        Initializes the BasePrompt with the given template file and prompt string.

        :param template_file: The path to the template file or None if not provided.
        :param prompt_string: The prompt string to be used.
        """
        self.template_file = self._format_template_file(template_file=template_file)
        self.prompt_string = self._format_prompt_string(prompt_string=prompt_string)
        self.agent_prompt = self.prompt_string


    def _format_template_file(self, template_file: Any) -> str:
        """
        Reads and returns the content of the template file.

        :param template_file: The path to the template file.
        :return: The content of the template file as a string.
        """
        if template_file is not None:
            with open(template_file, 'r') as template:
                loaded_template = template.read()
        else:
            loaded_template = ""
        return loaded_template

    def _format_prompt_string(self, prompt_string: str) -> str:
        """
        Formats the prompt string by appending it to the template file content if provided.

        :param prompt_string: The prompt string to be formatted.
        :return: The formatted prompt string.
        """
        if len(self.template_file) == 0:
            return prompt_string
        else:
            return self.template_file + '\n' + prompt_string

    def __repr__(self) -> str:
        """
        Returns a string representation of the BasePrompt instance for debugging.

        :return: A string representation of the instance.
        """
        return f"model prompt initialized with {self.prompt_string}"

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the BasePrompt instance.

        :return: A string representation of the instance.
        """
        return f"model prompt initialized with {self.prompt_string}"

    def __add__(self, other) -> str:
        """
        Concatenates the prompt string of this instance with another BasePrompt instance.

        :param other: Another BasePrompt instance.
        :return: The concatenated prompt strings.
        """
        return self.prompt_string + '\n' + other.prompt_string


