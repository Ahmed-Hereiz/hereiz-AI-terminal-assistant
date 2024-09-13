from customAgents.agent_llm import BaseLLM, SimpleInvokeLLM, SimpleStreamLLM
from customAgents.agent_prompt import BasePrompt, PlaceHoldersPrompt, SimplePrompt, ReActPrompt

llm1 = BaseLLM(api_key='dummy',model='gemini-pro',temperature=0.7)
llm2 = SimpleInvokeLLM(api_key='dummy',model='gemini-pro',temperature=0.7)
llm3 = SimpleStreamLLM(api_key='dummy',model='gemini-pro',temperature=0.7)
print(type(llm1))
print(type(llm2))
print(type(llm3))

prompt1 = BasePrompt()
prompt2 = PlaceHoldersPrompt()
prompt3 = SimplePrompt()
prompt4 = ReActPrompt(question="dummy")
print(type(prompt1))
print(type(prompt2))
print(type(prompt3))
print(type(prompt4))