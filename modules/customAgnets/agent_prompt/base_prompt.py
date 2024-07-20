class BasePrompt:
    def __init__(self, prompt_string: str = ""):
        """
        Initializes the BasePrompt with the given template file and prompt string.

        :param prompt_string: The prompt string to be used.
        """

        self.prompt_string = prompt_string
        self.prompt = self._generate_prompt()


    def _generate_prompt(self):
        """
        method for interfacing with runtime (used inside the runtime class), setting default to use prompt_string,
        but this needs to overwritten inside every inherited class for being customizable for the use case.
        """

        return self.prompt_string


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


