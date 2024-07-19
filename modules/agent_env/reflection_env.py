from typing import List
from modules.agent_env import BaseEnv

class ReflectionEnv(BaseEnv):
    def __init__(self, agents):
        if len(agents) != 2:
            raise ValueError("Reflection class must be initialized with exactly 2 agents.")
        super().__init__(agents)

    def run(self, num_max_iters=3):
        agent1 = self.agents[0]
        agent2 = self.agents[1]

        for _ in range(num_max_iters):
            print("Agent 1 : ")
            agent1_response = agent1.loop()
            print("\n\n")
            print("Agent 2 : ")
            agent2.prompt.prompt += agent1_response
            agent2_response = agent2.loop()
            agent1.prompt.prompt += agent2_response
            print("\n")

            if agent2_response == "0":
                break

        return agent1_response, agent2_response

    @property
    def agent1(self):
        return self.agents[0]

    @property
    def agent2(self):
        return self.agents[1]