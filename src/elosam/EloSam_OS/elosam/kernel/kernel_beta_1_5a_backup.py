from .bundle_loader import BundleLoader
from .logger import create_logger
from .registry import CapabilityRegistry
from .resolver import CapabilityResolver
from .transport import TransportAdapter
from .worker_runtime import WorkerRuntime


class Kernel:
    VERSION = "Beta 1.5"

    def __init__(
        self,
        bundles_path="./bundles",
    ):
        self.logger = create_logger(
            "kernel"
        )

        self.registry = CapabilityRegistry()

        self.resolver = CapabilityResolver(
            self.registry
        )

        self.transport = TransportAdapter()

        self.worker_runtime = WorkerRuntime(
            logger=self.logger
        )

        self.loader = BundleLoader(
            bundles_path,
            self.registry,
            self.resolver,
            self.transport,
            self.logger,
        )

        self.running = False

    async def boot(self):
        if self.running:
            return

        self.logger.info(
            "ELOSAM OS: inicializando Kernel..."
        )

        self.logger.info(
            "Worker Runtime: ONLINE."
        )

        await self.loader.load_all()

        self.running = True

        self.logger.info(
            "ELOSAM OS: Kernel pronto."
        )

    async def shutdown(self):
        active_workers = (
            self.worker_runtime.list_active()
        )

        for worker in active_workers:
            self.worker_runtime.destroy(
                worker["id"]
            )

        self.running = False

        self.logger.info(
            "ELOSAM OS: Kernel encerrado."
        )

    def status(self):
        return {
            "system": "EloSam OS",
            "version": self.VERSION,
            "status": (
                "online"
                if self.running
                else "offline"
            ),
            "bundles":
                self.loader.loaded_bundles,
            "capabilities":
                self.registry.list_capabilities(),
            "worker_runtime":
                self.worker_runtime.status(),
        }
