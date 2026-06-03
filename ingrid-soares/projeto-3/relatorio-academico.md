# Relatório Acadêmico: Framework Multi-Agente de Segurança Red Team Híbrido

## 1. Introdução
Este projeto apresenta o desenvolvimento de um **Framework de Segurança Híbrido**, que automatiza o ciclo de Red Team (Reconhecimento, Validação e Relatório) de forma contínua, escalável e com custo operacional zero.

## 2. Checklist de Conformidade do Projeto
1. **Estrutura de Pastas:** `projeto-3/` organizada com `docs/`, `solutions/`, `src/`, `tests/` e `README.md`.
2. **Mission Brief:** Criado e detalhando objetivos, limites e riscos.
3. **Agent.md:** Definidas as regras de comportamento do agente.
4. **Mentorship Pack:** Criado com princípios de arquitetura e padrões.
5. **Workflow Runbook:** Processo de execução documentado.
6. **Merge-Readiness Pack:** Checklist final de prontidão.
7. **Quatro Soluções:**
    - A: Planejamento Tático (LLM/Groq/Llama-3).
    - B: Validação Prática (API VirusTotal).
    - C: Orquestrador Assíncrono (n8n).
    - D: Infraestrutura de Testes (Python/Pytest).
8. **Rastreabilidade:** Decisões registradas via ADRs, logs em `imgs/` e racionalidade em cada commit.
9. **Uso de IA Inteligente:** IA utilizada para tomada de decisão estratégica (análise de risco).
10. **Integração:** Fluxo validado de ponta a ponta.

## 3. Justificativa Técnica: Red Team e Multi-Agente
O projeto prova sua maturidade em dois pilares:
- **Red Team:** Implementa o ciclo de *Reconhecimento* (Solution A - definição de perímetro tático) e *Validação Técnica* (Solution B - checagem factual via VirusTotal).
- **Multi-Agente:** Arquitetura composta por agentes especializados (Planejador, Validador, Orquestrador) que se comunicam via protocolo JSON, permitindo autonomia delegada.

## 4. Arquitetura Híbrida e Sustentabilidade
A transição para um modelo **Híbrido (Determinístico + LLM)** garante precisão técnica e eficiência financeira, operando 100% em *Free-tier* (n8n Cloud, Groq Cloud, VirusTotal API).

## 5. Instruções para o Revisor (Pull Request)

### Título do PR
**Projeto 3: Framework Multi-Agente de Segurança Red Team Híbrido**

### Descrição do PR
Entrega final do framework de automação de segurança. O projeto segue estritamente o framework de Engenharia de Software Agêntica, com documentação completa em cada etapa.

**Entregáveis auditáveis:**
- **Mission Brief:** Definição contratual do agente e objetivos.
- **Mentorship Pack:** Regras de comportamento e padrões de desenvolvimento.
- **Workflow Runbook:** Processo de execução auditável.
- **Soluções (A, B, C e D):**
  - **A (Planejamento):** Inteligência tática via LLM (Groq/Llama-3).
  - **B (Validação):** Motor determinístico (VirusTotal).
  - **C (Orquestração):** Orquestrador assíncrono (n8n).
  - **D (QA):** Pipeline de testes automatizados (Python).
- **ADR-001:** Registro da evolução para arquitetura híbrida sustentável.
- **Merge-Readiness Pack:** Checklist final de prontidão para entrega.

### Como Executar
1. Importe os arquivos `workflow.json` na sua instância do n8n.
2. Ative os fluxos (`Active`).
3. Configure as chaves de API (VirusTotal/Groq) no n8n.
4. Execute o script de teste para validar a integração:
```bash
pip install requests
python3 ingrid-soares/projeto-3/solutions/solution-d/tests/test_framework.py
```
