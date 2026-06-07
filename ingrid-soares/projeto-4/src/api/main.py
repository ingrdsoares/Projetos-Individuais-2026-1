from fastapi import FastAPI, Query
from typing import List, Optional
from pathlib import Path
from src.database.database import get_db_connection

app = FastAPI(
    title="API de Conjuntura Habitacional",
    description="API para consulta de métricas extraídas de relatórios de RI via Pipeline de UDA",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Conjuntura Habitacional. Acesse /docs para a documentação Swagger."}

@app.get("/api/conjuntura")
def get_conjuntura(
    empresa: str = Query(..., description="Nome da empresa (ex: MRV, Tenda)"),
    ano: Optional[int] = Query(None, description="Ano de referência"),
    trimestre: Optional[str] = Query(None, description="Trimestre de referência (ex: 1T, 2T, 3T, 4T)")
):
    """
    Consulta métricas estruturadas filtrando por empresa, ano e trimestre.
    """
    query = """
        SELECT m.metric_name, m.metric_value, m.unit, d.company_name, m.year, m.quarter
        FROM metrics m
        JOIN documents d ON m.document_id = d.id
        WHERE d.company_name LIKE ?
    """
    params = [f"%{empresa}%"]

    if ano:
        query += " AND d.year = ?"
        params.append(ano)
    if trimestre:
        query += " AND d.quarter = ?"
        params.append(trimestre)

    with get_db_connection() as conn:
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]

@app.get("/api/documents")
def list_documents():
    """
    Lista todos os documentos processados para auditoria de linhagem.
    """
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT id, company_name, url, filename, status, processed_at FROM documents")
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
