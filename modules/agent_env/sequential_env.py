from typing import List
from agent_env import BaseEnv

class SequentialEnv(BaseEnv):
    def __init__(self, agents):
        if len(agents) < 2:
            raise ValueError("SequentialEnv class needs at least 2 or more agents to work")
        super().__init__(agents)

    def run(self, initial_input: str=""):

        current_input = initial_input

        for agent in self.agents:
            
            agent.prompt.prompt += current_input
            current_input = agent.loop()

        return current_input


    def get_agent(self, index: int):
        """
        Returns the agent at the specified index.

        :param index: The index of the agent to retrieve.
        :return: The agent at the specified index.
        :raises IndexError: If the index is out of range.
        """
        return self.agents[index]