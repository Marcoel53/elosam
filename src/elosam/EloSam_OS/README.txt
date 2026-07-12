ELOSAM OS DESKTOP BETA 1.0
==========================

INSTALACAO
----------

1. Instale Python 3.11 ou Python 3.12.
2. Durante a instalacao marque:
   Add Python to PATH

3. Execute:
   INSTALAR.bat

4. Depois execute:
   INICIAR_ELOSAM.bat

5. Abra:
   http://127.0.0.1:8080

API:
   http://127.0.0.1:8080/docs

STATUS:
   http://127.0.0.1:8080/api/status


ARQUITETURA INICIAL
-------------------

EloSam OS
  |
  +-- Kernel
  |    +-- Capability Registry
  |    +-- Capability Resolver
  |    +-- Transport
  |    +-- Bundle Loader
  |
  +-- Engines
  |    +-- Knowledge
  |    +-- Mission
  |    +-- Policy
  |    +-- Approval
  |    +-- Maestro
  |
  +-- Brothers
       +-- Engenharia
       +-- Financeiro
       +-- Pesquisa
       +-- Marketing
       +-- Comercial
