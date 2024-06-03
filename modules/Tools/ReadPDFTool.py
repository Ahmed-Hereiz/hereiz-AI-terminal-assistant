import PyPDF2
from utils import add_root_to_path
hereiz_root = add_root_to_path()

from modules.Tools import ToolBase

class PDFDocReader(ToolBase):
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text_from_pdf(self):
        text = ""
        with open(self.pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text

    def save_as_markdown(self, text, md_path):
        with open(md_path, "w") as file:
            file.write("# PDF Content\n\n")
            file.write(text)
        print(f"Content saved to {md_path}")


