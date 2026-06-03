# Mission Brief

> **Aluno(a):** Ingrid Soares
> **Matrícula:** [Sua Matrícula]
> **Domínio:** Análise de Dados Não Estruturados (UDA) - Setor Habitacional

---

## 1. Objetivo do agente

Implementar um Pipeline de Engenharia e Análise de Dados Inteligente capaz de monitorar automaticamente Centrais de Resultados (RI) de incorporadoras, extrair métricas financeiras e operacionais de relatórios em PDF utilizando LLMs e servir esses dados integrados através de uma API estruturada para alimentar o Relatório de Conjuntura do Setor Habitacional.

---

## 2. Problema que ele resolve

O Ministério das Cidades precisa de dados consolidados para o Relatório de Conjuntura, porém as informações estão pulverizadas em documentos PDF não estruturados publicados trimestralmente por diversas empresas. A extração manual é lenta, propensa a erros e difícil de escalar. Além disso, as empresas frequentemente alteram o layout de seus relatórios, tornando extratores baseados em regras rígidas (regex ou coordenadas) obsoletos rapidamente.

---

## 3. Usuários-alvo

Analistas de dados e gestores do Ministério das Cidades responsáveis pela elaboração do Relatório de Conjuntura do Setor Habitacional.

---

## 4. Contexto de uso

O sistema operará de forma contínua (orientada a eventos). Ele monitorará periodicamente os portais de RI das construtoras. Ao detectar um novo PDF de Prévia Operacional, o pipeline iniciará a ingestão, processamento semântico e armazenamento, permitindo que os analistas consultem os dados atualizados via API.

---

## 5. Entradas e saídas esperadas

| Item | Descrição |
|------|-----------|
| **Entrada** | Documentos PDF de Prévias Operacionais coletados de portais de RI. |
| **Formato da entrada** | Arquivos PDF (estáticos, variando em layout). |
| **Saída** | Dados estruturados de métricas habitacionais e financeiras. |
| **Formato da saída** | Respostas JSON via API REST (filtráveis por empresa, ano e trimestre). |

---

## 6. Limites do agente

### O que o agente faz:

- Monitora portais de RI de forma automatizada (Polling/Cron).
- Garante a idempotência da ingestão via cálculo de hash dos arquivos.
- Realiza a extração semântica de dados utilizando LLMs (evitando regras rígidas de layout).
- Valida a saída dos dados através de um Contrato Semântico (estilo Pydantic/JSON Schema).
- Mantém a linhagem dos dados, vinculando cada registro ao link do PDF original.
- Disponibiliza os dados via API REST.

### O que o agente NÃO deve fazer:

- Criar interfaces gráficas complexas (dashboards).
- Realizar previsões financeiras ou análises preditivas de mercado.
- Modificar a estrutura original dos PDFs coletados.

---

## 7. Critérios de aceitação

- [ ] O pipeline extrai dados com sucesso de pelo menos dois layouts de empresas diferentes (ex: tabelas vs slides).
- [ ] Os valores extraídos são valores brutos, ignorando porcentagens de variação destacadas no texto.
- [ ] A API retorna dados consistentes e filtráveis por empresa, ano e trimestre.
- [ ] Cada linha de dado no banco de dados possui a URL do PDF de origem (Data Lineage).
- [ ] O sistema ignora arquivos já processados anteriormente (Idempotência).

---

## 8. Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Mudança drástica no layout do PDF | Média | Médio | Uso de extração semântica via LLM em vez de regras fixas. |
| Bloqueio de acesso aos sites de RI | Média | Alto | Implementação de políticas de agendamento (Polling) moderadas e uso de headers de User-Agent. |
| Alucinações do LLM nos valores numéricos | Baixa | Alto | Implementação de Contrato Semântico rigoroso e validação de tipos. |
| Custo excessivo de tokens em PDFs longos | Média | Médio | Implementação de estratégia de Chunking Semântico para enviar apenas trechos relevantes. |

---

## 9. Evidências necessárias

- [ ] Logs de execução demonstrando a detecção de novos arquivos e a verificação de hash.
- [ ] Amostras de JSONs de saída comparando o dado extraído com o PDF original.
- [ ] Print de requisições bem-sucedidas à API de Conjuntura.
- [ ] Tabela de linhagem demonstrando o vínculo Dado $ightarrow$ PDF.
