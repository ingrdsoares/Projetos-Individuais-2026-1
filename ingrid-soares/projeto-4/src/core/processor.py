import os
import json
import time
from pathlib import Path
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv

from src.database.database import get_db_connection, mark_as_processed
from src.extractors.parser import PDFParser
from src.core.schemas import CompanyReport, Metric

# Load environment variables
load_dotenv(Path(".env"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class UDAProcessor:
    """
    Orchestrates the UDA process: PDF -> Markdown -> Gemini -> SQLite.
    """
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.parser = PDFParser()

    def _generate_prompt(self, content: str) -> str:
        """Creates a strict system prompt for high-precision UDA extraction."""
        return f"""
        SISTEMA: Especialista em Extração de Dados Financeiros Habitacionais.
        TAREFA: Analisar os trechos de relatório fornecidos e extrair métricas estruturadas.

        REGRAS CRÍTICAS de QUALIDADE:
        1. VALORES ABSOLUTOS: Extraia apenas o valor bruto (ex: R$ 150 milhões). IGNORE porcentagens de variação (ex: 'crescimento de 10%').
        2. TRATAMENTO de NULOS: Se a métrica não for encontrada explicitamente nos trechos, defina o valor como null. NÃO invente dados.
        3. CONTEXTO TEMPORAL: Identifique com precisão a Empresa, o Ano e o Trimestre.
        4. FORMATO: Responda EXCLUSIVAMENTE em JSON válido.

        CONTRATO de SAÍDA:
        {{
          "company_name": "Nome da Empresa",
          "year": 2025,
          "quarter": "3T",
          "metrics": [
            {{ "name": "Vendas Líquidas", "value": 123.45, "unit": "R$ milhões" }},
            {{ "name": "Lançamentos", "value": 450, "unit": "unidades" }}
          ]
        }}

        TRECHOS DO RELATÓRIO:
        {content}
        """

    def process_document(self, document_id: int, file_path: Path):
        """
        Advanced UDA Process: Parse -> Semantic Chunking -> Gemini -> SQLite.
        Implements retry logic for API Rate Limits (429).
        """
        print(f"Processing document ID {document_id}...")
        
        try:
            # 1. Semantic Chunking
            chunks = self.parser.get_semantic_chunks(file_path)
            content_to_analyze = (chr(10) + chr(10)).join(chunks)
            
            if not content_to_analyze:
                print(f"  [Warning] No relevant content found in document {document_id}.")
                return

            prompt = self._generate_prompt(content_to_analyze)
            
            # Retry loop for Rate Limits (429)
            max_retries = 3
            retry_delay = 10 
            response = None
            
            for attempt in range(max_retries):
                try:
                    response = self.model.generate_content(
                        prompt, 
                        generation_config={"response_mime_type": "application/json"}
                    )
                    break # Success!
                except Exception as e:
                    if "429" in str(e) or "quota" in str(e).lower():
                        if attempt < max_retries - 1:
                            print(f"  [Rate Limit] API quota reached. Retrying in {retry_delay}s... (Attempt {attempt+1}/{max_retries})")
                            time.sleep(retry_delay)
                            retry_delay *= 2
                            continue
                    raise e

            # 2. Parse and Validate
            data = json.loads(response.text)
            if isinstance(data, list):
                data = data[0] if data else {}
            
            report = CompanyReport(**data)
            
            # 3. Save and Mark
            self._save_to_db(document_id, report)
            mark_as_processed(document_id)
            print(f"  [Success] Document {document_id} processed. Extracted {len(report.metrics)} metrics.")
            
        except Exception as e:
            print(f"  [Error] Failed to process document {document_id}: {e}")

    def _save_to_db(self, document_id: int, report: CompanyReport):
        """Saves the extracted metrics to the SQLite database."""
        with get_db_connection() as conn:
            for metric in report.metrics:
                conn.execute(
                    "INSERT INTO metrics (document_id, year, quarter, metric_name, metric_value, unit) VALUES (?, ?, ?, ?, ?, ?)",
                    (document_id, report.year, report.quarter, metric.name, metric.value, metric.unit)
                )
            conn.commit()

if __name__ == "__main__":
    processor = UDAProcessor()
    processor.process_document(1, Path("exemplo_Boletim_Conjuntura_2025_3T.pdf"))
