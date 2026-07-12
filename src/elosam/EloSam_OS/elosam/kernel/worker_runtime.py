from datetime import datetime
from enum import Enum
import inspect
import uuid


class WorkerStatus(str, Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    DESTROYED = "DESTROYED"


class WorkerRuntime:
    """
    Runtime central de Workers temporários do EloSam OS.

    Responsabilidades:
    - criar Workers;
    - executar handlers;
    - registrar ciclo de vida;
    - armazenar resultados;
    - observar Workers ativos e históricos;
    - destruir Workers temporários.
    """

    VERSION = "1.0.0"

    def __init__(self, logger=None):
        self.logger = logger
        self._active = {}
        self._history = {}

    @staticmethod
    def _now():
        return datetime.now().isoformat(
            timespec="seconds"
        )

    def _log(self, message):
        if self.logger is not None:
            self.logger.info(message)

    def create(
        self,
        *,
        name,
        role,
        task,
        metadata=None,
    ):
        worker_id = str(uuid.uuid4())

        worker = {
            "id": worker_id,
            "name": name,
            "role": role,
            "task": task,
            "status": WorkerStatus.CREATED.value,
            "metadata": dict(metadata or {}),
            "created_at": self._now(),
            "started_at": None,
            "completed_at": None,
            "destroyed_at": None,
            "result": None,
            "error": None,
            "events": [],
        }

        self._add_event(
            worker,
            "worker.created",
            f"{name} criado.",
        )

        self._active[worker_id] = worker

        self._log(
            f"Worker criado: {name} [{worker_id}]"
        )

        return worker

    async def execute(
        self,
        worker,
        handler,
        *args,
        **kwargs,
    ):
        worker_id = worker["id"]

        if worker_id not in self._active:
            raise RuntimeError(
                "Worker não está ativo no runtime."
            )

        worker["status"] = WorkerStatus.RUNNING.value
        worker["started_at"] = self._now()

        self._add_event(
            worker,
            "worker.started",
            f"{worker['name']} iniciou.",
        )

        self._log(
            "Worker executando: "
            f"{worker['name']} [{worker_id}]"
        )

        try:
            result = handler(
                *args,
                **kwargs,
            )

            if inspect.isawaitable(result):
                result = await result

            worker["result"] = result
            worker["status"] = (
                WorkerStatus.COMPLETED.value
            )
            worker["completed_at"] = self._now()

            self._add_event(
                worker,
                "worker.completed",
                f"{worker['name']} concluído.",
            )

            self._log(
                "Worker concluído: "
                f"{worker['name']} [{worker_id}]"
            )

            return result

        except Exception as error:
            worker["status"] = (
                WorkerStatus.FAILED.value
            )
            worker["error"] = str(error)
            worker["completed_at"] = self._now()

            self._add_event(
                worker,
                "worker.failed",
                (
                    f"{worker['name']} falhou: "
                    f"{error}"
                ),
            )

            self._log(
                "Worker falhou: "
                f"{worker['name']} [{worker_id}]"
            )

            raise

    def destroy(
        self,
        worker_id,
    ):
        worker = self._active.pop(
            worker_id,
            None,
        )

        if worker is None:
            return None

        previous_status = worker["status"]

        worker["metadata"]["final_status"] = (
            previous_status
        )

        worker["status"] = (
            WorkerStatus.DESTROYED.value
        )
        worker["destroyed_at"] = self._now()

        self._add_event(
            worker,
            "worker.destroyed",
            f"{worker['name']} destruído.",
        )

        self._history[worker_id] = worker

        self._log(
            "Worker destruído: "
            f"{worker['name']} [{worker_id}]"
        )

        return worker

    def get(
        self,
        worker_id,
    ):
        worker = self._active.get(
            worker_id
        )

        if worker is not None:
            return worker

        return self._history.get(
            worker_id
        )

    def list_active(self):
        return list(
            self._active.values()
        )

    def list_history(self):
        return list(
            self._history.values()
        )

    def status(self):
        return {
            "version": self.VERSION,
            "active_workers": len(
                self._active
            ),
            "historical_workers": len(
                self._history
            ),
        }

    def _add_event(
        self,
        worker,
        event_type,
        message,
    ):
        worker["events"].append(
            {
                "time": self._now(),
                "type": event_type,
                "message": message,
            }
        )