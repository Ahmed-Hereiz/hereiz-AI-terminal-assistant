import json
from typing import Any
from agent_runtime import BaseRuntime


class ReActRuntime(BaseRuntime):
    def __init__(self, llm: Any, prompt: Any, toolkit: Any):

        super().__init__(llm, prompt, toolkit)


    def step(self) -> str:
        return super().step()
    
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


    def _extract_json_from_string(self, text: str):

        json_objects = []
        brace_stack = []
        json_str = ""
        inside_json = False

        for _, char in enumerate(text):
            if char == '{':
                brace_stack.append(char)
                inside_json = True
            if inside_json:
                json_str += char
            if char == '}':
                brace_stack.pop()
                if not brace_stack:
                    inside_json = False
                    try:
                        json_object = json.loads(json_str)
                        json_objects.append(json_object)
                    except json.JSONDecodeError:
                        pass
                    json_str = ""

        return json_objects