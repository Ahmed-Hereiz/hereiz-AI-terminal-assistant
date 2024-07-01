from typing import Any, Dict
from agent_runtime import BaseRuntime


class ReActRuntime(BaseRuntime):
    def __init__(self, llm: Any, prompt: Any, toolkit: Any):

        super().__init__(llm, prompt, toolkit)


    def step(self) -> str:
        response = super().step()
        return self._parse_response(response=response)
    
    def loop(self, agent_max_steps: int = 5) -> str:

        for _ in range(agent_max_steps):

            agent_response = self.step()
            print(agent_response)
            self.prompt.prompt += f"\n{agent_response}"
            extracted_json_response = self._extract_json_from_string(text=agent_response)

            if len(extracted_json_response) > 0:
                function_name = extracted_json_response[0]['function_name']
                function_params = extracted_json_response[0]['function_params']
                if function_name not in self.toolkit.tool_names:
                    raise Exception(f"Unknown action: {function_name}")

                tool_result = self.toolkit.execute_tool(function_params.values())
                result = f"\nAction_Response: {tool_result}"
                self.prompt.prompt += result
            else:
                break

        return agent_response
    

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

