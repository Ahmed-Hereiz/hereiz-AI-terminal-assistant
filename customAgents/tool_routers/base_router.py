import time


class BaseRouter:
    def __init__(self, exec_after: float = 0):
        
        self.exec_after = exec_after
        
    def exec_router(self):

        time.sleep(self.exec_after)

        return "router executed !"
    
    def __str__(self) -> str:
        
        return f"router will execute after {self.exec_after}"
    
    def __repr__(self) -> str:
        
        return f"router will execute after {self.exec_after}"
    
    