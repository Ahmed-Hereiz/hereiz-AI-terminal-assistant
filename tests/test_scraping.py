from customAgents.agent_tools import ScrapeDynamicLinkTool

s = ScrapeDynamicLinkTool(description="tool to scrape")
r = s.execute_func(url="https://www.spaceappschallenge.org/nasa-space-apps-2024/challenges/globe-protocol-games/?tab=details")