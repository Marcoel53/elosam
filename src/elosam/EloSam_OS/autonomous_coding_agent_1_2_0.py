import json
import re
import uuid


class AutonomousCodingAgent:
    """
    Agente autônomo de codificação do EloSam OS.

    Fluxo:
    - recebe uma missão em linguagem natural;
    - solicita um plano de código ao modelo local;
    - valida estruturalmente o plano;
    - corrige autonomamente planos inválidos;
    - entrega o plano ao CodingAgent;
    - observa compilação e execução;
    - se houver falha, envia os erros ao modelo;
    - solicita uma versão corrigida do projeto;
    - repete até concluir ou atingir o limite.

    O modelo nunca escreve diretamente no disco.
    Toda materialização passa pelo CodingAgent
    e pelo CodingWorkspace.
    """

    VERSION = "1.2.0"

    SYSTEM_PROMPT = """
Você é o Coding Worker do EloSam OS.

Sua tarefa é transformar uma missão de programação
em um pequeno projeto Python funcional.

REGRAS OBRIGATÓRIAS:

1. Retorne somente um objeto JSON válido.
2. Não use markdown.
3. Não use blocos com crases.
4. Não inclua explicações fora do JSON.
5. Gere apenas arquivos Python.
6. Use somente a biblioteca padrão do Python.
7. Não use rede.
8. Não use subprocess.
9. Não use os, pathlib ou shutil.
10. Não leia arquivos externos.
11. Não escreva arquivos por conta própria.
12. Não use input().
13. O programa deve executar sem interação humana.
14. O programa principal deve demonstrar seu uso
    usando valores definidos no próprio código.
15. Inclua pelo menos um arquivo de teste executável.
16. Os testes devem validar a missão solicitada.
17. TODO arquivo citado em validation_files deve
    existir na lista files.
18. TODO arquivo citado em execution_files deve
    existir na lista files.
19. Antes de responder, confira se os nomes dos
    arquivos são exatamente iguais em toda a resposta.
20. Quando estiver corrigindo uma falha, devolva
    o projeto completo corrigido, não apenas trechos.
21. Preserve os requisitos da missão original.
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
Não use caminhos absolutos.
Não use .. nos caminhos.
"""

    def __init__(
        self,
        *,
        model_provider,
        coding_agent,
        logger=None,
        max_plan_attempts=3,
        max_execution_attempts=3,
    ):
        self.model_provider = model_provider
        self.coding_agent = coding_agent
        self.logger = logger
        self.max_plan_attempts = max_plan_attempts
        self.max_execution_attempts = (
            max_execution_attempts
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
                "Caminho de arquivo inválido."
            )

        if not re.fullmatch(
            r"[A-Za-z0-9_-]+\.py",
            path,
        ):
            raise ValueError(
                "O modelo retornou um caminho "
                f"de arquivo não permitido: {path}"
            )

    def _validate_plan(
        self,
        plan,
    ):
        if not isinstance(plan, dict):
            raise ValueError(
                "O plano do modelo não é "
                "um objeto JSON."
            )

        files = plan.get(
            "files"
        )

        if not isinstance(files, list):
            raise ValueError(
                "O plano não contém "
                "uma lista de arquivos."
            )

        if not files:
            raise ValueError(
                "O plano não contém arquivos."
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
                    "Especificação de arquivo "
                    "inválida."
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
                    "Conteúdo de arquivo inválido: "
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
                "O plano não definiu "
                "arquivos para validação."
            )

        if not execution_files:
            raise ValueError(
                "O plano não definiu "
                "arquivos para execução."
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
                    "validação ou execução "
                    "não existe no plano: "
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
            "MISSÃO DE PROGRAMAÇÃO:\n\n"
            f"{mission}\n\n"
            "Gere o projeto completo.\n"
            "O programa deve executar "
            "sem qualquer entrada do usuário.\n"
            "Não use input().\n"
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
            "MISSÃO ORIGINAL:\n"
            f"{mission}\n\n"
            "ERRO DE VALIDAÇÃO:\n"
            f"{validation_error}\n\n"
            "PLANO INVÁLIDO:\n"
            f"{invalid_plan_text}\n\n"
            "Corrija o projeto completo.\n"
            "Retorne somente um novo objeto "
            "JSON completo e válido."
        )

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
                f"{phase}: geração de plano "
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

                attempts.append(
                    {
                        "attempt":
                            attempt_number,
                        "status":
                            "VALID",
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
                        "O modelo não conseguiu "
                        "gerar um plano válido "
                        f"após {self.max_plan_attempts} "
                        "tentativas. "
                        f"Último erro: {error_text}"
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
            "Falha inesperada na geração "
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
            "uma missão do EloSam OS, mas falhou "
            "na validação ou execução.\n\n"
            "MISSÃO ORIGINAL:\n"
            f"{mission}\n\n"
            "PROJETO ATUAL:\n"
            f"{current_plan_text}\n\n"
            "FALHAS REAIS CAPTURADAS:\n"
            f"{failures_text}\n\n"
            "Analise a causa real das falhas.\n"
            "Corrija o projeto completo.\n"
            "Não use input().\n"
            "O programa deve executar sem "
            "interação humana.\n"
            "Preserve os requisitos da missão.\n"
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
                "A missão deve ser texto."
            )

        mission = mission.strip()

        if not mission:
            raise ValueError(
                "A missão não pode estar vazia."
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
                "Execução autônoma: "
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
                    "concluiu a missão: "
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
                "Solicitando correção autônoma."
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
            "sem conclusão após o limite "
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
            "model_provider":
                self.model_provider.status(),
            "coding_agent":
                self.coding_agent.status(),
        }