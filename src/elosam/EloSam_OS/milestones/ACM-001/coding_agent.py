class CodingAgent:
    """
    Agente de codificação do EloSam OS.

    Responsabilidades:
    - receber um plano estruturado de arquivos;
    - escrever código no Coding Workspace;
    - validar arquivos Python;
    - executar arquivos quando solicitado;
    - devolver o resultado da missão.
    """

    VERSION = "1.0.0"

    def __init__(
        self,
        workspace,
        logger=None,
    ):
        self.workspace = workspace
        self.logger = logger

    def _log(
        self,
        message,
    ):
        if self.logger is not None:
            self.logger.info(message)

    def execute_plan(
        self,
        *,
        mission_id,
        files,
        validation_files=None,
        execution_files=None,
    ):
        self._log(
            f"Coding Agent iniciou: {mission_id}"
        )

        created_files = []
        validations = []
        executions = []

        for file_spec in files:
            relative_path = (
                f"{mission_id}/"
                f"{file_spec['path']}"
            )

            result = self.workspace.write_text(
                relative_path,
                file_spec["content"],
            )

            created_files.append(
                result
            )

        for file_path in (
            validation_files or []
        ):
            relative_path = (
                f"{mission_id}/"
                f"{file_path}"
            )

            result = (
                self.workspace.compile_python(
                    relative_path
                )
            )

            validations.append(
                {
                    "file": file_path,
                    **result,
                }
            )

        for file_path in (
            execution_files or []
        ):
            relative_path = (
                f"{mission_id}/"
                f"{file_path}"
            )

            result = (
                self.workspace.run_python(
                    relative_path
                )
            )

            executions.append(
                {
                    "file": file_path,
                    **result,
                }
            )

        validation_success = all(
            item["success"]
            for item in validations
        )

        execution_success = all(
            item["success"]
            for item in executions
        )

        success = (
            validation_success
            and execution_success
        )

        status = (
            "COMPLETED"
            if success
            else "FAILED"
        )

        self._log(
            "Coding Agent terminou: "
            f"{mission_id} "
            f"status={status}"
        )

        return {
            "mission_id": mission_id,
            "status": status,
            "created_files": created_files,
            "validations": validations,
            "executions": executions,
            "files": self.workspace.list_files(
                mission_id
            ),
        }

    def status(self):
        return {
            "version": self.VERSION,
            "workspace": (
                self.workspace.status()
            ),
        }