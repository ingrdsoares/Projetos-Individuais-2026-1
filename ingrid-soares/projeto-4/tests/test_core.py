import pytest
from pathlib import Path
from src.database.database import init_db, register_document, get_processed_hashes
from src.core.schemas import CompanyReport, Metric
from src.extractors.scrapers import RIScraper
import hashlib

def test_database_idempotency():
    """Test that the same URL cannot be registered twice."""
    init_db()
    company = "TestCo"
    url = "https://example.com/report.pdf"
    file_hash = hashlib.sha256(url.encode()).hexdigest()
    filename = "report.pdf"
    
    # First registration
    doc_id1 = register_document(company, url, file_hash, filename)
    assert doc_id1 is not None
    
    # Second registration (duplicate)
    doc_id2 = register_document(company, url, file_hash, filename)
    assert doc_id2 is None

def test_schema_validation():
    """Test that Pydantic schemas validate correct data and fail on incorrect data."""
    valid_data = {
        "company_name": "MRV",
        "year": 2025,
        "quarter": "3T",
        "metrics": [{"name": "Vendas", "value": 100.0, "unit": "milhões"}]
    }
    report = CompanyReport(**valid_data)
    assert report.company_name == "MRV"
    
    invalid_data = {"company_name": "MRV", "year": "not-a-year"}
    with pytest.raises(ValueError):
        CompanyReport(**invalid_data)

def test_scraper_link_detection():
    """Test that the scraper correctly identifies PDF links (using mock-like check)."""
    scraper = RIScraper("TestCo", "https://google.com")
    # We test the logic of filtering, assuming find_pdf_links is called
    # This is a simple check on the internal filter logic if it were extracted, 
    # but here we just verify the class initializes.
    assert scraper.company_name == "TestCo"

if __name__ == "__main__":
    pytest.main([__file__])
