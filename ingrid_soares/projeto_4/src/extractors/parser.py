import fitz  # PyMuPDF
from pathlib import Path

class PDFParser:
    def to_markdown(self, file_path: Path) -> str:
        doc = fitz.open(file_path)
        markdown_text = []
        for page_num, page in enumerate(doc):
            markdown_text.append(f"## Page {page_num + 1}")
            tabs = page.find_tables()
            if tabs:
                for tab in tabs:
                    markdown_text.append(tab.to_pandas().to_markdown(index=False))
            text = page.get_text("text")
            markdown_text.append(text)
            markdown_text.append("---")
        doc.close()
        return "\n\n".join(markdown_text)

if __name__ == "__main__":
    try:
        parser = PDFParser()
        print(parser.to_markdown(Path("projeto-individual-4/exemplo_Boletim_Conjuntura_2025_3T.pdf"))[:500])
    except Exception as e:
        print(f"Error: {e}")
