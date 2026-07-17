from __future__ import annotations

from typing import List, Optional

from app.plugins.dynamic_loader import DynamicLoader
from app.plugins.models import Plugin, PluginPermission, PluginStatus
from app.plugins.plugin_registry import PluginRegistry
from app.plugins.sandbox import PluginSandbox
from app.plugins.version_manager import VersionManager


class PluginManager:
    """
    Enterprise Plugin Manager

    High-level facade for the plugin subsystem.

    Responsibilities
    ----------------
    • Plugin discovery
    • Loading / unloading
    • Registry management
    • Version management
    • Sandbox execution
    • Permission validation
    • Export
    """

    def __init__(
        self,
        loader: Optional[DynamicLoader] = None,
        registry: Optional[PluginRegistry] = None,
        versions: Optional[VersionManager] = None,
        sandbox: Optional[PluginSandbox] = None,
    ):

        self.loader = loader or DynamicLoader()

        self.registry = registry or self.loader.registry

        self.versions = versions or VersionManager()

        self.sandbox = sandbox or PluginSandbox()

    # -------------------------------------------------
    # Internal Copy
    # -------------------------------------------------

    @staticmethod
    def _copy(plugin: Plugin) -> Plugin:

        copied = Plugin.model_validate(
            plugin.model_dump(
                exclude={"module"}
            )
        )

        copied.module = plugin.module

        return copied
    
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
    # Load
    # -------------------------------------------------

    def load(
        self,
        path: str,
        overwrite: bool = False,
    ) -> Plugin:

        plugin = self.loader.load(
            path,
            overwrite=overwrite,
        )

        self.versions.register(
            plugin
        )

        self.sandbox.register(
            plugin
        )

        return plugin

    # -------------------------------------------------
    # Load All
    # -------------------------------------------------

    def load_all(
        self,
        plugin_directory: str,
        overwrite: bool = False,
    ) -> List[Plugin]:

        plugins = self.loader.load_all(
            plugin_directory,
            overwrite=overwrite,
        )

        for plugin in plugins:

            self.versions.register(
                plugin
            )

            self.sandbox.register(
                plugin
            )

        return plugins

    # -------------------------------------------------
    # Reload
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

        self.versions.register(
            plugin
        )

        self.sandbox.register(
            plugin
        )

        return plugin

    # -------------------------------------------------
    # Unload
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

            self.versions.unregister(
                name
            )

            self.sandbox.unregister(
                name
            )

        return unloaded

    # -------------------------------------------------
    # Refresh
    # -------------------------------------------------

    def refresh(
        self,
        plugin_directory: str,
    ) -> List[Plugin]:

        plugins = self.loader.refresh(
            plugin_directory
        )

        for plugin in plugins:

            self.versions.register(
                plugin
            )

            self.sandbox.register(
                plugin
            )

        return plugins

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

    def exists(
        self,
        name: str,
    ) -> bool:

        return self.registry.exists(
            name
        )

    # -------------------------------------------------
    # Version
    # -------------------------------------------------

    def version(
        self,
        name: str,
    ) -> Optional[str]:

        return self.versions.version(
            name
        )

    def upgrade(
        self,
        name: str,
        version: str,
    ) -> bool:

        return self.versions.upgrade(
            name,
            version,
        )

    def downgrade(
        self,
        name: str,
        version: str,
    ) -> bool:

        return self.versions.downgrade(
            name,
            version,
        )

    # -------------------------------------------------
    # Permissions
    # -------------------------------------------------

    def has_permission(
        self,
        name: str,
        permission: PluginPermission,
    ) -> bool:

        return self.sandbox.has_permission(
            name,
            permission,
        )

    # -------------------------------------------------
    # Execute
    # -------------------------------------------------

    def execute(
        self,
        plugin_name: str,
        command: List[str],
        timeout: int = 30,
        env: Optional[dict] = None,
    ):

        return self.sandbox.execute(
            plugin_name,
            command,
            timeout=timeout,
            env=env,
        )

    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    def enable(
        self,
        name: str,
    ):

        self.registry.enable(
            name
        )

    def disable(
        self,
        name: str,
    ):

        self.registry.disable(
            name
        )

    def status(
        self,
        name: str,
    ) -> PluginStatus:

        return self.registry.status(
            name
        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ) -> dict:

        return {
            "registry": self.registry.statistics(),
            "versions": self.versions.export(),
            "sandbox": self.sandbox.export(),
        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ) -> dict:

        return {
            "registry": self.registry.export(),
            "versions": self.versions.export(),
            "sandbox": self.sandbox.export(),
        }

    # -------------------------------------------------
    # Utilities
    # -------------------------------------------------

    def count(
        self,
    ) -> int:

        return len(
            self.registry
        )

    def clear(
        self,
    ):

        self.loader.clear()

        self.registry.clear()

        self.versions.clear()

        self.sandbox.clear()

    def empty(
        self,
    ) -> bool:

        return self.registry.empty()

    # -------------------------------------------------
    # Dunder
    # -------------------------------------------------

    def __len__(
        self,
    ):

        return self.count()

    def __contains__(
        self,
        name: str,
    ):

        return self.exists(
            name
        )

    def __iter__(
        self,
    ):

        return iter(
            self.plugins()
        )