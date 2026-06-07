import json
from pathlib import Path
from typing import List
from src.database.database import get_db_connection, mark_as_processed
from src.core.schemas import CompanyReport, Metric

class MockUDAProcessor:
    """
    Simulates the UDA Processor to allow testing of the API and Database
    without consuming Gemini API tokens.
    """
    def process_document(self, document_id: int, file_path: Path):
        print(f" [MOCK] Processing document ID {document_id}...")
        
        # Simulated data based on a typical 'Boletim de Conjuntura'
        mock_data = {
            "company_name": "Incorporadora Exemplo S.A.",
            "year": 2025,
            "quarter": "3T",
            "metrics": [
                {"name": "Lançamentos", "value": 1250.0, "unit": "unidades"},
                {"name": "Vendas Líquidas", "value": 450.5, "unit": "R$ milhões"},
                {"name": "Estoque Total", "value": 3100.0, "unit": "unidades"},
                {"name": "Margem Bruta", "value": 22.4, "unit": "%"},
                {"name": "Custo de Construção", "value": 180.2, "unit": "R$ milhões"}
            ]
        }
        
        try:
            report = CompanyReport(**mock_data)
            
            with get_db_connection() as conn:
                for metric in report.metrics:
                    conn.execute(
                        "INSERT INTO metrics (document_id, year, quarter, metric_name, metric_value, unit) VALUES (?, ?, ?, ?, ?, ?)",
                        (document_id, report.year, report.quarter, metric.name, metric.value, metric.unit)
                    )
                conn.commit()
            
            mark_as_processed(document_id)
            print(f"  [MOCK Success] Document {document_id} processed and saved with mock data.")
            
        except Exception as e:
            print(f"  [MOCK Error] Failed to process document {document_id}: {e}")

if __name__ == "__main__":
    # Test the mock
    processor = MockUDAProcessor()
    processor.process_document(1, Path("projeto-individual-4/exemplo_Boletim_Conjuntura_2025_3T.pdf"))
