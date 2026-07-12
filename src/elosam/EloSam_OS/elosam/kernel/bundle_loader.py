import importlib
import inspect
from pathlib import Path

import yaml

from .descriptors import CapabilityDescriptor


class BundleLoader:
    def __init__(
        self,
        path,
        registry,
        resolver,
        transport,
        logger,
        worker_runtime=None,
    ):
        self.path = Path(path)
        self.registry = registry
        self.resolver = resolver
        self.transport = transport
        self.logger = logger
        self.worker_runtime = worker_runtime
        self.loaded_bundles = []

    async def load_all(self):
        if not self.path.exists():
            self.logger.warning(
                "Pasta de bundles não encontrada."
            )
            return

        for bundle_dir in sorted(
            self.path.iterdir()
        ):
            if not bundle_dir.is_dir():
                continue

            manifest_path = (
                bundle_dir / "bundle.yaml"
            )

            if not manifest_path.exists():
                continue

            try:
                manifest = yaml.safe_load(
                    manifest_path.read_text(
                        encoding="utf-8"
                    )
                )

                bundle_name = manifest["name"]

                module = importlib.import_module(
                    f"bundles.{bundle_name}.main"
                )

                activate = getattr(
                    module,
                    "activate",
                    None,
                )

                if activate:
                    await self._activate_bundle(
                        activate
                    )

                for capability in manifest.get(
                    "provides",
                    [],
                ):
                    capability_name = (
                        capability["name"]
                    )

                    function_name = (
                        capability_name.replace(
                            ".",
                            "_",
                        )
                    )

                    implementation = getattr(
                        module,
                        function_name,
                        None,
                    )

                    if implementation is None:
                        self.logger.warning(
                            f"{capability_name}: "
                            "implementação ausente"
                        )
                        continue

                    descriptor = (
                        CapabilityDescriptor(
                            id=capability_name,
                            version=str(
                                capability.get(
                                    "version",
                                    "1.0",
                                )
                            ),
                            timeout=int(
                                capability.get(
                                    "timeout",
                                    60,
                                )
                            ),
                            retries=int(
                                capability.get(
                                    "retries",
                                    3,
                                )
                            ),
                            owner=capability.get(
                                "owner",
                                bundle_name,
                            ),
                            priority=int(
                                capability.get(
                                    "priority",
                                    0,
                                )
                            ),
                        )
                    )

                    self.registry.register(
                        descriptor,
                        implementation,
                    )

                self.loaded_bundles.append(
                    bundle_name
                )

                self.logger.info(
                    "Bundle carregado: "
                    f"{bundle_name}"
                )

            except Exception:
                self.logger.exception(
                    "Falha ao carregar bundle: "
                    f"{bundle_dir.name}"
                )

    async def _activate_bundle(
        self,
        activate,
    ):
        """
        Injeta apenas as dependências declaradas
        explicitamente pelo activate() do bundle.

        Mantém compatibilidade com bundles antigos.
        """

        available_dependencies = {
            "resolver": self.resolver,
            "transport": self.transport,
            "logger": self.logger,
            "worker_runtime":
                self.worker_runtime,
        }

        signature = inspect.signature(
            activate
        )

        kwargs = {}

        for parameter_name in (
            signature.parameters
        ):
            if (
                parameter_name
                in available_dependencies
            ):
                kwargs[parameter_name] = (
                    available_dependencies[
                        parameter_name
                    ]
                )

        result = activate(**kwargs)

        if inspect.isawaitable(result):
            await result