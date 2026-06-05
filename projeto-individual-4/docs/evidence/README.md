# Evidências de Implementação - Projeto 4

Este diretório contém as evidências de funcionamento do Pipeline de UDA.

## Evidências Disponíveis
1. **Logs do Pipeline:** O arquivo `run_pipeline.py` gera logs no console detalhando:
   - PDFs encontrados e registrados no Catálogo de Dados.
   - Documentos processados com sucesso pela LLM.
   - Erros de parsing ou conexão.
2. **Dados Estruturados (SQLite):** A tabela `metrics` no arquivo `catalog.db` serve como prova da extração correta de valores absolutos.
3. **Resposta da API:** O endpoint `/api/conjuntura` retorna JSONs estruturados, validando a camada de serviço.
4. **Linhagem de Dados:** A tabela `documents` registra a URL original de cada PDF, provando a rastreabilidade da informação.

## Como Validar
Para gerar novas evidências:
1. Configure a `GEMINI_API_KEY` no arquivo `.env`.
2. Execute `python run_pipeline.py`.
3. Inicie a API com `python -m ingrid_soares.projeto_4.src.api.main`.
4. Acesse `http://localhost:8000/api/conjuntura?empresa=MRV`.
