import json
import re
import uuid

from .code_guard import CodeGuard


class AutonomousCodingAgent:
    """
    Agente autÃ´nomo de codificaÃ§Ã£o do EloSam OS.

    Fluxo:
    - recebe uma missÃ£o em linguagem natural;
    - solicita um plano de cÃ³digo ao modelo local;
    - valida estruturalmente o plano;
    - corrige autonomamente planos invÃ¡lidos;
    - entrega o plano ao CodingAgent;
    - observa compilaÃ§Ã£o e execuÃ§Ã£o;
    - se houver falha, envia os erros ao modelo;
    - solicita uma versÃ£o corrigida do projeto;
    - repete atÃ© concluir ou atingir o limite.

    O modelo nunca escreve diretamente no disco.
    Toda materializaÃ§Ã£o passa pelo CodingAgent
    e pelo CodingWorkspace.
    """

    VERSION = "1.3.1"

    SYSTEM_PROMPT = """
VocÃª Ã© o Coding Worker do EloSam OS.

Sua tarefa Ã© transformar uma missÃ£o de programaÃ§Ã£o
em um pequeno projeto Python funcional.

REGRAS OBRIGATÃ“RIAS:

1. Retorne somente um objeto JSON vÃ¡lido.
2. NÃ£o use markdown.
3. NÃ£o use blocos com crases.
4. NÃ£o inclua explicaÃ§Ãµes fora do JSON.
5. Gere apenas arquivos Python.
6. Use somente a biblioteca padrÃ£o do Python.
7. NÃ£o use rede.
8. NÃ£o use subprocess.
9. NÃ£o use os, pathlib ou shutil.
10. NÃ£o leia arquivos externos.
11. NÃ£o escreva arquivos por conta prÃ³pria.
12. NÃ£o use input().
13. O programa deve executar sem interaÃ§Ã£o humana.
14. O programa principal deve demonstrar seu uso
    usando valores definidos no prÃ³prio cÃ³digo.
15. Inclua pelo menos um arquivo de teste executÃ¡vel.
16. Os testes devem validar a missÃ£o solicitada.
17. TODO arquivo citado em validation_files deve
    existir na lista files.
18. TODO arquivo citado em execution_files deve
    existir na lista files.
19. Antes de responder, confira se os nomes dos
    arquivos sÃ£o exatamente iguais em toda a resposta.
20. Quando estiver corrigindo uma falha, devolva
    o projeto completo corrigido, nÃ£o apenas trechos.
21. Preserve os requisitos da missÃ£o original.
22. Corrija a causa real do erro informado.

O JSON deve possuir exatamente esta estrutura:

{
    "summary": "resumo curto",
    "files": [
        {
            "path": "arquivo.py",
            "content": "codigo Python completo"
        },
        {
            "path": "test_arquivo.py",
            "content": "testes Python completos"
        }
    ],
    "validation_files": [
        "arquivo.py",
        "test_arquivo.py"
    ],
    "execution_files": [
        "arquivo.py",
        "test_arquivo.py"
    ]
}

Todos os caminhos devem ser nomes de arquivos simples.
NÃ£o use caminhos absolutos.
NÃ£o use .. nos caminhos.
"""

    def __init__(
        self,
        *,
        model_provider,
        coding_agent,
        logger=None,
        max_plan_attempts=3,
        max_execution_attempts=3,
        code_guard=None,
    ):
        self.model_provider = model_provider
        self.coding_agent = coding_agent
        self.logger = logger
        self.max_plan_attempts = max_plan_attempts
        self.max_execution_attempts = (
            max_execution_attempts
        )
        self.code_guard = (
            code_guard
            or CodeGuard(
                logger=logger
            )
        )

    def _log(
        self,
        message,
    ):
        if self.logger is not None:
            self.logger.info(message)

    def _create_mission_id(self):
        return (
            "autonomous_"
            f"{uuid.uuid4().hex[:12]}"
        )

    def _validate_file_path(
        self,
        path,
    ):
        if not isinstance(path, str):
            raise ValueError(
                "Caminho de arquivo invÃ¡lido."
            )

        if not re.fullmatch(
            r"[A-Za-z0-9_-]+\.py",
            path,
        ):
            raise ValueError(
                "O modelo retornou um caminho "
                f"de arquivo nÃ£o permitido: {path}"
            )

    def _validate_plan(
        self,
        plan,
    ):
        if not isinstance(plan, dict):
            raise ValueError(
                "O plano do modelo nÃ£o Ã© "
                "um objeto JSON."
            )

        files = plan.get(
            "files"
        )

        if not isinstance(files, list):
            raise ValueError(
                "O plano nÃ£o contÃ©m "
                "uma lista de arquivos."
            )

        if not files:
            raise ValueError(
                "O plano nÃ£o contÃ©m arquivos."
            )

        if len(files) > 10:
            raise ValueError(
                "O plano excedeu o limite "
                "de 10 arquivos."
            )

        known_paths = set()
        validated_files = []

        for file_spec in files:
            if not isinstance(
                file_spec,
                dict,
            ):
                raise ValueError(
                    "EspecificaÃ§Ã£o de arquivo "
                    "invÃ¡lida."
                )

            path = file_spec.get(
                "path"
            )

            content = file_spec.get(
                "content"
            )

            self._validate_file_path(
                path
            )

            if path in known_paths:
                raise ValueError(
                    "Arquivo duplicado no plano: "
                    f"{path}"
                )

            if not isinstance(
                content,
                str,
            ):
                raise ValueError(
                    "ConteÃºdo de arquivo invÃ¡lido: "
                    f"{path}"
                )

            if not content.strip():
                raise ValueError(
                    "Arquivo vazio no plano: "
                    f"{path}"
                )

            known_paths.add(
                path
            )

            validated_files.append(
                {
                    "path": path,
                    "content": content,
                }
            )

        validation_files = plan.get(
            "validation_files",
            [],
        )

        execution_files = plan.get(
            "execution_files",
            [],
        )

        if not isinstance(
            validation_files,
            list,
        ):
            raise ValueError(
                "validation_files deve "
                "ser uma lista."
            )

        if not isinstance(
            execution_files,
            list,
        ):
            raise ValueError(
                "execution_files deve "
                "ser uma lista."
            )

        if not validation_files:
            raise ValueError(
                "O plano nÃ£o definiu "
                "arquivos para validaÃ§Ã£o."
            )

        if not execution_files:
            raise ValueError(
                "O plano nÃ£o definiu "
                "arquivos para execuÃ§Ã£o."
            )

        for path in (
            validation_files
            + execution_files
        ):
            self._validate_file_path(
                path
            )

            if path not in known_paths:
                raise ValueError(
                    "Arquivo solicitado para "
                    "validaÃ§Ã£o ou execuÃ§Ã£o "
                    "nÃ£o existe no plano: "
                    f"{path}"
                )

        return {
            "summary": str(
                plan.get(
                    "summary",
                    "",
                )
            ),
            "files":
                validated_files,
            "validation_files":
                validation_files,
            "execution_files":
                execution_files,
        }

    def _build_initial_prompt(
        self,
        mission,
    ):
        return (
            "MISSÃƒO DE PROGRAMAÃ‡ÃƒO:\n\n"
            f"{mission}\n\n"
            "Gere o projeto completo.\n"
            "O programa deve executar "
            "sem qualquer entrada do usuÃ¡rio.\n"
            "NÃ£o use input().\n"
            "Retorne somente o JSON solicitado."
        )

    def _build_plan_repair_prompt(
        self,
        *,
        mission,
        invalid_plan,
        validation_error,
    ):
        invalid_plan_text = json.dumps(
            invalid_plan,
            ensure_ascii=False,
            indent=2,
        )

        return (
            "A resposta anterior foi rejeitada "
            "pelo validador do EloSam OS.\n\n"
            "MISSÃƒO ORIGINAL:\n"
            f"{mission}\n\n"
            "ERRO DE VALIDAÃ‡ÃƒO:\n"
            f"{validation_error}\n\n"
            "PLANO INVÃLIDO:\n"
            f"{invalid_plan_text}\n\n"
            "Corrija o projeto completo.\n"
            "Retorne somente um novo objeto "
            "JSON completo e vÃ¡lido."
        )

    def _format_guard_error(
        self,
        guard_report,
    ):
        lines = [
            "O CodeGuard rejeitou o projeto."
        ]

        for violation in guard_report.get(
            "violations",
            [],
        ):
            file_name = violation.get(
                "file",
                "<unknown>",
            )
            rule = violation.get(
                "rule",
                "unknown_rule",
            )
            message = violation.get(
                "message",
                "Violacao sem descricao.",
            )
            line = violation.get(
                "line"
            )

            location = file_name

            if line is not None:
                location = (
                    f"{location}:"
                    f"{line}"
                )

            lines.append(
                f"- {location} "
                f"[{rule}] "
                f"{message}"
            )

        lines.append(
            "Corrija todas as violacoes. "
            "O projeto completo corrigido "
            "sera analisado novamente antes "
            "de qualquer execucao."
        )

        return "\n".join(
            lines
        )

    def _build_guard_repair_prompt(
        self,
        *,
        mission,
        rejected_plan,
        guard_report,
    ):
        violations = []

        for violation in guard_report.get(
            "violations",
            [],
        ):
            file_name = violation.get(
                "file",
                "<unknown>",
            )
            rule = violation.get(
                "rule",
                "unknown_rule",
            )
            message = violation.get(
                "message",
                "Violacao sem descricao.",
            )
            line = violation.get(
                "line"
            )

            location = file_name

            if line is not None:
                location = (
                    f"{location}:"
                    f"{line}"
                )

            violations.append(
                f"- {location} "
                f"[{rule}] "
                f"{message}"
            )

        violations_text = "\n".join(
            violations
        )

        rejected_plan_json = json.dumps(
            rejected_plan,
            ensure_ascii=False,
            indent=2,
        )

        return f"""
O projeto abaixo foi REJEITADO pelo CodeGuard do EloSam.

MISSAO ORIGINAL:
{mission}

VIOLACOES DETECTADAS:
{violations_text}

PROJETO REJEITADO:
{rejected_plan_json}

ACAO OBRIGATORIA:

1. Corrija TODAS as violacoes detectadas.
2. Remova completamente qualquer chamada ou importacao proibida.
3. Se input() foi proibido:
   - remova TODAS as chamadas input();
   - nao use input() no programa;
   - nao use input() nos testes;
   - nao use mock, patch ou simulacao de input();
   - nao esconda input() dentro de outra funcao.
4. O programa deve executar automaticamente e terminar sozinho.
5. Para demonstracao, use um valor fixo no programa principal.
6. Os testes devem chamar diretamente as funcoes reutilizaveis.
7. Preserve todos os requisitos validos da missao original.
8. Retorne o PROJETO COMPLETO corrigido, incluindo todos os arquivos.
9. Retorne SOMENTE JSON valido.
10. Nao inclua markdown.
11. Nao inclua explicacoes fora do JSON.

IMPORTANTE:
O projeto corrigido sera analisado novamente pelo CodeGuard
ANTES de qualquer arquivo ser escrito ou executado.

Use exatamente esta estrutura:

{{
  "summary": "resumo curto",
  "files": [
    {{
      "path": "arquivo.py",
      "content": "codigo completo"
    }}
  ],
  "validation_files": [
    "arquivo.py"
  ],
  "execution_files": [
    "arquivo.py"
  ]
}}
""".strip()

    def _generate_valid_plan_from_prompt(
        self,
        *,
        mission,
        prompt,
        phase,
    ):
        attempts = []

        current_prompt = prompt

        for attempt_number in range(
            1,
            self.max_plan_attempts + 1,
        ):
            self._log(
                f"{phase}: geracao de plano "
                f"{attempt_number}/"
                f"{self.max_plan_attempts}"
            )

            raw_plan = (
                self.model_provider.generate_json(
                    current_prompt,
                    system=self.SYSTEM_PROMPT,
                    temperature=0.1,
                )
            )

            try:
                valid_plan = (
                    self._validate_plan(
                        raw_plan
                    )
                )

                guard_report = (
                    self.code_guard.analyze_plan(
                        valid_plan
                    )
                )

                if not guard_report[
                    "approved"
                ]:
                    guard_error = (
                        self._format_guard_error(
                            guard_report
                        )
                    )

                    attempts.append(
                        {
                            "attempt":
                                attempt_number,
                            "status":
                                "GUARD_REJECTED",
                            "error":
                                guard_error,
                            "guard_report":
                                guard_report,
                        }
                    )

                    if (
                        attempt_number
                        >= self.max_plan_attempts
                    ):
                        raise RuntimeError(
                            "O modelo nao conseguiu "
                            "gerar codigo aprovado "
                            "pelo CodeGuard apos "
                            f"{self.max_plan_attempts} "
                            "tentativas. "
                            f"Ultimo erro: "
                            f"{guard_error}"
                        )

                    current_prompt = (
                        self._build_guard_repair_prompt(
                            mission=mission,
                            rejected_plan=valid_plan,
                            guard_report=(
                                guard_report
                            ),
                        )
                    )

                    continue

                attempts.append(
                    {
                        "attempt":
                            attempt_number,
                        "status":
                            "VALID",
                        "guard_report":
                            guard_report,
                    }
                )

                return (
                    valid_plan,
                    attempts,
                )

            except ValueError as error:
                error_text = str(
                    error
                )

                attempts.append(
                    {
                        "attempt":
                            attempt_number,
                        "status":
                            "INVALID",
                        "error":
                            error_text,
                    }
                )

                if (
                    attempt_number
                    >= self.max_plan_attempts
                ):
                    raise RuntimeError(
                        "O modelo nao conseguiu "
                        "gerar um plano valido "
                        f"apos {self.max_plan_attempts} "
                        "tentativas. "
                        f"Ultimo erro: {error_text}"
                    ) from error

                current_prompt = (
                    self._build_plan_repair_prompt(
                        mission=mission,
                        invalid_plan=raw_plan,
                        validation_error=(
                            error_text
                        ),
                    )
                )

        raise RuntimeError(
            "Falha inesperada na geracao "
            "do plano."
        )

    def _collect_failures(
        self,
        execution,
    ):
        failures = []

        for validation in execution.get(
            "validations",
            [],
        ):
            if validation.get(
                "success"
            ):
                continue

            failures.append(
                {
                    "phase":
                        "validation",
                    "file":
                        validation.get(
                            "file"
                        ),
                    "returncode":
                        validation.get(
                            "returncode"
                        ),
                    "stdout":
                        validation.get(
                            "stdout",
                            "",
                        ),
                    "stderr":
                        validation.get(
                            "stderr",
                            "",
                        ),
                    "timed_out":
                        validation.get(
                            "timed_out",
                            False,
                        ),
                }
            )

        for item in execution.get(
            "executions",
            [],
        ):
            if item.get(
                "success"
            ):
                continue

            failures.append(
                {
                    "phase":
                        "execution",
                    "file":
                        item.get(
                            "file"
                        ),
                    "returncode":
                        item.get(
                            "returncode"
                        ),
                    "stdout":
                        item.get(
                            "stdout",
                            "",
                        ),
                    "stderr":
                        item.get(
                            "stderr",
                            "",
                        ),
                    "timed_out":
                        item.get(
                            "timed_out",
                            False,
                        ),
                }
            )

        return failures

    def _build_execution_repair_prompt(
        self,
        *,
        mission,
        current_plan,
        execution,
    ):
        current_plan_text = json.dumps(
            current_plan,
            ensure_ascii=False,
            indent=2,
        )

        failures = self._collect_failures(
            execution
        )

        failures_text = json.dumps(
            failures,
            ensure_ascii=False,
            indent=2,
        )

        return (
            "O projeto abaixo foi gerado para "
            "uma missÃ£o do EloSam OS, mas falhou "
            "na validaÃ§Ã£o ou execuÃ§Ã£o.\n\n"
            "MISSÃƒO ORIGINAL:\n"
            f"{mission}\n\n"
            "PROJETO ATUAL:\n"
            f"{current_plan_text}\n\n"
            "FALHAS REAIS CAPTURADAS:\n"
            f"{failures_text}\n\n"
            "Analise a causa real das falhas.\n"
            "Corrija o projeto completo.\n"
            "NÃ£o use input().\n"
            "O programa deve executar sem "
            "interaÃ§Ã£o humana.\n"
            "Preserve os requisitos da missÃ£o.\n"
            "Retorne TODOS os arquivos completos.\n"
            "Retorne somente o objeto JSON."
        )

    def run(
        self,
        mission,
        *,
        mission_id=None,
    ):
        if not isinstance(
            mission,
            str,
        ):
            raise ValueError(
                "A missÃ£o deve ser texto."
            )

        mission = mission.strip()

        if not mission:
            raise ValueError(
                "A missÃ£o nÃ£o pode estar vazia."
            )

        mission_id = (
            mission_id
            or self._create_mission_id()
        )

        self._log(
            "Autonomous Coding Agent iniciou: "
            f"{mission_id}"
        )

        initial_prompt = (
            self._build_initial_prompt(
                mission
            )
        )

        plan, planning_attempts = (
            self._generate_valid_plan_from_prompt(
                mission=mission,
                prompt=initial_prompt,
                phase="initial",
            )
        )

        execution_attempts = []

        for execution_attempt in range(
            1,
            self.max_execution_attempts + 1,
        ):
            self._log(
                "ExecuÃ§Ã£o autÃ´noma: "
                f"{execution_attempt}/"
                f"{self.max_execution_attempts}"
            )

            execution = (
                self.coding_agent.execute_plan(
                    mission_id=mission_id,
                    files=plan["files"],
                    validation_files=(
                        plan[
                            "validation_files"
                        ]
                    ),
                    execution_files=(
                        plan[
                            "execution_files"
                        ]
                    ),
                )
            )

            failures = self._collect_failures(
                execution
            )

            execution_attempts.append(
                {
                    "attempt":
                        execution_attempt,
                    "status":
                        execution["status"],
                    "failures":
                        failures,
                }
            )

            if (
                execution["status"]
                == "COMPLETED"
            ):
                result = {
                    "mission_id":
                        mission_id,
                    "mission":
                        mission,
                    "summary":
                        plan["summary"],
                    "planning_attempts":
                        planning_attempts,
                    "execution_attempts":
                        execution_attempts,
                    "generated_plan":
                        plan,
                    "execution":
                        execution,
                    "status":
                        "COMPLETED",
                }

                self._log(
                    "Autonomous Coding Agent "
                    "concluiu a missÃ£o: "
                    f"{mission_id}"
                )

                return result

            if (
                execution_attempt
                >= self.max_execution_attempts
            ):
                break

            self._log(
                "Falha detectada. "
                "Solicitando correÃ§Ã£o autÃ´noma."
            )

            repair_prompt = (
                self._build_execution_repair_prompt(
                    mission=mission,
                    current_plan=plan,
                    execution=execution,
                )
            )

            repaired_plan, repair_attempts = (
                self._generate_valid_plan_from_prompt(
                    mission=mission,
                    prompt=repair_prompt,
                    phase=(
                        "execution_repair_"
                        f"{execution_attempt}"
                    ),
                )
            )

            planning_attempts.extend(
                repair_attempts
            )

            plan = repaired_plan

        result = {
            "mission_id":
                mission_id,
            "mission":
                mission,
            "summary":
                plan["summary"],
            "planning_attempts":
                planning_attempts,
            "execution_attempts":
                execution_attempts,
            "generated_plan":
                plan,
            "execution":
                execution,
            "status":
                "FAILED",
        }

        self._log(
            "Autonomous Coding Agent encerrou "
            "sem conclusÃ£o apÃ³s o limite "
            "de tentativas: "
            f"{mission_id}"
        )

        return result

    def status(self):
        return {
            "version":
                self.VERSION,
            "max_plan_attempts":
                self.max_plan_attempts,
            "max_execution_attempts":
                self.max_execution_attempts,
            "code_guard":
                self.code_guard.status(),
            "model_provider":
                self.model_provider.status(),
            "coding_agent":
                self.coding_agent.status(),
        }
