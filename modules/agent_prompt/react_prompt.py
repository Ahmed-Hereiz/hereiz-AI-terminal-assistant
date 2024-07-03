from agent_prompt import BasePrompt
    

class ReActPrompt(BasePrompt):
    def __init__(self, question: str,  example_workflow: str = "", prompt_string: str = ""):
        
        self.example_workflow = example_workflow
        self.question = question

        super().__init__(prompt_string)

        self.prompt = self._generate_prompt()


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
Observation: the result of the action (NOTE THAT : it will be given to you, Don't write the Observation at all just use it if found to know more about the context)
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Action: finish
Final Answer: the final answer to the original input question

YOU MUST GO THROUGH ALL OF THESE STEPS IN ORDER. DO NOT SKIP ANY STEPS. AND STRICTLY FOLLOW ALL THE NOTES ABOVE.

{example_workflow}

Begin!

Question: {question}
"""

        react_prompt = react_prompt.replace("{example_workflow}",self.example_workflow)
        react_prompt = react_prompt.replace("{prompt_string}",self.prompt_string)
        react_prompt = react_prompt.replace("{question}",self.question)

        return react_prompt