from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class MemoryManager:
    def __init__(self, memory_file):
        self.memory_file = memory_file

    def save_buffer(self, new_string):
        """Overwrites the file with the new string."""
        with open(self.memory_file, 'w') as file:
            file.write(new_string)

    def clear_memory(self):
        """Clears the file content."""
        open(self.memory_file, 'w').close()

    def load_memory(self):
        """Loads the current content of the memory file."""
        try:
            with open(self.memory_file, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return 'File not found in the specified directory or location'
        
