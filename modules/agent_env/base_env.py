from typing import List, Union, Any
from agent_runtime import BaseRuntime
from agent_routers import BaseRouter

AgentType = Union[BaseRuntime, BaseRouter]


class BaseEnv:
    def __init__(self, agents: List[AgentType]):

        self.agents = agents

    def run(self):
        """modify this in every class you create that inherit from BaseEnv"""
        for agent in self.agents:
            print(f"agent in the agents list : {agent}")

        raise NotImplementedError(f"Need to implement the run method first to specify how the env will work")
        

    def __str__(self) -> str:
        return f"agents in this env is {self.agents}"
    
    def __add__(self, other) -> Any:
        self.agents = self.agents + other.agents

    def __repr__(self) -> str:
        return f"agents in this env is {self.agents}"
    
