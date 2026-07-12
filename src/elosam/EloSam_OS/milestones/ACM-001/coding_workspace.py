from pathlib import Path
import subprocess
import sys
import uuid


class CodingWorkspace:
    """
    Workspace isolado para missões de desenvolvimento
    do EloSam OS.

    Responsabilidades:
    - criar áreas de trabalho por missão;
    - restringir acesso à raiz do workspace;
    - criar e escrever arquivos;
    - ler arquivos;
    - listar arquivos;
    - compilar código Python;
    - executar programas Python sem interação humana.
    """

    VERSION = "1.1.0"

    def __init__(
        self,
        root="./workspace",
    ):
        self.root = Path(root).resolve()

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def create_mission_workspace(
        self,
        name=None,
    ):
        workspace_id = (
            name
            or f"mission_{uuid.uuid4().hex[:12]}"
        )

        path = self._safe_path(
            workspace_id
        )

        path.mkdir(
            parents=True,
            exist_ok=False,
        )

        return {
            "id": workspace_id,
            "path": str(path),
        }

    def _safe_path(
        self,
        relative_path,
    ):
        candidate = (
            self.root
            / relative_path
        ).resolve()

        try:
            candidate.relative_to(
                self.root
            )

        except ValueError as error:
            raise PermissionError(
                "Acesso fora do workspace negado."
            ) from error

        return candidate

    def write_text(
        self,
        relative_path,
        content,
    ):
        path = self._safe_path(
            relative_path
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

        return {
            "path": str(path),
            "bytes": len(
                content.encode("utf-8")
            ),
        }

    def read_text(
        self,
        relative_path,
    ):
        path = self._safe_path(
            relative_path
        )

        return path.read_text(
            encoding="utf-8"
        )

    def list_files(
        self,
        relative_path=".",
    ):
        path = self._safe_path(
            relative_path
        )

        if not path.exists():
            return []

        return [
            str(
                item.relative_to(
                    self.root
                )
            )
            for item in path.rglob("*")
            if item.is_file()
        ]

    def compile_python(
        self,
        relative_path,
        timeout=30,
    ):
        path = self._safe_path(
            relative_path
        )

        try:
            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "py_compile",
                    str(path),
                ],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(path.parent),
            )

            return {
                "success":
                    process.returncode == 0,
                "returncode":
                    process.returncode,
                "stdout":
                    process.stdout,
                "stderr":
                    process.stderr,
                "timed_out":
                    False,
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "returncode": None,
                "stdout": "",
                "stderr": (
                    "Compilação excedeu "
                    f"o limite de {timeout} segundos."
                ),
                "timed_out": True,
            }

    def run_python(
        self,
        relative_path,
        timeout=10,
        stdin_text="",
    ):
        path = self._safe_path(
            relative_path
        )

        try:
            process = subprocess.run(
                [
                    sys.executable,
                    str(path),
                ],
                input=stdin_text,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(path.parent),
            )

            return {
                "success":
                    process.returncode == 0,
                "returncode":
                    process.returncode,
                "stdout":
                    process.stdout,
                "stderr":
                    process.stderr,
                "timed_out":
                    False,
            }

        except subprocess.TimeoutExpired as error:
            stdout = error.stdout or ""
            stderr = error.stderr or ""

            if isinstance(stdout, bytes):
                stdout = stdout.decode(
                    "utf-8",
                    errors="replace",
                )

            if isinstance(stderr, bytes):
                stderr = stderr.decode(
                    "utf-8",
                    errors="replace",
                )

            return {
                "success": False,
                "returncode": None,
                "stdout": stdout,
                "stderr": (
                    stderr
                    + "\nExecução excedeu "
                    f"o limite de {timeout} segundos."
                ).strip(),
                "timed_out": True,
            }

    def status(self):
        return {
            "version": self.VERSION,
            "root": str(self.root),
        }