class AgentRuntimeMeta(type):
    def __repr__(cls):
        return "<class 'customAgents.Runtime'>"

    def __str__(cls):
        return "<class 'customAgents.Runtime'>"

def agent_runtime_type(cls):
    return AgentRuntimeMeta(cls.__name__, cls.__bases__, dict(cls.__dict__))
