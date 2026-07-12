class WorkerOrchestrator:
    """
    Orquestrador central de Workers do EloSam OS.

    Responsabilidades:
    - criar Workers através do Worker Runtime;
    - executar Workers com garantia de destruição;
    - compartilhar contexto entre etapas;
    - coletar resultados;
    - produzir snapshots do ciclo de vida;
    - executar pipelines de Workers.
    """

    VERSION = "1.0.0"

    def __init__(
        self,
        worker_runtime,
        logger=None,
    ):
        self.worker_runtime = worker_runtime
        self.logger = logger

    def _log(
        self,
        message,
    ):
        if self.logger is not None:
            self.logger.info(message)

    @staticmethod
    def _snapshot(
        worker,
    ):
        snapshot = dict(worker)

        snapshot["metadata"] = dict(
            worker.get(
                "metadata",
                {},
            )
        )

        snapshot["events"] = [
            dict(event)
            for event in worker.get(
                "events",
                []
            )
        ]

        return snapshot

    async def run_worker(
        self,
        *,
        name,
        role,
        task,
        handler,
        goal,
        context,
        metadata=None,
    ):
        worker_metadata = dict(
            metadata or {}
        )

        worker_metadata.setdefault(
            "temporary",
            True,
        )

        worker = self.worker_runtime.create(
            name=name,
            role=role,
            task=task,
            metadata=worker_metadata,
        )

        self._log(
            "Orchestrator iniciou Worker: "
            f"{name}"
        )

        try:
            result = (
                await self.worker_runtime.execute(
                    worker,
                    handler,
                    goal,
                    context,
                )
            )

            snapshot = self._snapshot(
                worker
            )

            return {
                "result": result,
                "worker": snapshot,
            }

        finally:
            self.worker_runtime.destroy(
                worker["id"]
            )

            self._log(
                "Orchestrator finalizou Worker: "
                f"{name}"
            )

    async def run_pipeline(
        self,
        *,
        goal,
        steps,
        context=None,
        metadata=None,
    ):
        shared_context = dict(
            context or {}
        )

        shared_context.setdefault(
            "goal",
            goal,
        )

        workers = []
        results = {}

        for index, step in enumerate(
            steps,
            start=1,
        ):
            key = step["key"]

            step_metadata = dict(
                metadata or {}
            )

            step_metadata.update(
                step.get(
                    "metadata",
                    {},
                )
            )

            step_metadata["pipeline_step"] = (
                index
            )

            execution = await self.run_worker(
                name=step["name"],
                role=step["role"],
                task=step["task"],
                handler=step["handler"],
                goal=goal,
                context=shared_context,
                metadata=step_metadata,
            )

            result = execution["result"]
            worker = execution["worker"]

            results[key] = result
            shared_context[key] = result
            workers.append(worker)

        return {
            "goal": goal,
            "status": "COMPLETED",
            "workers": workers,
            "results": results,
            "context": shared_context,
        }

    def status(self):
        return {
            "version": self.VERSION,
            "runtime_version": (
                self.worker_runtime.VERSION
            ),
        }