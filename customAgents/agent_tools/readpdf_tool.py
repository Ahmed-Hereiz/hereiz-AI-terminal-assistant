from typing import Any
import PyPDF2
from customAgents.agent_tools import BaseTool


class PDFDocReaderTool(BaseTool):
    def execute_func(self, pdf_path) -> str:
        
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text 
    


class PDFDocReaderSaverTool(PDFDocReaderTool):
    def execute_func(self, pdf_path, md_path) -> str:
        text = super().execute_func(pdf_path)

        with open(md_path, "w") as file:
            file.write("# PDF Content \n\n")
            file.write(text)

        print(f"Content Saved to {md_path}")