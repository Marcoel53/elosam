import importlib
from pathlib import Path

import yaml

from .descriptors import CapabilityDescriptor


class BundleLoader:
    def __init__(self, path, registry, resolver, transport, logger):
        self.path = Path(path)
        self.registry = registry
        self.resolver = resolver
        self.transport = transport
        self.logger = logger
        self.loaded_bundles = []

    async def load_all(self):
        if not self.path.exists():
            self.logger.warning("Pasta de bundles nÃ£o encontrada.")
            return

        for bundle_dir in sorted(self.path.iterdir()):
            if not bundle_dir.is_dir():
                continue

            manifest_path = bundle_dir / "bundle.yaml"

            if not manifest_path.exists():
                continue

            try:
                manifest = yaml.safe_load(
                    manifest_path.read_text(encoding="utf-8")
                )

                bundle_name = manifest["name"]
                module = importlib.import_module(
                    f"bundles.{bundle_name}.main"
                )

                activate = getattr(module, "activate", None)

                if activate:
                    await activate(
                        self.resolver,
                        self.transport,
                        self.logger,
                    )

                for capability in manifest.get("provides", []):
                    capability_name = capability["name"]

                    function_name = capability_name.replace(".", "_")
                    implementation = getattr(
                        module,
                        function_name,
                        None,
                    )

                    if implementation is None:
                        self.logger.warning(
                            f"{capability_name}: implementaÃ§Ã£o ausente"
                        )
                        continue

                    descriptor = CapabilityDescriptor(
                        id=capability_name,
                        version=str(
                            capability.get("version", "1.0")
                        ),
                        timeout=int(
                            capability.get("timeout", 60)
                        ),
                        retries=int(
                            capability.get("retries", 3)
                        ),
                        owner=capability.get(
                            "owner",
                            bundle_name,
                        ),
                        priority=int(
                            capability.get("priority", 0)
                        ),
                    )

                    self.registry.register(
                        descriptor,
                        implementation,
                    )

                self.loaded_bundles.append(bundle_name)

                self.logger.info(
                    f"Bundle carregado: {bundle_name}"
                )

            except Exception:
                self.logger.exception(
                    f"Falha ao carregar bundle: {bundle_dir.name}"
                )
