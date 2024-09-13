class AgentModelsMeta(type):
    def __repr__(cls):
        return "<class 'customAgents.Models'>"

    def __str__(cls):
        return "<class 'customAgents.Models'>"

def agent_models_type(cls):
    return AgentModelsMeta(cls.__name__, cls.__bases__, dict(cls.__dict__))
