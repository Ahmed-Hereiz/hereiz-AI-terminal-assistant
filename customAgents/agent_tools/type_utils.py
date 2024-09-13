class AgentToolsMeta(type):
    def __repr__(cls):
        return "<class 'customAgents.Tools'>"

    def __str__(cls):
        return "<class 'customAgents.Tools'>"

def agent_tools_type(cls):
    return AgentToolsMeta(cls.__name__, cls.__bases__, dict(cls.__dict__))
