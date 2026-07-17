from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from app.plugins.models import Plugin
from app.plugins.plugin_loader import PluginLoader
from app.plugins.plugin_registry import PluginRegistry


class DynamicLoader:
    """
    Enterprise Dynamic Plugin Loader

    Responsibilities
    ----------------
    • Discover plugins
    • Auto-load plugins
    • Register plugins
    • Hot reload plugins
    • Unload plugins
    • Refresh plugin directory
    """

    def __init__(
        self,
        loader: Optional[PluginLoader] = None,
        registry: Optional[PluginRegistry] = None,
    ):

        self.loader = loader or PluginLoader()

        self.registry = registry or PluginRegistry()

    # -------------------------------------------------
    # Discovery
    # -------------------------------------------------

    def discover(
        self,
        plugin_directory: str,
    ) -> List[str]:

        return self.loader.discover(
            plugin_directory
        )

    # -------------------------------------------------
    # Load Single Plugin
    # -------------------------------------------------

    def load(
        self,
        path: str,
        overwrite: bool = False,
    ) -> Plugin:

        plugin = self.loader.load_file(path)

        self.registry.register(
            plugin,
            overwrite=overwrite,
        )

        return plugin

    # -------------------------------------------------
    # Load All Plugins
    # -------------------------------------------------

    def load_all(
        self,
        plugin_directory: str,
        overwrite: bool = False,
    ) -> List[Plugin]:

        plugins: List[Plugin] = []

        for file in self.loader.discover(
            plugin_directory
        ):

            try:

                plugin = self.loader.load_file(
                    file
                )

                self.registry.register(
                    plugin,
                    overwrite=overwrite,
                )

                plugins.append(plugin)

            except Exception:

                continue

        return plugins

    # -------------------------------------------------
    # Reload Plugin
    # -------------------------------------------------

    def reload(
        self,
        name: str,
    ) -> Plugin:

        plugin = self.loader.reload(
            name
        )

        self.registry.register(
            plugin,
            overwrite=True,
        )

        return plugin

    # -------------------------------------------------
    # Unload Plugin
    # -------------------------------------------------

    def unload(
        self,
        name: str,
    ) -> bool:

        unloaded = self.loader.unload(
            name
        )

        if unloaded:

            self.registry.unregister(
                name
            )

        return unloaded

    # -------------------------------------------------
    # Refresh Directory
    # -------------------------------------------------

    def refresh(
        self,
        plugin_directory: str,
    ) -> List[Plugin]:

        loaded = []

        discovered = self.loader.discover(
            plugin_directory
        )

        existing = {

            plugin.metadata.name

            for plugin

            in self.registry.all()

        }

        for file in discovered:

            try:

                plugin = self.loader.load_file(
                    file
                )

                if (
                    plugin.metadata.name
                    not in existing
                ):

                    self.registry.register(
                        plugin
                    )

                    loaded.append(plugin)

            except Exception:

                continue

        return loaded

    # -------------------------------------------------
    # Lookup
    # -------------------------------------------------

    def plugin(
        self,
        name: str,
    ) -> Optional[Plugin]:

        return self.registry.get(
            name
        )

    def plugins(
        self,
    ) -> List[Plugin]:

        return self.registry.all()

    # -------------------------------------------------
    # Counts
    # -------------------------------------------------

    def count(self) -> int:

        return len(self.registry)

    def empty(self) -> bool:

        return self.count() == 0

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(self) -> dict:

        return {

            "plugins": self.registry.export()[
                "plugins"
            ]

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(self):

        for plugin in self.registry.all():

            self.loader.unload(
                plugin.metadata.name
            )

        self.registry.clear()

    # -------------------------------------------------
    # Directory Exists
    # -------------------------------------------------

    @staticmethod
    def exists(
        plugin_directory: str,
    ) -> bool:

        return Path(
            plugin_directory
        ).exists()

    # -------------------------------------------------
    # Empty Instance
    # -------------------------------------------------

    @staticmethod
    def empty_loader():

        return DynamicLoader()