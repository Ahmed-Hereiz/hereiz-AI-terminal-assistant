from agent_routers import ToolExecRouter
from agent_tools import SearchTool
from agent_env import SequentialEnv


tool = SearchTool(description="search internet",tool_name="search tool")
router = ToolExecRouter(tool=tool,exec_after=0)
env = SequentialEnv()


print(router.exec_router("who is albert einstien."))
