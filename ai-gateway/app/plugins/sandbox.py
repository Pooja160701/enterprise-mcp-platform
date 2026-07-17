from __future__ import annotations

import os
import subprocess
import tempfile
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional

from app.plugins.models import Plugin, PluginPermission


class PluginSandbox:
    """
    Enterprise Plugin Sandbox

    Responsibilities
    ----------------
    • Permission validation
    • Secure command execution
    • Environment isolation
    • Working directory isolation
    • Audit logging
    • Resource restrictions
    """

    DEFAULT_ALLOWED_COMMANDS = {
        "python",
        "python3",
        "echo",
        "dir",
        "ls",
        "pwd",
    }

    DEFAULT_BLOCKED_COMMANDS = {
        "rm",
        "rmdir",
        "del",
        "shutdown",
        "reboot",
        "mkfs",
        "format",
        "curl",
        "wget",
        "scp",
        "ssh",
        "powershell",
    }

    def __init__(self):

        self._plugins: Dict[str, Plugin] = {}

        self._audit_log: List[dict] = []

        self._allowed_commands = set(
            self.DEFAULT_ALLOWED_COMMANDS
        )

        self._blocked_commands = set(
            self.DEFAULT_BLOCKED_COMMANDS
        )

        self._lock = threading.RLock()

        self._root = Path(
            tempfile.mkdtemp(
                prefix="plugin_sandbox_"
            )
        )

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
    # Plugin Management
    # -------------------------------------------------

    def register(
        self,
        plugin: Plugin,
    ):

        with self._lock:

            self._plugins[
                plugin.metadata.name
            ] = self._copy(plugin)

    def unregister(
        self,
        name: str,
    ) -> bool:

        with self._lock:

            return (
                self._plugins.pop(
                    name,
                    None,
                )
                is not None
            )

    def plugin(
        self,
        name: str,
    ) -> Optional[Plugin]:

        plugin = self._plugins.get(name)

        if plugin is None:

            return None

        return self._copy(plugin)

    # -------------------------------------------------
    # Permissions
    # -------------------------------------------------

    def has_permission(
        self,
        plugin_name: str,
        permission: PluginPermission,
    ) -> bool:

        plugin = self._plugins.get(
            plugin_name
        )

        if plugin is None:

            return False

        return (
            permission
            in plugin.permissions
        )

    # -------------------------------------------------
    # Command Rules
    # -------------------------------------------------

    def allow_command(
        self,
        command: str,
    ):

        self._allowed_commands.add(command)

    def block_command(
        self,
        command: str,
    ):

        self._blocked_commands.add(command)

    def allowed_commands(
        self,
    ) -> List[str]:

        return sorted(
            self._allowed_commands
        )

    def blocked_commands(
        self,
    ) -> List[str]:

        return sorted(
            self._blocked_commands
        )

    # -------------------------------------------------
    # Execution
    # -------------------------------------------------

    def execute(
        self,
        plugin_name: str,
        command: List[str],
        timeout: int = 30,
        env: Optional[dict] = None,
    ) -> subprocess.CompletedProcess:

        if plugin_name not in self._plugins:

            raise ValueError(
                "Plugin not registered."
            )

        executable = Path(
            command[0]
        ).name.lower()

        if (
            executable
            in self._blocked_commands
        ):

            raise PermissionError(
                f"Blocked command: {executable}"
            )

        if (
            executable
            not in self._allowed_commands
        ):

            raise PermissionError(
                f"Command not allowed: {executable}"
            )

        working_dir = (
            self._root
            / plugin_name.replace(
                " ",
                "_",
            )
        )

        working_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        environment = os.environ.copy()

        if env:

            environment.update(env)

        result = subprocess.run(
            command,
            cwd=working_dir,
            env=environment,
            timeout=timeout,
            capture_output=True,
            text=True,
        )

        self._audit_log.append(
            {
                "plugin": plugin_name,
                "command": command,
                "returncode": result.returncode,
                "timestamp": time.time(),
            }
        )

        return result

    # -------------------------------------------------
    # Audit
    # -------------------------------------------------

    def audit_log(
        self,
    ) -> List[dict]:

        return [
            entry.copy()
            for entry in self._audit_log
        ]

    def clear_audit(
        self,
    ):

        self._audit_log.clear()

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ) -> dict:

        return {
            "plugins": list(
                self._plugins.keys()
            ),
            "audit": [
                entry.copy()
                for entry in self._audit_log
            ],
            "allowed_commands": self.allowed_commands(),
            "blocked_commands": self.blocked_commands(),
        }

    # -------------------------------------------------
    # Utilities
    # -------------------------------------------------

    def count(self) -> int:

        return len(
            self._plugins
        )

    def clear(self):

        self._plugins.clear()

        self._audit_log.clear()

    def empty(self) -> bool:

        return (
            len(self._plugins)
            == 0
        )

    # -------------------------------------------------
    # Dunder
    # -------------------------------------------------

    def __len__(
        self,
    ):

        return len(
            self._plugins
        )

    def __contains__(
        self,
        name: str,
    ):

        return (
            name
            in self._plugins
        )

    def __iter__(
        self,
    ):

        return iter(

            [

                self._copy(plugin)

                for plugin

                in self._plugins.values()

            ]

        )