import hashlib
import requests
from pathlib import Path
from typing import List, Dict
from ingrid_soares.projeto_4.src.database.database import init_db, register_document, get_processed_hashes
from ingrid_soares.projeto_4.src.extractors.scrapers import RIScraper

class IngestionPipeline:
    """
    Orchestrates the collection of RI PDFs and ensures idempotency.
    """
    def __init__(self, storage_dir: str = "ingrid-soares/projeto-4/data/pdfs"):
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

        for filename, url in pdf_links:
            try:
                # 1. Download temporarily to calculate hash
                response = requests.get(url, timeout=20)
                response.raise_for_status()
                content = response.content
                
                file_hash = self.calculate_hash(content)
                
                # 2. Idempotency Check
                if file_hash in processed_hashes:
                    print(f"  [Ignored] File already processed: {filename}")
                    continue
                
                # 3. Save file and register in DB
                file_path = self.storage_dir / filename
                with open(file_path, "wb") as f:
                    f.write(content)
                
                doc_id = register_document(company_name, url, file_hash, filename)
                if doc_id:
                    print(f"  [Success] New document registered: {filename} (ID: {doc_id})")
                    new_docs_count += 1
                
            except Exception as e:
                print(f"  [Error] Failed to process {filename}: {e}")
        
        print(f"Finished {company_name}. Added {new_docs_count} new documents.
")

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
