from typing import Any, Dict
from modules.agent_runtime import BaseRuntime


class ReActRuntime(BaseRuntime):
    def __init__(self, llm: Any, prompt: Any, toolkit: Any):

        super().__init__(llm, prompt, toolkit)


    def step(self) -> str:
        response = super().step()
        return self._parse_response(response=response)
    
    def loop(self, agent_max_steps: int = 5) -> str:

        
        self.prompt.prompt = self.prompt.prompt.replace("{tool_names}",*self.toolkit.tool_names)
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
            self.prompt.prompt += f"Thought: {agent_response['Thought']}\nAction: {agent_response['Action']}\nAction Input: {agent_response['Action Input']}\nObservation: {tool_result[0]['content']}"

        return "Max iterations reached without finding an answer."
    

    def _parse_response(self, response: str) -> Dict[str, str]:
        parsed = {}
        current_key = None
        for line in response.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if key in ['Thought', 'Action', 'Action Input', 'Observation', 'Final Answer']:
                    current_key = key
                    parsed[current_key] = value
            elif current_key:
                parsed[current_key] += ' ' + line.strip()
        return parsed

