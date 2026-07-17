import unittest

from app.plugins.models import (
    Plugin,
    PluginConfig,
    PluginMetadata,
    PluginPermission,
)
from app.plugins.sandbox import PluginSandbox


class TestPluginSandbox(unittest.TestCase):

    def setUp(self):

        self.sandbox = PluginSandbox()

        self.plugin = Plugin(

            metadata=PluginMetadata(
                name="Sandbox Plugin",
                version="1.0.0",
                author="Pooja",
                description="Sandbox Test Plugin",
            ),

            config=PluginConfig(),

            permissions=[
                PluginPermission.FILESYSTEM,
                PluginPermission.TOOLS,
            ],

            entrypoint="plugins.sandbox",
        )

    def tearDown(self):

        self.sandbox.clear()

    # -------------------------------------------------
    # Register
    # -------------------------------------------------

    def test_register(self):

        self.sandbox.register(
            self.plugin
        )

        self.assertEqual(
            self.sandbox.count(),
            1,
        )

        self.assertIn(
            "Sandbox Plugin",
            self.sandbox,
        )

    # -------------------------------------------------
    # Plugin Lookup
    # -------------------------------------------------

    def test_plugin(self):

        self.sandbox.register(
            self.plugin
        )

        plugin = self.sandbox.plugin(
            "Sandbox Plugin"
        )

        self.assertIsNotNone(
            plugin
        )

        self.assertEqual(
            plugin.metadata.name,
            "Sandbox Plugin",
        )

    # -------------------------------------------------
    # Permissions
    # -------------------------------------------------

    def test_has_permission(self):

        self.sandbox.register(
            self.plugin
        )

        self.assertTrue(

            self.sandbox.has_permission(
                "Sandbox Plugin",
                PluginPermission.FILESYSTEM,
            )

        )

        self.assertFalse(

            self.sandbox.has_permission(
                "Sandbox Plugin",
                PluginPermission.NETWORK,
            )

        )

    # -------------------------------------------------
    # Allowed Commands
    # -------------------------------------------------

    def test_allow_command(self):

        self.sandbox.allow_command(
            "whoami"
        )

        self.assertIn(
            "whoami",
            self.sandbox.allowed_commands(),
        )

    # -------------------------------------------------
    # Blocked Commands
    # -------------------------------------------------

    def test_block_command(self):

        self.sandbox.block_command(
            "danger"
        )

        self.assertIn(
            "danger",
            self.sandbox.blocked_commands(),
        )

    # -------------------------------------------------
    # Execute
    # -------------------------------------------------

    def test_execute_echo(self):

        self.sandbox.register(
            self.plugin
        )

        result = self.sandbox.execute(

            "Sandbox Plugin",

            ["echo", "hello"],

        )

        self.assertEqual(
            result.returncode,
            0,
        )

        self.assertIn(
            "hello",
            result.stdout.lower(),
        )

    # -------------------------------------------------
    # Execute Blocked
    # -------------------------------------------------

    def test_execute_blocked(self):

        self.sandbox.register(
            self.plugin
        )

        with self.assertRaises(
            PermissionError
        ):

            self.sandbox.execute(

                "Sandbox Plugin",

                ["rm", "-rf", "/"],

            )

    # -------------------------------------------------
    # Execute Unknown Command
    # -------------------------------------------------

    def test_execute_not_allowed(self):

        self.sandbox.register(
            self.plugin
        )

        with self.assertRaises(
            PermissionError
        ):

            self.sandbox.execute(

                "Sandbox Plugin",

                ["unknown_command"],

            )

    # -------------------------------------------------
    # Execute Missing Plugin
    # -------------------------------------------------

    def test_execute_missing_plugin(self):

        with self.assertRaises(
            ValueError
        ):

            self.sandbox.execute(

                "Unknown",

                ["echo", "hello"],

            )

    # -------------------------------------------------
    # Audit Log
    # -------------------------------------------------

    def test_audit_log(self):

        self.sandbox.register(
            self.plugin
        )

        self.sandbox.execute(

            "Sandbox Plugin",

            ["echo", "audit"],

        )

        audit = self.sandbox.audit_log()

        self.assertEqual(
            len(audit),
            1,
        )

        self.assertEqual(
            audit[0]["plugin"],
            "Sandbox Plugin",
        )

    # -------------------------------------------------
    # Clear Audit
    # -------------------------------------------------

    def test_clear_audit(self):

        self.sandbox.register(
            self.plugin
        )

        self.sandbox.execute(

            "Sandbox Plugin",

            ["echo", "audit"],

        )

        self.sandbox.clear_audit()

        self.assertEqual(

            len(
                self.sandbox.audit_log()
            ),

            0,

        )

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def test_export(self):

        self.sandbox.register(
            self.plugin
        )

        exported = self.sandbox.export()

        self.assertIn(
            "plugins",
            exported,
        )

        self.assertIn(
            "audit",
            exported,
        )

        self.assertIn(
            "allowed_commands",
            exported,
        )

        self.assertIn(
            "blocked_commands",
            exported,
        )

    # -------------------------------------------------
    # Unregister
    # -------------------------------------------------

    def test_unregister(self):

        self.sandbox.register(
            self.plugin
        )

        self.assertTrue(

            self.sandbox.unregister(
                "Sandbox Plugin"
            )

        )

        self.assertEqual(
            self.sandbox.count(),
            0,
        )

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    def test_empty(self):

        self.assertTrue(
            self.sandbox.empty()
        )

        self.sandbox.register(
            self.plugin
        )

        self.assertFalse(
            self.sandbox.empty()
        )

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def test_clear(self):

        self.sandbox.register(
            self.plugin
        )

        self.sandbox.clear()

        self.assertTrue(
            self.sandbox.empty()
        )

    # -------------------------------------------------
    # Dunder
    # -------------------------------------------------

    def test_len(self):

        self.sandbox.register(
            self.plugin
        )

        self.assertEqual(
            len(self.sandbox),
            1,
        )

    def test_contains(self):

        self.sandbox.register(
            self.plugin
        )

        self.assertIn(
            "Sandbox Plugin",
            self.sandbox,
        )

    def test_iterator(self):

        self.sandbox.register(
            self.plugin
        )

        names = [

            plugin.metadata.name

            for plugin

            in self.sandbox

        ]

        self.assertEqual(
            names,
            ["Sandbox Plugin"],
        )


if __name__ == "__main__":

    print(
        "\n=== Plugin Sandbox Test ===\n"
    )

    unittest.main(
        verbosity=2
    )