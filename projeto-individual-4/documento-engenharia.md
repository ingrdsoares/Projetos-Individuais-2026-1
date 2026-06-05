# Documento de Engenharia — Projeto Individual 4: Pipeline de UDA

## 1. Arquitetura do Sistema

O sistema foi projetado para resolver o problema de fragmentação de dados não estruturados em relatórios de RI. A arquitetura é dividida em três camadas principais:

### 1.1 Camada de Extração de Dados (Ingestion Layer)
A ingestão é orientada a eventos (simulada por Polling). 
- **Scraper:** Utiliza `BeautifulSoup` para varrer portais de RI e identificar links de PDF baseados em palavras-chave.
- **Idempotência:** Implementada através do cálculo de Hash SHA-256 da URL do documento. Antes de qualquer download ou processamento, o sistema consulta o `catalog.db` para verificar se o hash já existe, evitando custos redundantes de API.
- **Parsing:** O `PDFParser` converte o PDF em Markdown utilizando `PyMuPDF`. A escolha do Markdown visa preservar a estrutura de tabelas e a hierarquia do documento, facilitando a compreensão do LLM.

### 1.2 Camada de Processamento (UDA Module)
O processamento utiliza a técnica de **Full-Scan** (envio do texto integral por página) para garantir a captura de todas as métricas, dada a natureza concisa de prévias operacionais.
- **LLM:** Utiliza o modelo `gemini-1.5-flash` por sua alta janela de contexto e eficiência em extrações estruturadas.
- **Contrato Semântico:** A blindagem do banco é feita via Pydantic. O prompt instrui o LLM a ignorar variações percentuais de marketing e extrair apenas valores absolutos.

### 1.3 Camada de Serviço (API Layer)
A camada de serviço é implementada com **FastAPI**, fornecendo endpoints REST para consulta de dados.
- **Linhagem de Dados:** Cada métrica no banco de dados está vinculada a um `document_id`, que por sua vez está vinculado à URL original do PDF, garantindo rastreabilidade total.

## 2. Justificativa de Escolhas Tecnológicas

- **Gemini 1.5 Flash:** Escolhido pela capacidade de processar JSONs estruturados nativamente e a janela de contexto ampla.
- **SQLite:** Utilizado por ser leve e suficiente para a escala do projeto, permitindo a portabilidade do Catálogo de Dados.
- **PyMuPDF:** Escolhido pela alta performance na extração de tabelas e conversão para Markdown.
- **FastAPI:** Escolhido pela facilidade de implementação de endpoints tipados e documentação automática (Swagger).

## 3. Fluxo de Operação

1. `run_pipeline.py` inicia a orquestração.
2. `RIScraper` localiza PDFs $ightarrow$ `database.py` verifica Hash.
3. PDFs novos são baixados para `/data/pdfs/`.
4. `PDFParser` converte PDF $ightarrow$ Markdown.
5. `UDAProcessor` envia Markdown + Prompt para Gemini API $ightarrow$ Recebe JSON.
6. Pydantic valida o JSON $ightarrow$ Dados salvos em `metrics` table.
7. API serve os dados via requisições HTTP.

## 4. Considerações de Resiliência

O sistema é resiliente a mudanças de layout pois não depende de coordenadas fixas ou Regex. A extração baseia-se na compreensão semântica do LLM. Se uma empresa alterar a posição de uma tabela, o LLM ainda a identificará como "Tabela de Resultados" devido ao contexto textual.
