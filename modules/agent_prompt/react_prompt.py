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
You are an AI agent designed to answer questions through an iterative process. You have access to the following tools:
{tools_and_role}

IMPORTANT: This is an ITERATIVE PROCESS. You will go through multiple steps before reaching a final answer. Do not try to answer the question immediately.

Follow this format EXACTLY for each iteration:
Thought: [Your reasoning about the current state and what to do next]
Action: [One of: {tool_names}]
Action Input: [Python list of for the action (you make one action Input each iteration)]

CRITICAL RULES:
1. You operate in a loop. Each iteration, you provide ONLY Thought, Action, and Action Input.
2. DO NOT generate "Observation" text. Observations will be provided to you after each action.
3. After each observation, start a new iteration with a new Thought.
4. Use ONLY information from observations. Do not use external knowledge or assumptions.
5. You may need multiple iterations to gather enough information. Be patient and thorough.
6. Do NOT try to provide a final answer until you are absolutely certain you have all necessary information.
7. You Should Have good reasoning ability while thought so if there is inderect question you can use math to solve for it.

When you are CERTAIN you have ALL information needed to answer the original question:
Thought: I now have all the information to answer the question
Action: finish
Final Answer: [Your detailed answer, referencing specific observations]

Remember:
- You CANNOT provide a final answer without using the "finish" action.
- Always wait for an observation after each action before starting a new iteration.
- If an observation is unclear or insufficient, use your next action to clarify or gather more information.
- Your goal is to be thorough and accurate, not quick. Take as many iterations as needed use tools as much time as you need to get the best result.

Example workflow:
{example_workflow}

Let's begin!

Question: {question}
"""

        react_prompt = react_prompt.replace("{example_workflow}",self.example_workflow)
        react_prompt = react_prompt.replace("{prompt_string}",self.prompt_string)
        react_prompt = react_prompt.replace("{question}",self.question)

        return react_prompt