from customAgents.agent_llm import BaseLLM
from customAgents.agent_prompt import ReActPrompt
from customAgents.agent_runtime import ReActRuntime
from customAgents.agent_tools import (
    ToolKit,
    SearchTool,
    PythonRuntimeTool,
    ScrapeDynamicLinkTool,
    ModelInferenceTool,
    PDFDocReaderTool
)

from modules.generate_agents import txt2imgModel, sketch2imgModel

class MainLLM(BaseLLM):
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings=None):
        super().__init__(api_key, model, temperature, safety_settings)

    def llm_generate(self, input: str) -> str:
        return super().generate_response(input,output_style="green")


class MainPrompt(ReActPrompt):
    def __init__(self, question: str, memory: str):

        self.memory = memory

        super().__init__(question, example_workflow="", prompt_string="")

        self.example_workflow = """
Question: What is the date today ?

[you in iteration 1]
Thought: I have to search for the day today using the internet to get a good resault.
Action: search tool
Action Input: today's date

[you then STOP the first iteration after this]


... (not generated by AI it comes as from a software code) Observation: [the tool will return the today's date to you so you have to read the observation carefully to answer in the next step using it (you don't generate observation it just comes to you)]

[you in iteration 2]
Thought: from the previous Observation I can find good and specific information that can answer the user original question which is "What is the date today ?"
Action: finish
Final Answer: Today's date is... [if there is more to describe to make chat more user friendly do it]


Question: What is the product of 22 and 33 ?

[you in iteration 1]
Thought: I have to use python code to find the answer
Action: python tool
Action Input: 
```python

print(22*33)

```

[you then STOP the first iteration after this]

[you in iteration 2]
Thought: from the previous Observation I can find good and specific information that can answer the user original question which is "what is the product of 22 and 33"
Action: finish
Final Answer: the product of 22 * 33 is 726 [if there is more to describe to make chat more user friendly do it]

"""

        self.prompt = """
You are Hereiz, a friendly and helpful AI assistant. 
You are here to chat with people, provide assistance, and be a good friend. 
You are knowledgeable in various areas like programming, data science, machine learning, science, and math.
Your main goal is to have engaging and meaningful conversations while always being aware of the user's preferences, past interactions, and goals.

Identity:
- When someone asks who you are, you say that you are a friend who talks with people.
- When someone asks for your name, you say that your name is Hereiz.

Memory:
- Always reference both **long-term memory** and **short-term memory** to maintain context and provide relevant responses.
  - **Long-term memory** contains key information about the user from previous interactions, such as their name, preferences, and important topics or goals. Use this memory to make the conversation more personalized and show that you remember what's important to the user.
  - **Short-term memory** focuses on the current conversation and session-specific details. Use this memory to stay on track with the current topic and handle session-based questions or requests.

Approach:
- While answering you have to follow the ReAct loop paradigm bellow don't ever ignore the Though, Action, Action Input etc..
- Always prioritize answering the user's questions directly and accurately.
- After answering, if clarification is needed or if more information would improve the conversation, ask follow-up questions to gather more details.
- Don't try to end the chat with clarification alone; always provide a thoughtful answer and ask a follow-up if needed.
- If you don't know the answer to a question, admit that you don't know. Always prioritize being transparent and helpful.
- You also have access to various tools to help you provide more detailed or calculated responses. Use these tools iteratively to gather additional information when necessary.

Conversation Memory:

{history}

You are designed to answer questions through an iterative process. You have access to the following tools:
{tools_and_role}

IMPORTANT: You will determine whether you need to use a tool or answer the question based on your current knowledge. You will go through multiple steps before reaching a final answer if needed.

Follow this format EXACTLY for each step:

1. Decide whether to use a tool or answer directly:
Thought: [Your reasoning on whether you need to use tools or can answer based on current knowledge]
Action: [One of: "finish" OR one of {tool_names}]
Action Input: [Python list of inputs for the chosen action, if there is action choosen]

2. If you choose to use a tool:
- Do not generate "Observation" text. Observations will be provided to you after each action.
- Start a new iteration with a new Thought after receiving each observation.
- Use ONLY information from observations. Do not use external knowledge or assumptions.
- Keep gathering information until you are CERTAIN you have everything you need.

3. When you are CERTAIN you can answer the question:
Thought: I now have all the information to answer the question
Action: finish
Final Answer: [Your detailed answer, referencing specific observations or past memory if applicable]

RULES:
- You can only use the "finish" action when you are certain you have all necessary information.
- Be thorough and accurate, use tools and memory as needed to ensure the best result.
- Always be polite, friendly, and engaging, adding personal touches to your responses.
- Don't forget you have to always show the Thought and Action even if it is direct question.
- If you chose to use tools you have to answer based on the tool results and never make answer, only if you found it's results was not good after many iterations, you can then clarrify it don't have the answer and tell your answer if you know clarrifying that it is yours.


Example workflow:
{example_workflow}

Let's begin!

Question: {question}
"""

        self.prompt = self.prompt.replace("{history}",self.memory)
        self.prompt = self.prompt.replace("{example_workflow}",self.example_workflow)
        self.prompt = self.prompt.replace("{question}",question)


class MainAgent(ReActRuntime):
    def __init__(self, llm, prompt):

        txt2imge_model = txt2imgModel(saved_imgs_dir="output/Imgs",gradio_client_id="mukaist/DALLE-4k")
        sketch2img_model = sketch2imgModel(saved_imgs_dir="output/sketches")

        search_tool = SearchTool(description="tool that can search internet (each query you input will get different search) Note that it accepts only one param",tool_name="search_tool")
        python_tool = PythonRuntimeTool(description="tool that can run python code (give the code for this function as md format)",tool_name="python_tool")
        scrape_tool = ScrapeDynamicLinkTool(description="tool used to scrape provided links and get content (Note while passing the link make sure the link is correct and it takes one param at the time and in form of plain link text without '' or list) if you got the content don't use it again (Please notice after you use this tool and get results make sure you read the results well from it, no need to use it again with same link in 2 consecutive iterations) make sure to input the link as it is without adding spaces to it",tool_name="scrape_tool",max_num_chars=10000)
        readpdf_tool = PDFDocReaderTool(description="tool used to read text inside a pdf documment, input param is single unquoted pdf path not found in list just plain text",tool_name="readpdf_tool")
        img2txt_tool = ModelInferenceTool(description="tool used to use text to image model (take input as single text prompt without list or '' in between) Note once the tool finish generation you will get message of where the output is found you have to tell the user the where the output dir is and stop also if you didn't get any output from the tool confirming it genrated rerun the tool some times if still no output clarify that there is problem with the tool",tool_name="image_to_text_tool",model=txt2imge_model)
        sketch2img_tool = ModelInferenceTool(description="This tool is designed to convert a user's sketch and prompt into a refined image. (if you found in the prompt that the user want to draw or make sketch activate it) When the user expresses the intent to create a sketch, the tool will take a single input: a clear and detailed text prompt describing the desired modifications or enhancements to the sketch. The prompt should be provided as plain text (not using quotes or an input list). Once the image generation is complete, the tool will return the directory where the final image, refined from the user's sketch, is saved.",tool_name="sketch_to_image_tool",model=sketch2img_model)
        toolkit = ToolKit(tools=[search_tool,python_tool,scrape_tool,readpdf_tool,img2txt_tool,sketch2img_tool])

        super().__init__(llm, prompt, toolkit=toolkit)

    def loop(self, agent_max_steps: int = 10) -> str:
        return super().loop(agent_max_steps, verbose_tools=True)