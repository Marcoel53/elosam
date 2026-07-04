# RFC-001 — Core Constitution

**Status:** PROPOSTA

**Versão:** 1.0

**Tipo:** Request For Change

**Projeto:** EloSam

---

# Resumo

Esta RFC define oficialmente quais componentes pertencem ao Core do EloSam.

O objetivo é impedir que o núcleo cresça sem controle e preservar sua simplicidade ao longo da evolução do sistema.

---

# Motivação

Durante as primeiras Sprints, diversos componentes foram criados para validar conceitos arquiteturais.

Após a estabilização do projeto e a homologação da suíte de testes, tornou-se possível identificar um núcleo arquitetural estável.

Esta RFC formaliza esse núcleo.

---

# Problema

Sem limites claros, existe o risco de:

- crescimento excessivo do Core;
- duplicação de responsabilidades;
- aumento do acoplamento;
- perda da identidade arquitetural.

---

# Decisão

O Core do EloSam passa a ser composto exclusivamente pelos seguintes componentes:

- Application
- Kernel
- Runtime Engine
- Lifecycle
- Event Bus
- Capability Registry
- Capability Engine
- Mission Engine
- Decision Engine

Todos os demais componentes pertencem a outras camadas da arquitetura.

---

# Responsabilidades

## Core

Responsável apenas pela infraestrutura mínima necessária para execução do sistema.

O Core não implementa inteligência de domínio.

---

## Capabilities

Toda funcionalidade especializada deve ser implementada como Capability.

Exemplos:

- Knowledge
- Simulation
- Healing
- Diagnostic
- Observability
- Agents

---

## Experimental

Protótipos e pesquisas permanecem isolados do Core.

---

# Benefícios

A adoção desta RFC proporciona:

- arquitetura mais simples;
- menor acoplamento;
- maior previsibilidade;
- facilidade de testes;
- evolução incremental.

---

# Impacto

Esta RFC não altera comportamento do sistema.

Ela apenas estabelece limites arquiteturais.

---

# Compatibilidade

Compatível com a baseline atual.

Situação validada por:

- compilação bem-sucedida;
- suíte automatizada de testes;
- baseline estável.

---

# Critérios para alterar o Core

Uma modificação no Core somente poderá ocorrer quando houver:

1. nova RFC;
2. ADR correspondente;
3. implementação;
4. testes automatizados;
5. homologação.

---

# Resultado Esperado

O Core permanecerá pequeno, previsível e estável.

Toda evolução do EloSam deverá ocorrer prioritariamente por meio de novas Capabilities, preservando a integridade arquitetural do núcleo.