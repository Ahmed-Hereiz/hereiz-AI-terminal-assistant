from typing import Any
from agent_routers import BaseRouter


class ConditionalRouter(BaseRouter):
    def __init__(self, condition: Any, perform: Any, exec_after: float = 0):
        super().__init__(exec_after)

        self.condition = condition
        self.perform = perform


    def exec_router(self, check_on):

        if check_on == self.condition:
            return self.perform