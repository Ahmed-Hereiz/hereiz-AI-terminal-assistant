import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from typing import Any
from modules.agent_tools import BaseTool

class PythonRuntimeTool(BaseTool):
    def execute_func(self, code: str) -> Any:
        return self._execute_code(code)
    
    def _execute_code(self, code: str) -> str:
        stdout = io.StringIO()
        stderr = io.StringIO()
        
        try:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exec(code)
            
            output = stdout.getvalue()
            errors = stderr.getvalue()
            
            if errors:
                return f"Errors:\n{errors}\nOutput:\n{output}"
            else:
                return f"Output:\n{output}"
        except Exception as e:
            return f"Exception: {str(e)}"

# Usage:
# tool = PythonRuntimeTool()
# result = tool.execute_func("print('Hello, World!')\nfor i in range(5): print(i)")
# print(result)
