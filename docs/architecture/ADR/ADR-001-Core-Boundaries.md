# ADR-001 — Core Boundaries

**Status:** ACEITO

**Versão:** 1.0

**Tipo:** Architecture Decision Record

**Projeto:** EloSam

**Relacionado:**

- CCOS-001
- CCOS-002
- RFC-001

---

# Contexto

Durante a evolução do EloSam diversos componentes foram desenvolvidos para validar conceitos arquiteturais.

Após a estabilização do sistema e a homologação da suíte de testes, tornou-se possível identificar claramente quais componentes pertencem ao núcleo do sistema.

Foi necessário estabelecer limites formais para impedir que o Core crescesse indefinidamente.

---

# Decisão

O Core do EloSam deve permanecer pequeno.

O Core é composto exclusivamente por:

- Application
- Kernel
- Runtime Engine
- Lifecycle
- Event Bus
- Capability Registry
- Capability Engine
- Mission Engine
- Decision Engine

Nenhum outro componente pertence ao Core sem aprovação formal.

---

# Justificativa

Um núcleo reduzido apresenta vantagens importantes:

- menor acoplamento;
- maior estabilidade;
- facilidade de manutenção;
- melhor cobertura por testes;
- menor custo de evolução.

A inteligência do sistema deve crescer através das Capabilities, nunca através do Kernel.

---

# Consequências

## Positivas

- arquitetura previsível;
- responsabilidades bem definidas;
- facilidade para novos desenvolvedores;
- menor dívida técnica;
- evolução incremental.

## Negativas

Mudanças no Core exigirão maior disciplina de engenharia.

Essa restrição é intencional.

---

# Regras

## Kernel

Não conhece domínio.

Não implementa IA.

Não implementa regras de negócio.

---

## Runtime

Executa infraestrutura.

Não conhece Capabilities específicas.

---

## Mission Engine

Gerencia apenas missões.

Não executa inteligência.

---

## Decision Engine

Avalia decisões.

Publica eventos.

Não controla execução.

---

## Capability Engine

Executa Capabilities.

Não implementa regras específicas.

---

# Evolução

Novas funcionalidades devem ser implementadas como Capabilities registradas no Capability Registry.

O Core somente poderá ser alterado quando existir:

- RFC aprovada;
- ADR correspondente;
- implementação;
- cobertura por testes;
- homologação.

---

# Evidências

Estado da baseline no momento desta decisão:

- Compilação: OK
- Testes automatizados: 96 passando
- Runtime operacional
- Arquitetura estabilizada

---

# Conclusão

O EloSam passa a adotar oficialmente um Core mínimo.

A inteligência do sistema deverá evoluir prioritariamente através de componentes desacoplados, preservando a simplicidade do núcleo arquitetural.