from typing import Any
from agent_routers import BaseRouter


class ConditionalRouter(BaseRouter):
    def __init__(self, condition: Any, perform: Any, exec_after: float = 0):
        super().__init__(exec_after)

        self.condition = condition
        self.perform = perform


    def exec_router(self, check_on):
        """
        It's prefered to use this router as base and make other routers that inherit from it.
        use it to make more routers that checks some conditions like type, size,outputs,etc...
        """

        if check_on == self.condition:
            return self.perform
        

