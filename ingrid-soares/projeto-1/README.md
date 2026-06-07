# Projeto Individual 1: Agente de IA Orientado a Problema

## Objetivo

Projetar e implementar um **agente de IA funcional**, com foco em:

- Engenharia de requisitos
- Modelagem de fluxos (decisão e interação)
- Arquitetura de sistemas baseados em LLM / agentes
- Implementação e avaliação

---

## Descrição Geral

Cada aluno deverá:

1. **Escolher um domínio específico (único)**
2. **Definir um problema claro**
3. **Projetar um agente de IA que resolva esse problema**
4. **Implementar um protótipo funcional**
5. **Documentar requisitos, fluxos e decisões arquiteturais**

---

## Estratégia para garantir 30 projetos diferentes

Cada aluno receberá **1 item de cada coluna** abaixo, garantindo unicidade:

### 1. Domínios

| # | Domínio |
|---|---------|
| 1 | Saúde pública |
| 2 | Educação |
| 3 | Participação cidadã |
| 4 | Compras públicas |
| 5 | Meio ambiente |
| 6 | Mobilidade urbana |
| 7 | Cultura |
| 8 | Justiça |
| 9 | Assistência social |
| 10 | Open source / comunidades |

### 2. Função do agente

| # | Função |
|---|--------|
| 1 | Classificação |
| 2 | Recomendação |
| 3 | Resumo |
| 4 | Análise de sentimento |
| 5 | Extração de dados |
| 6 | Tomada de decisão |
| 7 | Planejamento |
| 8 | Geração de respostas |
| 9 | Detecção de anomalias |
| 10 | Mediação/conversação |

### 3. Restrição obrigatória

| # | Restrição |
|---|-----------|
| 1 | Tempo real |
| 2 | Baixo custo |
| 3 | Offline-first |
| 4 | Explicabilidade obrigatória |
| 5 | Privacidade (LGPD) |
| 6 | Multimodal |
| 7 | Dados incompletos |
| 8 | Integração com API externa |
| 9 | Escalabilidade |
| 10 | Auditoria e rastreabilidade |

---

## Entregáveis

### 1. Documento de Engenharia (obrigatório)

Seções mínimas:

- Problema e contexto
- Stakeholders
- Requisitos funcionais (RF)
- Requisitos não-funcionais (RNF)
- Casos de uso
- Fluxo do agente (diagrama ou descrição)
- Arquitetura (RAG? tool-using? pipeline?)
- Estratégia de avaliação

> Utilize o template disponível em [`templates/documento-engenharia.md`](templates/documento-engenharia.md)

### 2. Modelagem do Agente

Descrever claramente:

- **Entrada** (input)
- **Processamento** (pipeline do agente)
- **Decisão** (como o agente "pensa")
- **Saída** (output)

Exemplo de estrutura:

```
Usuário → Prompt → LLM → Tool (opcional) → Memória → Resposta
```

### 3. Implementação

Requisitos mínimos:

- Código funcional (Python recomendado)
- Uso de pelo menos 1:
  - LLM (OpenAI, Ollama, etc.)
  - ou modelo local
- Pipeline claro (não apenas um prompt simples)

**Diferencial esperado:**

- Uso de RAG, ferramentas (tools), memória ou agentes multi-etapas

### 4. Avaliação

O aluno deve definir:

- Métrica(s) de qualidade: precisão, relevância, latência, custo
- Testes com exemplos reais

> Utilize o template disponível em [`templates/relatorio-entrega.md`](templates/relatorio-entrega.md)

---

## Exemplos de projetos (para inspirar)

- Agente que classifica propostas do Brasil Participativo
- Agente que recomenda políticas públicas com base em dados abertos
- Agente que detecta inconsistências em compras públicas
- Agente que resume reuniões governamentais
- Agente que ajuda contribuidores de open source

---

## Critérios de Avaliação

| Critério | Peso |
|----------|------|
| Clareza dos requisitos | 20% |
| Qualidade da modelagem | 20% |
| Arquitetura do agente | 20% |
| Implementação | 20% |
| Avaliação e testes | 20% |

---

## Critérios de excelência (bônus)

Projetos que incluírem:

- RAG com base externa
- Múltiplos agentes
- Explicabilidade
- Análise crítica de limitações

receberão **pontuação bônus**.

---

## Observação importante

> "O objetivo não é só usar IA, mas **engenheirar um sistema baseado em IA**."

---

## Como submeter

**Data limite de entrega: 30/03/2026 (segunda-feira)**

1. Crie uma pasta com seu nome na raiz do repositório (ex: `maria-silva/`)
2. Dentro da sua pasta, crie a subpasta `projeto-1/`
3. Coloque todos os entregáveis dentro dessa subpasta
4. Abra um **Pull Request** para cada submissão
