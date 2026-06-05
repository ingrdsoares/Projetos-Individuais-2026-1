# Merge-Readiness Pack: Pipeline de UDA (Unstructured Data Analysis)

## Resumo da Solução
Implementação de um pipeline automatizado para extração de dados não estruturados (PDFs) de portais de Relações com Investidores (RI) de construtoras habitacionais. A solução utiliza a API do Google Gemini para extração semântica, transformando relatórios PDF em dados estruturados no banco de dados SQLite.

## Arquitetura Implementada
A solução segue rigorosamente as três camadas obrigatórias:
1. **Camada de Extração de Dados:** 
   - Scrapers automatizados com detecção de novos arquivos.
   - PDFParser utilizando PyMuPDF para conversão de PDF para Markdown (estratégia Full-Scan).
2. **Contrato Semântico dos Dados:**
   - Esquemas Pydantic (`CompanyReport`, `Metric`) que forçam a saída estruturada do LLM e tratam valores ausentes como NULL.
3. **Catálogo de Dados e Linhagem:**
   - Banco de dados SQLite rastreando a linhagem exata: URL original $ightarrow$ Hash do Arquivo $ightarrow$ ID do Documento $ightarrow$ Métricas Extraídas.

## Testes e Validação
- [x] **Idempotência:** Testado via hash SHA-256, evitando reprocessamento de arquivos já existentes.
- [x] **Resiliência de Layout:** A extração semântica via Gemini permite processar diferentes designs de PDF sem regras fixas.
- [x] **API de Serviço:** Endpoint `/api/conjuntura` funcional para filtros por empresa, ano e trimestre.

## Checklist de Revisão Final
- [x] Pipeline executa do início ao fim (Ingestão $ightarrow$ Processamento $ightarrow$ API).
- [x] Contrato semântico blinda a saída contra alucinações.
- [x] Linhagem de dados registrada no Catálogo de Dados.
- [x] Documentação de auditoria completa (Mission Brief, ADR, Evidências).
