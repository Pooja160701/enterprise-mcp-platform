from __future__ import annotations

import threading
from typing import Dict, List, Optional

from app.plugins.models import (
    Plugin,
    PluginStatistics,
    PluginStatus,
)


class PluginRegistry:
    """
    Enterprise Plugin Registry

    Responsibilities
    ----------------
    • Register plugins
    • Unregister plugins
    • Lookup plugins
    • Enable/Disable plugins
    • Maintain plugin state
    • Export registry
    """

    def __init__(self):

        self._plugins: Dict[str, Plugin] = {}

        self._lock = threading.RLock()

    # -------------------------------------------------
    # Internal
    # -------------------------------------------------

    def _copy(
        self,
        plugin: Plugin,
    ) -> Plugin:

        copied = Plugin.model_validate(
            plugin.model_dump(
                exclude={"module"}
            )
        )

        copied.module = plugin.module

        return copied

    # -------------------------------------------------
    # Registration
    # -------------------------------------------------

    def register(
        self,
        plugin: Plugin,
        overwrite: bool = False,
    ) -> Plugin:

        with self._lock:

            name = plugin.metadata.name

            if (
                name in self._plugins
                and not overwrite
            ):

                raise ValueError(
                    f"Plugin '{name}' already registered."
                )

            self._plugins[name] = plugin

            return self._copy(plugin)

    # -------------------------------------------------

    def unregister(
        self,
        name: str,
    ) -> bool:

        with self._lock:

            if name not in self._plugins:

                return False

            del self._plugins[name]

            return True

    # -------------------------------------------------
    # Lookup
    # -------------------------------------------------

    def get(
        self,
        name: str,
    ) -> Optional[Plugin]:

        with self._lock:

            plugin = self._plugins.get(name)

            if plugin is None:

                return None

            return self._copy(plugin)

    def exists(
        self,
        name: str,
    ) -> bool:

        with self._lock:

            return name in self._plugins

    def all(
        self,
    ) -> List[Plugin]:

        with self._lock:

            return [

                self._copy(plugin)

                for plugin in self._plugins.values()

            ]

    # -------------------------------------------------
    # Enable / Disable
    # -------------------------------------------------

    def enable(
        self,
        name: str,
    ) -> bool:

        with self._lock:

            plugin = self._plugins.get(name)

            if plugin is None:

                return False

            plugin.config.enabled = True

            plugin.status = PluginStatus.LOADED

            return True

    def disable(
        self,
        name: str,
    ) -> bool:

        with self._lock:

            plugin = self._plugins.get(name)

            if plugin is None:

                return False

            plugin.config.enabled = False

            plugin.status = PluginStatus.DISABLED

            return True

    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    def set_status(
        self,
        name: str,
        status: PluginStatus,
    ) -> bool:

        with self._lock:

            plugin = self._plugins.get(name)

            if plugin is None:

                return False

            plugin.status = status

            return True

    def status(
        self,
        name: str,
    ) -> Optional[PluginStatus]:

        with self._lock:

            plugin = self._plugins.get(name)

            if plugin is None:

                return None

            return plugin.status

    # -------------------------------------------------
    # Filtering
    # -------------------------------------------------

    def loaded(
        self,
    ) -> List[Plugin]:

        with self._lock:

            return [

                self._copy(plugin)

                for plugin in self._plugins.values()

                if plugin.status == PluginStatus.LOADED

            ]

    def enabled(
        self,
    ) -> List[Plugin]:

        with self._lock:

            return [

                self._copy(plugin)

                for plugin in self._plugins.values()

                if plugin.config.enabled

            ]

    def disabled(
        self,
    ) -> List[Plugin]:

        with self._lock:

            return [

                self._copy(plugin)

                for plugin in self._plugins.values()

                if not plugin.config.enabled

            ]

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ) -> PluginStatistics:

        with self._lock:

            stats = PluginStatistics()

            stats.plugins = len(self._plugins)

            for plugin in self._plugins.values():

                if plugin.status == PluginStatus.LOADED:

                    stats.loaded += 1

                elif plugin.status == PluginStatus.UNLOADED:

                    stats.unloaded += 1

                elif plugin.status == PluginStatus.DISABLED:

                    stats.disabled += 1

                elif plugin.status == PluginStatus.ERROR:

                    stats.errors += 1

            return stats

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ) -> dict:

        with self._lock:

            return {

                "plugins": [

                    plugin.model_dump(
                        exclude={"module"}
                    )

                    for plugin in self._plugins.values()

                ]

            }

    # -------------------------------------------------
    # Import
    # -------------------------------------------------

    def load(
        self,
        plugins: List[Plugin],
    ):

        with self._lock:

            self._plugins.clear()

            for plugin in plugins:

                self._plugins[
                    plugin.metadata.name
                ] = self._copy(plugin)

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        with self._lock:

            self._plugins.clear()

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    def empty(self) -> bool:

        with self._lock:

            return len(self._plugins) == 0

    # -------------------------------------------------
    # Length
    # -------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(self._plugins)

    # -------------------------------------------------
    # Contains
    # -------------------------------------------------

    def __contains__(
        self,
        name: str,
    ) -> bool:

        return name in self._plugins

    # -------------------------------------------------
    # Iterator
    # -------------------------------------------------

    def __iter__(
        self,
    ):

        return iter(self.all())