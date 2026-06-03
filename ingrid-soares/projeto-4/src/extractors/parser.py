import fitz  # PyMuPDF
from pathlib import Path

class PDFParser:
    """
    Extracts text from PDF files and prepares it for LLM consumption.
    """
    @staticmethod
    def to_markdown(file_path: Path) -> str:
        """
        Converts PDF content to a Markdown-like text format.
        Focuses on preserving the sequence of text and basic table structures.
        """
        doc = fitz.open(file_path)
        markdown_text = []
        
        for page_num, page in enumerate(doc):
            markdown_text.append(f"## Page {page_num + 1}")
            
            # Try to extract tables first
            tabs = page.find_tables()
            if tabs:
                for tab in tabs:
                    # Convert table to Markdown format
                    df = tab.to_pandas()
                    markdown_text.append(df.to_markdown(index=False))
            
            # Extract regular text
            text = page.get_text("text")
            markdown_text.append(text)
            markdown_text.append("
---
")
            
        doc.close()
        return "

".join(markdown_text)

if __name__ == "__main__":
    # Test with the example file provided in project-individual-4
    try:
        parser = PDFParser()
        content = parser.to_markdown(Path("projeto-individual-4/exemplo_Boletim_Conjuntura_2025_3T.pdf"))
        print(content[:1000])
    except Exception as e:
        print(f"Error: {e}")
