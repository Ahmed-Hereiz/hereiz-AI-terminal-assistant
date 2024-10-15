from customAgents.agent_tools import PDFDocReaderTool


tool = PDFDocReaderTool(description="tool to read data inside in pdf",tool_name="pdf_tool")
r = tool.execute_func("cv.pdf")
print(r)