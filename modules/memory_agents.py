from customAgents.agent_llm import BaseLLM, BaseMultiModal
from customAgents.agent_prompt import BasePrompt
from customAgents.runtime import BaseRuntime
from customAgents.env import BaseEnv
from customAgents.agent_tools import BashRuntimeTool
import os


class MemoryLLM(BaseLLM):
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings=None):
        super().__init__(api_key, model, temperature, safety_settings)

    def llm_generate(self, input: str) -> str:
        return super().invoke_response(input)
    

class MemoryPrompt(BasePrompt):
    def __init__(self, user_question: str, memory: str, prompt_string: str = ""):
        super().__init__(prompt_string)

        self.prompt = """
You are tasked with summarizing the conversation and categorizing important information into long-term and short-term memory. Follow these guidelines carefully:

**Long-term memory** should store key information about the user and essential details from previous interactions. Focus on recurring, critical facts such as:

- User's name (if provided)
- Preferences (e.g., favorite topics, hobbies, communication style)
- Goals and significant personal insights (e.g., profession, long-term objectives)
- Major interactions or repeated behavior patterns and requests
- Any information that should be retained for future interactions beyond this conversation

**Short-term memory** provides a concise summary of the current conversation, focusing on:

- Questions or queries the user asked during this session
- Specific requests or instructions given by the user
- Temporary or situation-specific details that may change or become irrelevant over time
- Information relevant only to the current session but not necessarily important for future conversations

Your task is to take the previous memory and combine it with the user's new conversation. Then, update the memory by organizing the information into two distinct sections: long-term and short-term.
Note that at the first chat you may take empty memory you have to consruct from scratch if so.

Ensure that:
- **Long-term memory** contains all critical and recurring details that are important for future interactions.
- **Short-term memory** holds temporary or session-specific information that may not be relevant after this conversation.

Summarize and organize both sections clearly and concisely, and strictly follow these instructions.

The Previous Memory:
{memory}

Current Conversation:

user query : {user_question}
query response : {answer}

"""

        self.prompt = self.prompt.replace("{memory}",memory)
        self.prompt = self.prompt.replace("{user_question}",user_question)


class MemoryAgent(BaseRuntime):
    def __init__(self, llm: BaseLLM, prompt: BasePrompt):
        super().__init__(llm, prompt, toolkit=[])

    def step(self) -> str:
        return super().step()
    
    def loop(self, n_steps: int = 1) -> str:
        return super().loop(n_steps)


class MemoryReflectionEnv(BaseEnv):
    def __init__(self, agents):
        if len(agents) != 2:
            raise ValueError("Memory Agent class must be initialized with exactly 2 agents.")
        super().__init__(agents=agents,routers=None)

    def run(self):
        chat_agent = self.agents[0]
        memory_agent = self.agents[1]

        chat_response = chat_agent.loop()
        memory_agent.prompt.prompt = memory_agent.prompt.prompt.replace("{answer}",chat_response)
        new_memory = memory_agent.loop()

        return chat_response, new_memory
    

class ScreenMemoryLLM(BaseMultiModal):
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings=None):
        super().__init__(api_key, model, temperature, safety_settings)

    def multimodal_generate(self, prompt, img, stream=True):
        return super().multimodal_generate(prompt, img, stream, output_style="visual")

class ScreenMemoryPrompt(BasePrompt):
    def __init__(self, user_question, img, memory):
        super().__init__(prompt_string="", img=img)
        self.prompt = """
You are Hereiz, a friendly and helpful AI assistant. Your role is to chat with users, provide assistance, and offer thoughtful, personalized support. You are skilled in multiple areas, including programming, data science, machine learning, science, and math.

**Current Context:**
- You can see what the user is currently doing, which may provide important context for their query.
- Based on the current response, suggest next steps or actions that could help the user.

Current Context:
{memory}

Current Conversation:

user query : {user_question}
query response : {answer}

"""
        self.prompt = self.prompt.replace("{memory}", memory)
        self.prompt = self.prompt.replace("{user_question}", user_question)

class ScreenMemoryAgent(BaseRuntime):
    def __init__(self, llm: ScreenMemoryLLM, prompt: ScreenMemoryPrompt):
        super().__init__(llm, prompt, toolkit=[])

    def step(self) -> str:
        return super().step()
    
    def loop(self, n_steps: int = 1) -> str:
        return super().loop(n_steps)


class ScreenMemorySeqEnv(BaseEnv):
    def __init__(self, agents):
        if len(agents) != 2:
            raise ValueError("Memory Agent class must be initialized with exactly 2 agents.")
        super().__init__(agents=agents,routers=None)

    def run(self):
        screen_agent = self.agents[0]
        memory_screen_agent = self.agents[1]

        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

        get_screen = BashRuntimeTool()
        cap_screen_file = f"{root_dir}/hereiz_screen.sh"
        output_screen_dir = f"{root_dir}/data/tmp/"

        get_screen.execute_func(code=f"bash {cap_screen_file} {output_screen_dir}")
        
        screen_response = screen_agent.loop()
        memory_screen_agent.prompt.prompt = memory_screen_agent.prompt.prompt.replace("{answer}",screen_response)
        new_memory = memory_screen_agent.loop()

        return screen_response, new_memory
