from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

from app.plugins.models import Plugin


class VersionManager:
    """
    Enterprise Plugin Version Manager

    Responsibilities
    ----------------
    • Validate semantic versions
    • Compare versions
    • Register plugin versions
    • Upgrade/Downgrade versions
    • Compatibility checks
    • Export version information
    """

    VERSION_PATTERN = re.compile(
        r"^(0|[1-9]\d*)\."
        r"(0|[1-9]\d*)\."
        r"(0|[1-9]\d*)"
        r"(?:-[0-9A-Za-z.-]+)?"
        r"(?:\+[0-9A-Za-z.-]+)?$"
    )

    def __init__(self):

        self._plugins: Dict[str, Plugin] = {}

    # -------------------------------------------------
    # Internal Copy
    # -------------------------------------------------

    @staticmethod
    def _copy(
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
    # Validation
    # -------------------------------------------------

    @classmethod
    def validate(
        cls,
        version: str,
    ) -> bool:

        return bool(
            cls.VERSION_PATTERN.match(version)
        )

    # -------------------------------------------------
    # Parse
    # -------------------------------------------------

    @staticmethod
    def parse(
        version: str,
    ) -> Tuple[int, int, int]:

        version = version.split("-")[0]
        version = version.split("+")[0]

        major, minor, patch = version.split(".")

        return (
            int(major),
            int(minor),
            int(patch),
        )

    # -------------------------------------------------
    # Compare
    # -------------------------------------------------

    @classmethod
    def compare(
        cls,
        version1: str,
        version2: str,
    ) -> int:

        a = cls.parse(version1)
        b = cls.parse(version2)

        if a > b:
            return 1

        if a < b:
            return -1

        return 0

    # -------------------------------------------------
    # Register
    # -------------------------------------------------

    def register(
        self,
        plugin: Plugin,
    ):

        version = plugin.metadata.version

        if not self.validate(version):

            raise ValueError(
                f"Invalid version '{version}'"
            )

        self._plugins[plugin.metadata.name] = self._copy(plugin)

    # -------------------------------------------------
    # Exists
    # -------------------------------------------------

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._plugins

    # -------------------------------------------------
    # Get Plugin
    # -------------------------------------------------

    def plugin(
        self,
        name: str,
    ) -> Optional[Plugin]:

        plugin = self._plugins.get(name)

        if plugin is None:

            return None

        return self._copy(plugin)

    # -------------------------------------------------
    # Version
    # -------------------------------------------------

    def version(
        self,
        name: str,
    ) -> Optional[str]:

        plugin = self._plugins.get(name)

        if plugin is None:

            return None

        return plugin.metadata.version

    # -------------------------------------------------
    # Upgrade
    # -------------------------------------------------

    def upgrade(
        self,
        name: str,
        version: str,
    ) -> bool:

        if not self.validate(version):

            raise ValueError(
                "Invalid version."
            )

        plugin = self._plugins.get(name)

        if plugin is None:

            return False

        if self.compare(
            version,
            plugin.metadata.version,
        ) <= 0:

            return False

        plugin.metadata.version = version

        return True

    # -------------------------------------------------
    # Downgrade
    # -------------------------------------------------

    def downgrade(
        self,
        name: str,
        version: str,
    ) -> bool:

        if not self.validate(version):

            raise ValueError(
                "Invalid version."
            )

        plugin = self._plugins.get(name)

        if plugin is None:

            return False

        if self.compare(
            version,
            plugin.metadata.version,
        ) >= 0:

            return False

        plugin.metadata.version = version

        return True

    # -------------------------------------------------
    # Compatibility
    # -------------------------------------------------

    def compatible(
        self,
        name: str,
        minimum: str,
    ) -> bool:

        plugin = self._plugins.get(name)

        if plugin is None:

            return False

        return (
            self.compare(
                plugin.metadata.version,
                minimum,
            )
            >= 0
        )

    # -------------------------------------------------
    # Latest
    # -------------------------------------------------

    def latest(self) -> List[Plugin]:

        return [

            self._copy(plugin)

            for plugin in self._plugins.values()

        ]

    # -------------------------------------------------
    # Remove
    # -------------------------------------------------

    def unregister(
        self,
        name: str,
    ) -> bool:

        if name not in self._plugins:

            return False

        del self._plugins[name]

        return True

    # -------------------------------------------------
    # Count
    # -------------------------------------------------

    def count(self) -> int:

        return len(self._plugins)

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(self) -> dict:

        return {

            "plugins": [

                {
                    "name": plugin.metadata.name,
                    "version": plugin.metadata.version,
                    "author": plugin.metadata.author,
                }

                for plugin

                in self._plugins.values()

            ]

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(self):

        self._plugins.clear()

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    def empty(self) -> bool:

        return len(self._plugins) == 0

    # -------------------------------------------------
    # Dunder Methods
    # -------------------------------------------------

    def __len__(self):

        return len(self._plugins)

    def __contains__(
        self,
        name: str,
    ):

        return name in self._plugins

    def __iter__(self):

        return iter(self.latest())