class AgentPromptMeta(type):
    def __repr__(cls):
        return "<class 'customAgents.Prompt'>"

    def __str__(cls):
        return "<class 'customAgents.Prompt'>"

def agent_prompt_type(cls):
    return AgentPromptMeta(cls.__name__, cls.__bases__, dict(cls.__dict__))
