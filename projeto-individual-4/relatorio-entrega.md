# Relatório de Entrega — Projeto Individual 4

> **Aluno(a):** Ingrid Soares
> **Data de entrega:** 06/06/2026

---

## 1. Resumo do Projeto

O projeto consiste na implementação de um Pipeline de Análise de Dados Não Estruturados (UDA - Unstructured Data Analysis) para o setor habitacional. O sistema automatiza a coleta de relatórios operacionais em PDF de portais de Relações com Investidores (RI), processa a extração de métricas financeiras e operacionais utilizando a API do Google Gemini (LLM) sob um contrato semântico rigoroso, e disponibiliza esses dados através de uma API REST estruturada para alimentar o Relatório de Conjuntura do Setor Habitacional.

---

## 2. Escopo Técnico

| Componente | Implementação |
|------------|---------------|
| **Gatilho de Ingestão** | Polling de URLs de RI com detecção de novos PDFs |
| **Idempotência** | Verificação de Hash SHA-256 da URL no Catálogo de Dados |
| **Segmentação de PDF** | Estratégia de Full-Scan e Chunking Semântico via PyMuPDF |
| **Motor de Extração** | LLM Gemini 1.5 Flash com Contrato Semântico (Pydantic) |
| **Camada de Serviço** | API FastAPI com filtros por Empresa, Ano e Trimestre |
| **Qualidade e Testes** | Suíte de testes unitários com Pytest para core e banco de dados |

---

## 3. Modelagem do Pipeline

### 3.1 Fluxo de Dados (Pipeline)

```
Scraper (RI Portals) → Hash Check (SQLite) → PDF Download → Markdown Parser → Gemini LLM (Semantic Extraction) → SQLite (Structured Data) → FastAPI (Service Layer)
```

### 3.2 Contrato Semântico

A extração é blindada por esquemas Pydantic, forçando o LLM a retornar JSONs com campos específicos (`company_name`, `year`, `quarter`, `metrics`), tratando valores ausentes como NULL e ignorando ruídos de marketing.

---

## 4. Implementação

### 4.1 Tecnologias utilizadas

| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| Python | 3.9+ | Linguagem principal |
| Gemini 1.5 Flash | API | Motor de extração semântica (LLM) |
| FastAPI | 0.100+ | Camada de Serviço (API REST) |
| PyMuPDF (fitz) | 1.23+ | Parsing de PDF para Markdown |
| SQLite | 3.x | Catálogo de Dados e Armazenamento de Métricas |
| Pydantic | 2.x | Contrato Semântico e Validação de Dados |
| BeautifulSoup4 | 4.x | Scraping de portais de RI |

### 4.2 Estrutura do código

```
ingrid_soares/projeto_4/
├── data/
│   └── pdfs/              # Armazenamento de PDFs baixados
│   └── catalog.db         # Banco de Dados (Catálogo e Métricas)
├── src/
│   ├── api/               # FastAPI endpoints
│   ├── core/              # Ingestão, Processamento e Schemas
│   ├── database/          # Gerenciamento do SQLite
│   └── extractors/        # Scrapers e Parsers de PDF
├── .env                   # Chaves de API
└── run_pipeline.py        # Orquestrador principal
```

### 4.3 Como executar

```bash
# 1. Instalar dependências
pip install fastapi uvicorn requests beautifulsoup4 pymupdf pydantic google-generativeai python-dotenv

# 2. Configurar a chave da API no arquivo .env
echo "GEMINI_API_KEY=sua_chave_aqui" > ingrid_soares/projeto_4/.env

# 3. Executar o pipeline de ingestão e processamento
python run_pipeline.py

# 4. Iniciar a API de serviço
python -m ingrid_soares.projeto_4.src.api.main
```

---

## 5. Checklist de entrega

- [x] Documento de engenharia preenchido
- [x] Código funcional no repositório
- [x] Relatório de entrega preenchido
- [x] Pull Request aberto
- [x] Artefatos de auditoria completos (Mission Brief, ADR, Evidence, Merge-Readiness)
