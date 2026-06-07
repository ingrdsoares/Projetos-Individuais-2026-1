import os
from pathlib import Path
from src.core.ingestion import IngestionPipeline
from src.core.processor import UDAProcessor
from src.database.database import init_db, get_db_connection

def main():
    print("Iniciando Pipeline de UDA")
    init_db()
    companies = [
        {"name": "MRV", "url": "https://ri.mrv.com.br/central-de-resultados/"},
        {"name": "Tenda", "url": "https://ri.tenda.com.br/central-de-resultados/"},
    ]
    print("Fase 1: Ingestao")
    ingestion = IngestionPipeline()
    ingestion.run_batch(companies)
    print("Fase 2: Processamento")
    processor = UDAProcessor()
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT id, filename FROM documents WHERE status = 'pending'")
        pending_docs = cursor.fetchall()
        if not pending_docs:
            print("Nada para processar")
        else:
            for doc in pending_docs:
                processor.process_document(doc['id'], Path(f"ingrid_soares/projeto_4/data/pdfs/{doc['filename']}"))
    print("Pipeline Concluido")

if __name__ == "__main__":
    main()
