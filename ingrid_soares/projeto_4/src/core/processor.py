import os
import json
from pathlib import Path
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv

from ingrid_soares.projeto_4.src.database.database import get_db_connection, mark_as_processed
from ingrid_soares.projeto_4.src.extractors.parser import PDFParser
from ingrid_soares.projeto_4.src.core.schemas import CompanyReport, Metric

# Load environment variables
load_dotenv(Path("ingrid_soares/projeto_4/.env"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class UDAProcessor:
    """
    Orchestrates the UDA process: PDF -> Markdown -> Gemini -> SQLite.
    """
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.parser = PDFParser()

    def _generate_prompt(self, markdown_content: str) -> str:
        """Creates the system prompt for the LLM."""
        return f"""
        Você é um especialista em extração de dados financeiros e operacionais do setor habitacional.
        Sua tarefa é analisar o relatório fornecido em Markdown e extrair métricas precisas.

        DIRETRIZES RÍGIDAS:
        1. Extraia apenas VALORES BRUTOS. Ignore porcentagens de variação destacadas pelo marketing.
        2. Se uma métrica não estiver explicitamente no texto, defina o valor como null.
        3. Identifique corretamente a Empresa, o Ano e o Trimestre.
        4. Retorne a resposta EXCLUSIVAMENTE como um JSON válido seguindo a estrutura do contrato.

        CONTRATO DE SAÍDA:
        {{
          "company_name": "Nome da Empresa",
          "year": 2025,
          "quarter": "3T",
          "metrics": [
            {{ "name": "Nome da Métrica", "value": 123.45, "unit": "R$ milhões" }},
            ...
          ]
        }}

        CONTEÚDO DO RELATÓRIO:
        {markdown_content}
        """

    def process_document(self, document_id: int, file_path: Path):
        """
        Processes a single PDF: Parse -> Gemini -> Save to DB.
        """
        print(f"Processing document ID {document_id}...")
        
        try:
            # 1. PDF to Markdown
            markdown_text = self.parser.to_markdown(file_path)
            
            # 2. LLM Extraction
            prompt = self._generate_prompt(markdown_text)
            response = self.model.generate_content(
                prompt, 
                generation_config={"response_mime_type": "application/json"}
            )
            
            # 3. Parse and Validate with Pydantic
            data = json.loads(response.text)
            report = CompanyReport(**data)
            
            # 4. Save to Database
            self._save_to_db(document_id, report)
            
            # 5. Mark as processed
            mark_as_processed(document_id)
            print(f"  [Success] Document {document_id} processed and saved.")
            
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
    # Simple test
    processor = UDAProcessor()
    # Assuming doc_id 1 exists and is in the data folder
    processor.process_document(1, Path("projeto-individual-4/exemplo_Boletim_Conjuntura_2025_3T.pdf"))
