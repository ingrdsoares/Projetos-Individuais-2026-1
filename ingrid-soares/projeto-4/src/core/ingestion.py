import hashlib
import requests
from pathlib import Path
from typing import List, Dict
from src.database.database import init_db, register_document, get_processed_hashes
from src.extractors.scrapers import RIScraper

class IngestionPipeline:
    """
    Orchestrates the collection of RI PDFs and ensures idempotency.
    """
    def __init__(self, storage_dir: str = "data/pdfs"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        init_db()

    def calculate_hash(self, content: bytes) -> str:
        """Calculates SHA-256 hash of a file content."""
        return hashlib.sha256(content).hexdigest()

    def download_pdf(self, url: str, filename: str) -> Path:
        """Downloads a PDF from a URL and saves it locally."""
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        
        file_path = self.storage_dir / filename
        with open(file_path, "wb") as f:
            f.write(response.content)
        
        return file_path

    def process_company(self, company_name: str, base_url: str):
        """
        Pipeline for a single company: Scrape -> Download -> Hash Check -> Register.
        """
        print(f"Processing company: {company_name}...")
        scraper = RIScraper(company_name, base_url)
        pdf_links = scraper.find_pdf_links()
        
        processed_hashes = get_processed_hashes()
        new_docs_count = 0

        # Demo Mode: If no PDFs found (likely due to server issues), simulate discovery of local files
        if not pdf_links:
            # Try to find a simulated file in the storage dir for this company
            simulated_files = list(self.storage_dir.glob(f"*{company_name}*.pdf"))
            if simulated_files:
                for file_path in simulated_files:
                    with open(file_path, "rb") as f:
                        content = f.read()
                        file_hash = self.calculate_hash(content)
                    
                    if file_hash not in processed_hashes:
                        # Register as if it were just found online
                        doc_id = register_document(company_name, f"simulated://{file_path.name}", file_hash, file_path.name)
                        if doc_id:
                            print(f"  [Success] Local document registered: {file_path.name} (ID: {doc_id})")
                            new_docs_count += 1
        else:
            for filename, url in pdf_links:
                try:
                    response = requests.get(url, timeout=20)
                    response.raise_for_status()
                    content = response.content
                    file_hash = self.calculate_hash(content)
                    if file_hash in processed_hashes:
                        continue
                    file_path = self.storage_dir / filename
                    with open(file_path, "wb") as f:
                        f.write(content)
                    doc_id = register_document(company_name, url, file_hash, filename)
                    if doc_id:
                        print(f"  [Success] New document registered: {filename} (ID: {doc_id})")
                        new_docs_count += 1
                except Exception as e:
                    print(f"  [Error] Failed to process {filename}: {e}")
        
        print(f"Finished {company_name}. Added {new_docs_count} new documents.")

    def run_batch(self, companies: List[Dict[str, str]]):
        """Runs the pipeline for a list of companies."""
        for company in companies:
            self.process_company(company['name'], company['url'])

if __name__ == "__main__":
    # Example usage
    pipeline = IngestionPipeline()
    
    # Test list of companies (Example data)
    test_companies = [
        {"name": "MRV", "url": "https://ri.mrv.com.br/central-de-resultados/"},
        {"name": "Tenda", "url": "https://ri.tenda.com.br/central-de-resultados/"},
    ]
    
    pipeline.run_batch(test_companies)
