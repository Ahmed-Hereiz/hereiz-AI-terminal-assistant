from agent_prompt import BasePrompt
    

class ReActPrompt(BasePrompt):
    def __init__(self, question: str,  example_workflow: str = "", prompt_string: str = ""):
        
        self.example_workflow = example_workflow
        self.question = question

        super().__init__(prompt_string)


    def _generate_prompt(self):

        react_prompt = """
{prompt_string}
Answer the following questions as best you can. You have access to the following tools:
{tools_and_role}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action Make sure to return these parameters as python list
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

{example_workflow}

Begin!

Question: {question}
"""

        react_prompt.replace("{example_workflow}",self.example_workflow)
        react_prompt.replace("{prompt_string}",self.prompt_string)
        react_prompt.replace("{question}",self.question)

        return react_prompt