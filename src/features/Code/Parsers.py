from langchain_core.pydantic_v1 import BaseModel, Field

class ParseOutFileRunner(BaseModel):
    syntax_check: int = Field(description="Identify any syntax errors or issues in the code. if no errors output 0 if errors write 1")
    language_classification: str = Field(description="Specify the programming language of the provided code.") 
    dependencies_and_libraries: list = Field(description="Identify required dependencies (this dependencies will be taken by another command to pip install them so make sure to only write what will be installed with pip only).")
    directory_requirements: list = Field(description="Identify any specific directory or file requirements for running the code.")
    file_name: str = Field(description="Specify the file name with the appropriate extension.")
    command: str = Field(description="Generate the linux terminal command needed to run the code.")