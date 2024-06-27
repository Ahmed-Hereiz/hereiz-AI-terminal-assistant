from agent_prompt import PlaceHoldersPrompt


class ReActPrompt(PlaceHoldersPrompt):
    def __init__(self, tools_and_roles: str, example_workflow: str, final_output: str, placeholders: dict = {}, prompt_string: str = ""):
        
        self.tools_and_roles = tools_and_roles
        self.example_workflow = example_workflow
        self.final_output = final_output

        super().__init__(placeholders, prompt_string)


    def _generate_prompt(self):

        react_prompt = """
You operate in a loop of Thought, Action, PAUSE, and Action_Response. At the end of the loop, you output an Answer.

Use Thought to understand the task you have been given.
Use Action to execute one of the available actions, then return PAUSE.
Action_Response will be the result of executing those actions.

{prompt_string}
{tools_and_role}

Instructions:
1. Identify and gather all necessary information based on the task.
2. Use the provided tools to collect data or perform actions as needed.
3. Ensure that the output is concise, relevant, and meets the specified goal.

{example_workflow}

You then output:
{final_output}
"""

        react_prompt.replace("{tools_and_role}",self.tools_and_roles)
        react_prompt.replace("{example_workflow}",self.example_workflow)
        react_prompt.replace("{final_output}",self.final_output)
        react_prompt.replace("{prompt_string}",self.prompt_string)

        for replace in self.placeholders.keys():
            react_prompt = react_prompt.replace(replace,self.placeholders[replace])


        return react_prompt
    



class ReActPromptModified(PlaceHoldersPrompt):
    def __init__(self, tools_and_roles: str, example_workflow: str, final_output: str, placeholders: dict = {}, prompt_string: str = ""):
        
        self.tools_and_roles = tools_and_roles
        self.example_workflow = example_workflow
        self.final_output = final_output

        super().__init__(placeholders, prompt_string)


    def _generate_prompt(self):

        react_prompt = """
{prompt_string}
Answer the following questions as best you can. You have access to the following tools:
{tools_and_role}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

{example_workflow}

Begin!

Question: 
"""

        react_prompt.replace("{tools_and_role}",self.tools_and_roles)
        react_prompt.replace("{example_workflow}",self.example_workflow)
        react_prompt.replace("{final_output}",self.final_output)
        react_prompt.replace("{prompt_string}",self.prompt_string)

        for replace in self.placeholders.keys():
            react_prompt = react_prompt.replace(replace,self.placeholders[replace])


        return react_prompt