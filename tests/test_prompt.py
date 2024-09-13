from customAgents.agent_prompt import ReActPrompt, PlaceHoldersPrompt, SimplePrompt

assert type(ReActPrompt(question=".").prompt) == str
assert type(PlaceHoldersPrompt().prompt) == str
assert type(SimplePrompt().prompt) == str

print("all assertions bassed")