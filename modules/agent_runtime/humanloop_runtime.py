from typing import Any
from agent_runtime import BaseRuntime


class HumanLoopRuntime(BaseRuntime):
    def __init__(self, llm: Any, prompt: Any):
        super().__init__(llm=llm, prompt=prompt, tools=[])


    def step(self) -> str:
        return super().step()
    
    def loop(self, activate_loop=True) -> str:
        
        while activate_loop:
            print(self.prompt.prompt)
            self.prompt.prompt += self.step()

            if activate_loop:
                human_feedback = input("\n\nEnter feedback (or 'exit' to end loop): ")

                if human_feedback.lower() == 'exit':
                    activate_loop = False
                else:
                    self.prompt.prompt += f"\n\n### Feedback\n{human_feedback}\n"

