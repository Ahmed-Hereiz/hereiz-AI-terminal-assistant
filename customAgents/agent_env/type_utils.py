class AgentEnvMeta(type):
    def __repr__(cls):
        return "<class 'customAgents.Env'>"

    def __str__(cls):
        return "<class 'customAgents.Env'>"

def agent_env_type(cls):
    return AgentEnvMeta(cls.__name__, cls.__bases__, dict(cls.__dict__))
