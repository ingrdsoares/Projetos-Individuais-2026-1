# ADR-001: Definição da Arquitetura do Pipeline de UDA

> **Data:** 30/05/2026
> **Status:** aceita

---

## Contexto

O desafio do Projeto 4 exige a construção de um pipeline para extrair dados de relatórios em PDF de portais de RI de construtoras. O sistema deve ser resiliente a mudanças de layout, automatizado e fornecer dados estruturados via API. O objetivo é alcançar a máxima profundidade de análise sem custo financeiro de infraestrutura ou API.

---

## Alternativas consideradas

### Alternativa A: Solução Lean (Full-Scan Simples)

- **Descrição:** Extração de texto linear via PyMuPDF e envio integral ao LLM.
- **Prós:** Implementação rápida, simplicidade.
- **Contras:** Menor precisão em tabelas complexas, maior consumo de tokens em PDFs longos.

### Alternativa B: Solução Semantic-RAG (Chunking)

- **Descrição:** Segmentação do PDF em blocos semânticos e recuperação de trechos relevantes antes de enviar ao LLM.
- **Prós:** Menor custo de tokens, alta precisão em documentos extensos.
- **Contras:** Complexidade adicional no código, risco de corte de tabelas ao meio.

### Alternativa C: Solução Híbrida "Deep-Free" (Markdown + Contextual Full-Scan)

- **Descrição:** Conversão de PDFs para Markdown (preservando estrutura de tabelas) e uso do Gemini 1.5 Flash via API gratuita, aproveitando sua janela de contexto de 1M de tokens para realizar um Full-Scan sem perdas.
- **Prós:** Máxima precisão em tabelas, visão global do documento, custo zero, simplicidade de implementação comparada ao RAG.
- **Contras:** Dependência de API externa (Google).

---

## Decisão

Foi escolhida a **Alternativa C: Solução Híbrida "Deep-Free"**.

A decisão baseia-se no fato de que o Gemini 1.5 Flash elimina a necessidade de chunking complexo devido à sua imensa janela de contexto, enquanto a conversão para Markdown resolve o problema histórico de extração de tabelas em PDFs. O uso de Pydantic para a saída estruturada garante a integridade do Contrato Semântico.

---

## Consequências

- **Tecnologias Adotadas**: Python, Gemini 1.5 Flash, PyMuPDF/Marker (Markdown), FastAPI e SQLite.
- **Fluxo de Dados**: Site RI $ightarrow$ PDF $ightarrow$ Markdown $ightarrow$ Gemini (Structured Output) $ightarrow$ SQLite $ightarrow$ FastAPI.
- **Manutenção**: O sistema torna-se independente de layouts específicos, dependendo apenas da capacidade semântica do modelo.

---

## Referências

- Documentação Gemini 1.5 Flash (Google AI Studio).
- Especificação do Desafio Prático: Pipeline de UDA.
