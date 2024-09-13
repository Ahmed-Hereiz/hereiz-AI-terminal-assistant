import warnings
from typing import Dict
from customAgents.agent_runtime import BaseRuntime
from customAgents.agent_llm import BaseLLM
from customAgents.agent_prompt import BasePrompt
from customAgents.agent_tools import ToolKit


class ReActRuntime(BaseRuntime):
    def __init__(self, llm: BaseLLM, prompt: BasePrompt, toolkit: ToolKit):

        super().__init__(llm, prompt, toolkit)


    def step(self) -> str:
        response = super().step()
        return self._parse_response(response=response)
    
    def loop(self, agent_max_steps: int = 5) -> str:

        self.prompt.prompt = self.prompt.prompt.replace("{tool_names}",' '.join(self.toolkit.tool_names))
        self.prompt.prompt = self.prompt.prompt.replace("{tools_and_role}",self.toolkit.tool_instructions)
        

        for _ in range(agent_max_steps):

            print("\n")
            agent_response = self.step()

            if agent_response['Action'].lower() == 'finish':
                final_answer = agent_response['Final Answer']
                print("\n")
                return final_answer
            
            if agent_response['Action'] not in self.toolkit.tool_names:
                raise Exception(f"Unknown action: {agent_response['Action']}")

            tool_result = self.toolkit.execute_tool(agent_response['Action'], agent_response['Action Input'])
    
            if len(tool_result) == 0 or tool_result == None:
                warnings.warn("Tool is giving no results (Rerunning the loop again) please check the tools")
            
            self.prompt.prompt += f"Thought: {agent_response['Thought']}\nAction: {agent_response['Action']}\nAction Input: {agent_response['Action Input']}\nObservation: {tool_result}"

        return "Max iterations reached without finding an answer."
    

    def _parse_response(self, response: str) -> Dict[str, str]:
        parsed = {}
        current_key = None
        multiline_value = False

        for line in response.split('\n'):
            if ':' in line and not multiline_value:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                if key in ['Thought', 'Action', 'Action Input', 'Observation', 'Final Answer']:
                    current_key = key
                    if key == 'Action Input':
                        multiline_value = True
                        parsed[current_key] = value
                    else:
                        parsed[current_key] = value
            elif multiline_value and current_key == 'Action Input':
                parsed[current_key] += '\n' + line.strip()
                if line.strip().endswith('```'):
                    multiline_value = False
            elif current_key:
                parsed[current_key] += ' ' + line.strip()

        return parsed

