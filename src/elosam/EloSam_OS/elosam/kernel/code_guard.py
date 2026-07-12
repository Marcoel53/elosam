import ast


class CodeGuard:
    """
    Guarda determinístico de código do EloSam OS.

    Responsabilidades:
    - analisar código Python antes da execução;
    - detectar erros de sintaxe;
    - bloquear chamadas proibidas;
    - bloquear imports proibidos;
    - produzir relatório estruturado;
    - analisar todos os arquivos de um plano.

    O CodeGuard não modifica o código.
    Ele apenas analisa, aprova ou rejeita.
    """

    VERSION = "1.0.0"

    DEFAULT_FORBIDDEN_CALLS = {
        "input",
        "eval",
        "exec",
        "compile",
        "__import__",
    }

    DEFAULT_FORBIDDEN_IMPORTS = {
        "subprocess",
        "os",
        "pathlib",
        "shutil",
    }

    def __init__(
        self,
        *,
        forbidden_calls=None,
        forbidden_imports=None,
        logger=None,
    ):
        self.forbidden_calls = set(
            forbidden_calls
            or self.DEFAULT_FORBIDDEN_CALLS
        )

        self.forbidden_imports = set(
            forbidden_imports
            or self.DEFAULT_FORBIDDEN_IMPORTS
        )

        self.logger = logger

    def _log(
        self,
        message,
    ):
        if self.logger is not None:
            self.logger.info(
                message
            )

    @staticmethod
    def _violation(
        *,
        rule,
        message,
        line=None,
        column=None,
        symbol=None,
    ):
        return {
            "rule": rule,
            "message": message,
            "line": line,
            "column": column,
            "symbol": symbol,
        }

    @staticmethod
    def _root_name(
        module_name,
    ):
        if not module_name:
            return ""

        return module_name.split(
            ".",
            1,
        )[0]

    @staticmethod
    def _call_name(
        node,
    ):
        if isinstance(
            node,
            ast.Name,
        ):
            return node.id

        if isinstance(
            node,
            ast.Attribute,
        ):
            parts = []
            current = node

            while isinstance(
                current,
                ast.Attribute,
            ):
                parts.append(
                    current.attr
                )

                current = (
                    current.value
                )

            if isinstance(
                current,
                ast.Name,
            ):
                parts.append(
                    current.id
                )

            if parts:
                return ".".join(
                    reversed(
                        parts
                    )
                )

        return None

    def analyze_source(
        self,
        *,
        source,
        filename="<generated>",
    ):
        violations = []

        if not isinstance(
            source,
            str,
        ):
            violations.append(
                self._violation(
                    rule=(
                        "invalid_source"
                    ),
                    message=(
                        "O conteúdo do arquivo "
                        "não é texto."
                    ),
                )
            )

            return {
                "filename":
                    filename,
                "approved":
                    False,
                "violations":
                    violations,
            }

        try:
            tree = ast.parse(
                source,
                filename=filename,
            )

        except SyntaxError as error:
            violations.append(
                self._violation(
                    rule=(
                        "syntax_error"
                    ),
                    message=str(
                        error
                    ),
                    line=(
                        error.lineno
                    ),
                    column=(
                        error.offset
                    ),
                )
            )

            return {
                "filename":
                    filename,
                "approved":
                    False,
                "violations":
                    violations,
            }

        for node in ast.walk(
            tree
        ):
            if isinstance(
                node,
                ast.Import,
            ):
                for alias in node.names:
                    root_name = (
                        self._root_name(
                            alias.name
                        )
                    )

                    if (
                        root_name
                        in self.forbidden_imports
                    ):
                        violations.append(
                            self._violation(
                                rule=(
                                    "forbidden_import"
                                ),
                                message=(
                                    "Import proibido: "
                                    f"{alias.name}"
                                ),
                                line=getattr(
                                    node,
                                    "lineno",
                                    None,
                                ),
                                column=getattr(
                                    node,
                                    "col_offset",
                                    None,
                                ),
                                symbol=(
                                    alias.name
                                ),
                            )
                        )

            elif isinstance(
                node,
                ast.ImportFrom,
            ):
                root_name = (
                    self._root_name(
                        node.module
                    )
                )

                if (
                    root_name
                    in self.forbidden_imports
                ):
                    violations.append(
                        self._violation(
                            rule=(
                                "forbidden_import"
                            ),
                            message=(
                                "Import proibido: "
                                f"{node.module}"
                            ),
                            line=getattr(
                                node,
                                "lineno",
                                None,
                            ),
                            column=getattr(
                                node,
                                "col_offset",
                                None,
                            ),
                            symbol=(
                                node.module
                            ),
                        )
                    )

            elif isinstance(
                node,
                ast.Call,
            ):
                call_name = (
                    self._call_name(
                        node.func
                    )
                )

                if not call_name:
                    continue

                root_call = (
                    call_name.split(
                        ".",
                        1,
                    )[0]
                )

                if (
                    call_name
                    in self.forbidden_calls
                    or root_call
                    in self.forbidden_calls
                ):
                    violations.append(
                        self._violation(
                            rule=(
                                "forbidden_call"
                            ),
                            message=(
                                "Chamada proibida: "
                                f"{call_name}()"
                            ),
                            line=getattr(
                                node,
                                "lineno",
                                None,
                            ),
                            column=getattr(
                                node,
                                "col_offset",
                                None,
                            ),
                            symbol=(
                                call_name
                            ),
                        )
                    )

        approved = not violations

        self._log(
            "CodeGuard analisou "
            f"{filename}: "
            f"approved={approved}"
        )

        return {
            "filename":
                filename,
            "approved":
                approved,
            "violations":
                violations,
        }

    def analyze_plan(
        self,
        plan,
    ):
        reports = []

        files = plan.get(
            "files",
            [],
        )

        for file_spec in files:
            path = file_spec.get(
                "path",
                "<unknown>",
            )

            content = file_spec.get(
                "content",
                "",
            )

            report = (
                self.analyze_source(
                    source=content,
                    filename=path,
                )
            )

            reports.append(
                report
            )

        violations = []

        for report in reports:
            for violation in report[
                "violations"
            ]:
                violations.append(
                    {
                        "file":
                            report[
                                "filename"
                            ],
                        **violation,
                    }
                )

        approved = not violations

        return {
            "version":
                self.VERSION,
            "approved":
                approved,
            "files":
                reports,
            "violations":
                violations,
        }

    def status(
        self,
    ):
        return {
            "version":
                self.VERSION,
            "forbidden_calls":
                sorted(
                    self.forbidden_calls
                ),
            "forbidden_imports":
                sorted(
                    self.forbidden_imports
                ),
        }