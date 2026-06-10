import requests
from bs4 import BeautifulSoup
from typing import List, Tuple
from urllib.parse import urljoin
import hashlib

from src.database import database  # Importa o módulo database

class RIScraper:
    """
    Scraper to find PDF reports in Investor Relations (RI) portals.
    """
    def __init__(self, company_name: str, base_url: str):
        self.company_name = company_name
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def find_pdf_links(self, keywords: List[str] = ["PDF", "Prévia Operacional", "Resultados", "Relatório", "Trimestral", "Operacional"]) -> List[Tuple[str, str, str]]:
        """
        Scans the base URL for links that likely point to PDFs and match the specified keywords.
        Returns a list of tuples (filename, absolute_url, url_hash).
        """
        try:
            print(f"Scraping {self.company_name} at {self.base_url}...")
            response = requests.get(self.base_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            found_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text().strip()
                
                if '.pdf' in href.lower():
                    if any(kw.lower() in text.lower() or kw.lower() in href.lower() for kw in keywords):
                        full_url = urljoin(self.base_url, href)
                        filename = href.split('/')[-1].split('?')[0]
                        url_hash = hashlib.sha256(full_url.encode('utf-8')).hexdigest()
                        found_links.append((filename, full_url, url_hash))
            
            return found_links
        except requests.exceptions.RequestException:
            print(f"  [Info] Server unavailable for {self.company_name}, skipping...")
            return []
        except Exception as e:
            print(f"  [Info] {self.company_name}: {e}")
            return []

def scrape_all_companies(company_urls: List[Tuple[str, str]]) -> List[Tuple[str, str, str, int]]:
    """
    Scrapes PDF links for a list of companies, applies idempotency check,
    and registers new documents. Returns a list of (filename, absolute_url, url_hash, document_id) for new PDFs.
    """
    all_new_pdf_links = []
    database.init_db()  # Initialize DB on first scrape
    processed_hashes = database.get_processed_hashes()

    for company_name, url in company_urls:
        scraper = RIScraper(company_name, url)
        links = scraper.find_pdf_links()
        
        for filename, full_url, url_hash in links:
            if url_hash not in processed_hashes:
                document_id = database.register_document(company_name, full_url, url_hash, filename)
                if document_id:
                    print(f"New PDF found and registered: {filename} from {company_name}")
                    all_new_pdf_links.append((filename, full_url, url_hash, document_id))
                else:
                    # This case should ideally not be hit due to processed_hashes check,
                    # but acts as a safeguard against race conditions or direct DB insertions.
                    print(f"PDF {filename} from {company_name} already registered (IntegrityError).")
            else:
                print(f"PDF {filename} from {company_name} already processed. Skipping.")
    return all_new_pdf_links

if __name__ == "__main__":
    # Example usage with multiple companies
    companies_to_scrape = [
        ("MRV", "https://ri.mrv.com.br/central-de-resultados/"),
        ("Tenda", "https://ri.tenda.com.br/central-de-resultados/"),
        ("Direcional", "https://ri.direcional.com.br/central-de-resultados/"),
    ]
    
    # Initialize the database if not already done
    database.init_db()
    print("Database initialized.")

    found_pdfs = scrape_all_companies(companies_to_scrape)
    print("\n--- New PDFs for Processing ---")
    if not found_pdfs:
        print("No new PDFs found.")
    for filename, url, url_hash, doc_id in found_pdfs:
        print(f"Ready for processing: {filename} - {url} (Hash: {url_hash}, Doc ID: {doc_id})")
