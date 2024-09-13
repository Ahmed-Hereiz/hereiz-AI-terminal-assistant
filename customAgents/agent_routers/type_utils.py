class AgentRoutersMeta(type):
    def __repr__(cls):
        return "<class 'customAgents.Routers'>"

    def __str__(cls):
        return "<class 'customAgents.Routers'>"

def agent_routers_type(cls):
    return AgentRoutersMeta(cls.__name__, cls.__bases__, dict(cls.__dict__))
