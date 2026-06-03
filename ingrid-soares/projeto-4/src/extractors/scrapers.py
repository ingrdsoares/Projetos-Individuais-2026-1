import requests
from bs4 import BeautifulSoup
from typing import List, Tuple
from urllib.parse import urljoin

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

    def find_pdf_links(self, keywords: List[str] = ["PDF", "Prévia Operacional", "Resultados", "Relatório"]) -> List[Tuple[str, str]]:
        """
        Scans the base URL for links ending in .pdf that match the specified keywords.
        Returns a list of tuples (filename, absolute_url).
        """
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            found_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text().strip()
                
                if href.lower().endswith('.pdf'):
                    # Check if any keyword is in the link text or URL
                    if any(kw.lower() in text.lower() or kw.lower() in href.lower() for kw in keywords):
                        full_url = urljoin(self.base_url, href)
                        filename = href.split('/')[-1]
                        found_links.append((filename, full_url))
            
            return found_links
        except Exception as e:
            print(f"Error scraping {self.company_name} at {self.base_url}: {e}")
            return []

if __name__ == "__main__":
    # Quick test
    scraper = RIScraper("Example Co", "https://www.example.com/ri")
    print(scraper.find_pdf_links())
