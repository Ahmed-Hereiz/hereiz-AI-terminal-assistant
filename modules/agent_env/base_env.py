from typing import List, Union, Any
from agent_runtime import BaseRuntime
from agent_routers import BaseRouter

AgentType = Union[BaseRuntime, BaseRouter]


class BaseEnv:
    def __init__(self, env_runs: List[AgentType]):

        self.env_runs = env_runs

    def run(self):
        """modify this in every class you create that inherit from BaseEnv"""
        for env_run in self.env_runs:
            print(f"agent in the agents list : {env_run}")

        raise NotImplementedError(f"Need to implement the run method first to specify how the env will work")
        

    def __str__(self) -> str:
        return f"agents or routers in this env is {self.env_run}"
    
    def __add__(self, other) -> Any:
        self.env_runs = self.env_runs + other.env_runs

    def __repr__(self) -> str:
        return f"agents or routers in this env is {self.env_runs}"
    
