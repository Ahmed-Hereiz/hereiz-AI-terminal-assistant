from typing import List, Any
from customAgents.runtime import BaseRuntime
from customAgents.tool_routers import BaseRouter


class BaseEnv:
    def __init__(self, agents: List[BaseRuntime], routers: List[BaseRouter] = None):

        self.agents = agents
        self.routers = routers

    def run(self):
        """modify this in every class you create that inherit from BaseEnv"""
        for agent in self.agents:
            print(f"agent in the agents list : {agent}")

        raise NotImplementedError(f"Need to implement the run method first to specify how the env will work")
        

    def __str__(self) -> str:
        return f"agents in this env is {self.agents}, routers in this env is {self.routers}"
    
    def __add__(self, other) -> Any:
        self.agents = self.agents + other.agents
        self.routers = self.routers + other.routers

    def __repr__(self) -> str:
        return f"agents in this env is {self.agents}, routers in this env is {self.routers}"

