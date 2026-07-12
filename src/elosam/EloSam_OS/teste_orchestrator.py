import asyncio

from elosam.kernel.worker_orchestrator import WorkerOrchestrator
from elosam.kernel.worker_runtime import WorkerRuntime


def worker_one(goal, context):
    return {
        "message": "Worker 1 executado",
        "goal": goal,
    }


def worker_two(goal, context):
    return {
        "message": "Worker 2 executado",
        "received_worker_one": context.get("worker_one"),
    }


async def main():
    runtime = WorkerRuntime()

    orchestrator = WorkerOrchestrator(
        worker_runtime=runtime
    )

    result = await orchestrator.run_pipeline(
        goal="Validar Worker Orchestrator",
        steps=[
            {
                "key": "worker_one",
                "name": "Worker Teste 1",
                "role": "test_one",
                "task": "Executar etapa 1",
                "handler": worker_one,
            },
            {
                "key": "worker_two",
                "name": "Worker Teste 2",
                "role": "test_two",
                "task": "Executar etapa 2",
                "handler": worker_two,
            },
        ],
        metadata={
            "test": True,
        },
    )

    print("STATUS:", result["status"])
    print("WORKERS:", len(result["workers"]))
    print(
        "RESULTADOS:",
        list(result["results"].keys()),
    )
    print(
        "ATIVOS:",
        runtime.status()["active_workers"],
    )
    print(
        "HISTORICOS:",
        runtime.status()["historical_workers"],
    )
    print(
        "CONTEXTO COMPARTILHADO:",
        result["results"]["worker_two"][
            "received_worker_one"
        ]
        is not None,
    )


asyncio.run(main())