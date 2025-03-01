from customAgents.agent_llm import BaseLLM
from customAgents.agent_prompt import ReActPrompt
from customAgents.agent_tools import ToolKit, SearchTool, PythonRuntimeTool
from customAgents.runtime import ReActRuntime


class SearchLLM(BaseLLM):
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings=None):
        super().__init__(api_key, model, temperature, safety_settings)

    def llm_generate(self, input: str) -> str:
        return super().generate_response(input,output_style="green")


class SearchPrompt(ReActPrompt):
    def __init__(self, question: str, prompt_string: str = ""):

        example_workflow = """
Question: What is the date today ?

[you in iteration 1]
Thought: I have to search for the day today using the internet to get a good resault.
Action: search tool
Action Input: today's date

[you then STOP the first iteration after this]


... (not generated by AI it comes as from a software code) Observation: [the tool will return the today's date to you so you have to read the observation carefully to answer in the next step using it (you don't generate observation it just comes to you)]

[you in iteration 2]
Thought: from the previous Observation I can find good and specific information that can answer the user original question which is "What is the date today ?"
Action: finish
Final Answer: Today's date is... [if there is more to describe to make chat more user friendly do it]


Question: What is the product of 22 and 33 ?

[you in iteration 1]
Thought: I have to use python code to find the answer
Action: python tool
Action Input: 
```python

print(22*33)

```

[you then STOP the first iteration after this]

[you in iteration 2]
Thought: from the previous Observation I can find good and specific information that can answer the user original question which is "what is the product of 22 and 33"
Action: finish
Final Answer: the product of 22 * 33 is 726 [if there is more to describe to make chat more user friendly do it]

"""

        super().__init__(question, example_workflow=example_workflow, prompt_string=prompt_string)
        

class SearchAgent(ReActRuntime):
    def __init__(self, llm, prompt):

        search_tool = SearchTool(description="tool that can search internet (each query you input will get different search) Note that it accepts only one param",tool_name="search_tool")
        python_tool = PythonRuntimeTool(description="tool that can run python code (give the code for this function as md format)",tool_name="python_tool")
        toolkit = ToolKit(tools=[search_tool,python_tool])

        super().__init__(llm, prompt, toolkit=toolkit)

    def loop(self, agent_max_steps: int = 15) -> str:
        return super().loop(agent_max_steps)
