from modules.agent_tools import ToolKit, SearchTool, ScrapeLinkTool

search_tool = SearchTool(description="tool to search on the internet",tool_name="search tool")
scrape_tool = ScrapeLinkTool(description="tool to scrape some link",tool_name="scrape tool")

search_r = search_tool.execute_func("who is einstien")
scrape_r = scrape_tool.execute_func("https://example.com")

print(search_r)
print(scrape_r)

tools = ToolKit(tools=[search_tool,scrape_tool])
print(tools.tool_descriptions)
print(tools.tool_instructions)
print(tools.tool_names)

toolkit_search = tools.execute_tool("search tool","who is einstien")
toolkit_scrape = tools.execute_tool("scrape tool","https://example.com")

print(toolkit_search)
print(toolkit_scrape)
