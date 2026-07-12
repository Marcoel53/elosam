from .bundle_loader import BundleLoader
from .logger import create_logger
from .registry import CapabilityRegistry
from .resolver import CapabilityResolver
from .transport import TransportAdapter


class Kernel:
    VERSION = "Beta 1.0"

    def __init__(self, bundles_path="./bundles"):
        self.logger = create_logger("kernel")
        self.registry = CapabilityRegistry()
        self.resolver = CapabilityResolver(self.registry)
        self.transport = TransportAdapter()

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

        await self.loader.load_all()

        self.running = True

        self.logger.info(
            "ELOSAM OS: Kernel pronto."
        )

    async def shutdown(self):
        self.running = False
        self.logger.info(
            "ELOSAM OS: Kernel encerrado."
        )

    def status(self):
        return {
            "system": "EloSam OS",
            "version": self.VERSION,
            "status": "online" if self.running else "offline",
            "bundles": self.loader.loaded_bundles,
            "capabilities": self.registry.list_capabilities(),
        }
