# RFC-002 — Capability Architecture

**Status:** PROPOSTA

**Versão:** 1.0

**Projeto:** EloSam

---

# Objetivo

Definir oficialmente a arquitetura de Capabilities do EloSam.

A partir desta RFC, toda nova funcionalidade deverá ser implementada preferencialmente como uma Capability.

---

# Motivação

O Core do EloSam foi estabilizado.

Novas funcionalidades não devem aumentar a complexidade do núcleo.

A arquitetura baseada em Capabilities permite expansão sem aumento de acoplamento.

---

# Definição

Uma Capability representa uma capacidade especializada do sistema.

Ela encapsula uma responsabilidade única.

Pode ser registrada dinamicamente.

Pode ser inicializada independentemente.

Pode evoluir sem alterar o Core.

---

# Estrutura

Application

↓

Kernel

↓

Runtime

↓

Capability Registry

↓

Capability Engine

↓

Capabilities

---

# Ciclo de Vida

Registro

↓

Inicialização

↓

Disponível

↓

Execução

↓

Shutdown

---

# Interface mínima

Toda Capability deve implementar:

initialize()

shutdown()

ready()

---

# Descoberta

Capabilities devem ser registradas no Capability Registry.

O Kernel nunca instancia Capabilities diretamente.

---

# Comunicação

A comunicação entre Capabilities deve ocorrer preferencialmente através do Event Bus.

Acoplamento direto deve ser evitado.

---

# Benefícios

- baixo acoplamento;

- alta coesão;

- expansão modular;

- facilidade de testes;

- carregamento dinâmico;

- evolução incremental.

---

# Exemplos

Knowledge Capability

Simulation Capability

Healing Capability

Diagnostic Capability

Observability Capability

Meta-Agent Capability

---

# Restrições

Capabilities não pertencem ao Core.

Capabilities não modificam o Kernel.

Capabilities não alteram o Runtime.

---

# Evolução

Novas Capabilities poderão ser adicionadas sem alterar a arquitetura constitucional do EloSam.

Esta RFC estabelece a Capability como unidade oficial de expansão do sistema.