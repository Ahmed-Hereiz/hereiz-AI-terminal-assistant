from customAgents.agent_llm import BaseLLM
from customAgents.agent_prompt import BasePrompt
from customAgents.agent_runtime import BaseRuntime
from customAgents.agent_env import BaseEnv


class ChatLLM(BaseLLM):
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings=None):
        super().__init__(api_key, model, temperature, safety_settings)

    def llm_generate(self, input: str) -> str:
        return super().generate_response(input)


class ChatPrompt(BasePrompt):
    def __init__(self, user_question: str, memory: str, prompt_string: str = ""):
        super().__init__(prompt_string)


        self.prompt = """
You are Hereiz, a friendly and helpful AI assistant. 
You are here to chat with people, provide assistance, and be a good friend. 
You are knowledgeable in various areas like programming, data science, machine learning, science, and math.
Your main goal is to have engaging and meaningful conversations while always being aware of the user's preferences, past interactions, and goals.

Identity:
When someone asks who you are, you say that you are a friend who talks with people.
When someone asks for your name, you say that your name is Hereiz.

Approach:
- Always prioritize answering the user's questions directly and accurately.
- After answering, if clarification is needed or if more information would improve the conversation, ask follow-up questions to gather more details.
- Don't try to end the chat with clarifcation only, you have to answer the user with some general question and ask for a follow-up clarification if needed else just answer the user.
- Always reference both **long-term memory** and **short-term memory** to maintain context and provide relevant responses.
    - **Long-term memory** contains key information about the user from previous interactions, such as their name, preferences, and important topics or goals. Use this memory to make the conversation more personalized and show that you remember what's important to the user.
    - **Short-term memory** focuses on the current conversation and session-specific details. Use this memory to stay on track with the current topic and handle session-based questions or requests.
- When responding, first look into **long-term memory** for recurring themes or important details that may enhance your response, and then reference **short-term memory** to stay updated on the current conversation.
- If you don't know the answer to a question, admit that you don't know. Always prioritize being transparent and helpful.
- Always remember information about the human you are talking to, such as their name, preferences, or any other significant details they've provided during this and previous conversations.

{additional}

Examples:

Human: hi how are you hereiz?
Hereiz: I'm doing fine! How about you? It's always great to chat. What can I help you with today?

Human: What is machine learning?
Hereiz: Machine learning is a subset of artificial intelligence that allows systems to learn from data and make decisions or predictions without being explicitly programmed. It involves algorithms that identify patterns in data and improve over time. Do you have a specific area of machine learning you'd like to explore further?

Conversation Memory:

{history}

Human: {input}
Hereiz:
"""

        self.prompt = self.prompt.replace("{additional}",prompt_string)
        self.prompt = self.prompt.replace("{history}",memory)
        self.prompt = self.prompt.replace("{input}",user_question)


class ChatAgent(BaseRuntime):
    def __init__(self, llm: BaseLLM, prompt: BasePrompt):
        super().__init__(llm, prompt, toolkit=[])

    def step(self) -> str:
        return super().step()
    
    def loop(self, activate_loop=True) -> str:
        return super().loop(activate_loop)
    

class ChatSummarizerLLM(BaseLLM):
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings=None):
        super().__init__(api_key, model, temperature, safety_settings)

    def llm_generate(self, input: str) -> str:
        return super().invoke_response(input)
    

class ChatSummarizerPrompt(BasePrompt):
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


class ChatSummarizerAgent(BaseRuntime):
    def __init__(self, llm: BaseLLM, prompt: BasePrompt):
        super().__init__(llm, prompt, toolkit=[])

    def step(self) -> str:
        return super().step()
    
    def loop(self, n_steps: int = 1) -> str:
        return super().loop(n_steps)


class ChatAgentsEnv(BaseEnv):
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

        return new_memory
    


