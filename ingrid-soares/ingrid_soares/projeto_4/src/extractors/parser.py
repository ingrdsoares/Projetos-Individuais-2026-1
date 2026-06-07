import fitz  # PyMuPDF
from pathlib import Path
from typing import List

class PDFParser:
    def to_markdown(self, file_path: Path) -> str:
        """Converts PDF to a full markdown representation (Full-Scan)."""
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
        return "

".join(markdown_text)

    def get_semantic_chunks(self, file_path: Path, keywords: List[str] = None) -> List[str]:
        """
        Implements Semantic Chunking. 
        Divides the document into blocks based on keywords and headers, 
        returning only chunks relevant to the extraction.
        """
        if keywords is None:
            keywords = ["Resultados", "Balanço", "Financeiro", "Operacional", "Métricas", "Vendas"]
        
        full_text = self.to_markdown(file_path)
        # Split by page markers or logical sections
        pages = full_text.split("---")
        semantic_chunks = []
        
        for page in pages:
            # Keep the page if it contains any of the key semantic markers
            if any(kw.lower() in page.lower() for kw in keywords):
                semantic_chunks.append(page.strip())
        
        # Fallback: if no semantic chunks found, return first 3 pages (Full-Scan Lite)
        if not semantic_chunks:
            return pages[:3]
            
        return semantic_chunks

if __name__ == "__main__":
    try:
        parser = PDFParser()
        path = Path("projeto-individual-4/exemplo_Boletim_Conjuntura_2025_3T.pdf")
        print("--- Full Scan (first 500 chars) ---")
        print(parser.to_markdown(path)[:500])
        print("
--- Semantic Chunks Count ---")
        print(f"Chunks found: {len(parser.get_semantic_chunks(path))}")
    except Exception as e:
        print(f"Error: {e}")
