# 📖 ELOSAM OPERATING MANUAL

Versão: 1.0

Status: NORMATIVO

---

# Introdução

Este documento descreve como o EloSam deve ser desenvolvido, mantido e evoluído.

Nenhuma implementação deve ocorrer sem respeitar este manual.

---

# Fluxo Oficial

Toda mudança segue obrigatoriamente o fluxo abaixo.

```
Necessidade
      │
      ▼
Análise
      │
      ▼
RFC
      │
      ▼
ADR
      │
      ▼
Sprint Plan
      │
      ▼
Implementação
      │
      ▼
Testes
      │
      ▼
Architecture Review
      │
      ▼
Commit
      │
      ▼
Release
```

---

# Ordem de Prioridade

Quando existir conflito entre decisões, a seguinte prioridade deve ser respeitada.

1. Vision
2. Constitution
3. Architecture Catalog
4. RFC
5. ADR
6. Sprint Plan
7. Código
8. Testes

---

# Regras

## Nunca

- quebrar o Core sem RFC
- remover testes para fazer código passar
- adicionar acoplamento desnecessário
- duplicar responsabilidades

---

## Sempre

- escrever testes
- documentar decisões
- preservar compatibilidade
- preferir simplicidade

---

# Definição de Concluído

Uma Sprint somente é considerada concluída quando:

- implementação finalizada
- testes verdes
- documentação atualizada
- arquitetura preservada
- commit realizado

---

# Filosofia

A arquitetura vem antes da implementação.

O conhecimento vem antes da arquitetura.

A simplicidade vem antes da sofisticação.

---

Fim.