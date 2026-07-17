from __future__ import annotations

import importlib
import importlib.util
import inspect
import sys
import time
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from typing import Dict, List, Optional

from app.plugins.models import (
    Plugin,
    PluginMetadata,
    PluginStatistics,
    PluginStatus,
)


class PluginLoader:
    """
    Enterprise Plugin Loader

    Responsibilities
    ----------------
    • Discover plugins
    • Load plugins
    • Reload plugins
    • Unload plugins
    • Validate plugin metadata
    • Keep loaded modules in memory
    """

    def __init__(self):

        self._plugins: Dict[str, Plugin] = {}

        self._modules: Dict[str, ModuleType] = {}

    # -------------------------------------------------
    # Safe Copy
    # -------------------------------------------------

    def _copy_plugin(
        self,
        plugin: Plugin,
    ) -> Plugin:

        data = plugin.model_dump(
            exclude={"module"}
        )

        copied = Plugin.model_validate(data)

        copied.module = plugin.module

        return copied
    
    # -------------------------------------------------
    # Discovery
    # -------------------------------------------------

    def discover(
        self,
        plugin_directory: str,
    ) -> List[str]:

        directory = Path(plugin_directory)

        if not directory.exists():

            return []

        discovered = []

        for file in directory.rglob("*.py"):

            if file.name.startswith("_"):

                continue

            discovered.append(str(file))

        return sorted(discovered)

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    def validate(
        self,
        module: ModuleType,
    ) -> bool:

        if not hasattr(module, "PLUGIN_METADATA"):

            return False

        metadata = getattr(module, "PLUGIN_METADATA")

        if isinstance(metadata, PluginMetadata):

            return True

        return False

    # -------------------------------------------------
    # Load From Module
    # -------------------------------------------------

    def load_module(
        self,
        module_name: str,
    ) -> Plugin:

        module = importlib.import_module(module_name)

        if not self.validate(module):

            raise ValueError(
                f"{module_name} missing PLUGIN_METADATA"
            )

        metadata = deepcopy(module.PLUGIN_METADATA)

        plugin = Plugin(

            metadata=metadata,

            entrypoint=module_name,

            module=module,

            status=PluginStatus.LOADED,

            loaded_at=time.time(),

        )

        plugin.permissions = list(
            getattr(
                module,
                "PERMISSIONS",
                [],
            )
        )

        plugin.tools = list(
            getattr(
                module,
                "TOOLS",
                [],
            )
        )

        self._plugins[metadata.name] = plugin

        self._modules[metadata.name] = module

        return self._copy_plugin(plugin)

    # -------------------------------------------------
    # Load From File
    # -------------------------------------------------

    def load_file(
        self,
        path: str,
    ) -> Plugin:

        file = Path(path)

        module_name = file.stem

        spec = importlib.util.spec_from_file_location(

            module_name,

            file,

        )

        if spec is None:

            raise ImportError(path)

        module = importlib.util.module_from_spec(spec)

        sys.modules[module_name] = module

        spec.loader.exec_module(module)

        if not self.validate(module):

            raise ValueError(
                "PLUGIN_METADATA not found"
            )

        metadata = deepcopy(module.PLUGIN_METADATA)

        plugin = Plugin(

            metadata=metadata,

            entrypoint=str(file),

            module=module,

            status=PluginStatus.LOADED,

            loaded_at=time.time(),

        )

        plugin.permissions = list(
            getattr(
                module,
                "PERMISSIONS",
                [],
            )
        )

        plugin.tools = list(
            getattr(
                module,
                "TOOLS",
                [],
            )
        )

        plugin.permissions = list(
            getattr(
                module,
                "PERMISSIONS",
                [],
            )
        )

        self._plugins[metadata.name] = plugin

        self._modules[metadata.name] = module

        return self._copy_plugin(plugin)

    # -------------------------------------------------
    # Reload
    # -------------------------------------------------

    def reload(
        self,
        name: str,
    ) -> Plugin:

        if name not in self._plugins:

            raise KeyError(name)

        plugin = self._plugins[name]

        # ---------------------------------------------
        # Plugin loaded from a Python file
        # ---------------------------------------------
        if Path(plugin.entrypoint).exists():

            file = Path(plugin.entrypoint)

            module_name = file.stem

            spec = importlib.util.spec_from_file_location(
                module_name,
                file,
            )

            if spec is None or spec.loader is None:

                raise ImportError(
                    f"Unable to reload {file}"
                )

            module = importlib.util.module_from_spec(
                spec
            )

            sys.modules[module_name] = module

            spec.loader.exec_module(module)

        # ---------------------------------------------
        # Plugin loaded via importlib.import_module()
        # ---------------------------------------------
        else:

            module = importlib.import_module(
                plugin.entrypoint
            )

        if not self.validate(module):

            raise ValueError(
                "PLUGIN_METADATA not found"
            )

        metadata = deepcopy(
            module.PLUGIN_METADATA
        )

        plugin.module = module

        plugin.metadata = metadata

        plugin.status = PluginStatus.LOADED

        plugin.loaded_at = time.time()

        plugin.tools = list(
            getattr(
                module,
                "TOOLS",
                [],
            )
        )

        self._modules[metadata.name] = module

        return self._copy_plugin(plugin)

    # -------------------------------------------------
    # Unload
    # -------------------------------------------------

    def unload(
        self,
        name: str,
    ) -> bool:

        if name not in self._plugins:

            return False

        plugin = self._plugins[name]

        module = plugin.module

        if module:

            sys.modules.pop(module.__name__, None)

        plugin.status = PluginStatus.UNLOADED

        plugin.module = None

        self._modules.pop(name, None)

        return True

    # -------------------------------------------------
    # Accessors
    # -------------------------------------------------

    def plugin(
        self,
        name: str,
    ) -> Optional[Plugin]:

        plugin = self._plugins.get(name)

        if plugin is None:

            return None

        return self._copy_plugin(plugin)

    def plugins(
        self,
    ) -> List[Plugin]:

        return [

            self._copy_plugin(plugin)

            for plugin in self._plugins.values()

        ]

    def module(
        self,
        name: str,
    ) -> Optional[ModuleType]:

        return self._modules.get(name)

    def has_plugin(
        self,
        name: str,
    ) -> bool:

        return name in self._plugins

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ) -> PluginStatistics:

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

        return {

            "plugins": [

                plugin.model_dump(

                    exclude={"module"}

                )

                for plugin in self._plugins.values()

            ]

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        for plugin in self._plugins.values():

            if plugin.module:

                sys.modules.pop(

                    plugin.module.__name__,

                    None,

                )

        self._plugins.clear()

        self._modules.clear()

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return PluginLoader()