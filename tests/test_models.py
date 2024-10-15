from customAgents.agent_models import GradioClientModels
from customAgents.agent_tools import ModelInferenceTool


model = GradioClientModels(gradio_client_id="mukaist/DALLE-4k")
model_tool = ModelInferenceTool(model=model)
r = model_tool.execute_func("green yellow ai assistant chatbot robot")
print(r)
