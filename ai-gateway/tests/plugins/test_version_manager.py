import unittest

from app.plugins.models import (
    Plugin,
    PluginConfig,
    PluginMetadata,
)
from app.plugins.version_manager import VersionManager


class TestVersionManager(unittest.TestCase):

    def setUp(self):

        self.manager = VersionManager()

        self.plugin = Plugin(

            metadata=PluginMetadata(
                name="Test Plugin",
                version="1.0.0",
                author="Pooja",
                description="Version Manager Test Plugin",
            ),

            config=PluginConfig(),

            entrypoint="plugins.test",

        )

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    def test_validate_valid(self):

        self.assertTrue(
            self.manager.validate("1.0.0")
        )

        self.assertTrue(
            self.manager.validate("10.25.300")
        )

        self.assertTrue(
            self.manager.validate("1.0.0-alpha")
        )

    def test_validate_invalid(self):

        self.assertFalse(
            self.manager.validate("1")
        )

        self.assertFalse(
            self.manager.validate("1.0")
        )

        self.assertFalse(
            self.manager.validate("v1.0.0")
        )

    # -------------------------------------------------
    # Parse
    # -------------------------------------------------

    def test_parse(self):

        self.assertEqual(

            self.manager.parse("2.5.10"),

            (2, 5, 10),

        )

    # -------------------------------------------------
    # Compare
    # -------------------------------------------------

    def test_compare_equal(self):

        self.assertEqual(

            self.manager.compare(
                "1.0.0",
                "1.0.0",
            ),

            0,

        )

    def test_compare_greater(self):

        self.assertEqual(

            self.manager.compare(
                "2.0.0",
                "1.9.9",
            ),

            1,

        )

    def test_compare_less(self):

        self.assertEqual(

            self.manager.compare(
                "1.2.0",
                "2.0.0",
            ),

            -1,

        )

    # -------------------------------------------------
    # Register
    # -------------------------------------------------

    def test_register(self):

        self.manager.register(
            self.plugin
        )

        self.assertEqual(

            self.manager.count(),

            1,

        )

        self.assertTrue(

            self.manager.exists(
                "Test Plugin"
            )

        )

    # -------------------------------------------------
    # Plugin Lookup
    # -------------------------------------------------

    def test_plugin(self):

        self.manager.register(
            self.plugin
        )

        plugin = self.manager.plugin(
            "Test Plugin"
        )

        self.assertIsNotNone(
            plugin
        )

        self.assertEqual(

            plugin.metadata.version,

            "1.0.0",

        )

    def test_version(self):

        self.manager.register(
            self.plugin
        )

        self.assertEqual(

            self.manager.version(
                "Test Plugin"
            ),

            "1.0.0",

        )

    # -------------------------------------------------
    # Upgrade
    # -------------------------------------------------

    def test_upgrade(self):

        self.manager.register(
            self.plugin
        )

        result = self.manager.upgrade(

            "Test Plugin",

            "2.0.0",

        )

        self.assertTrue(
            result
        )

        self.assertEqual(

            self.manager.version(
                "Test Plugin"
            ),

            "2.0.0",

        )

    def test_upgrade_lower_version(self):

        self.manager.register(
            self.plugin
        )

        self.assertFalse(

            self.manager.upgrade(

                "Test Plugin",

                "0.9.0",

            )

        )

    # -------------------------------------------------
    # Downgrade
    # -------------------------------------------------

    def test_downgrade(self):

        self.plugin.metadata.version = "3.0.0"

        self.manager.register(
            self.plugin
        )

        result = self.manager.downgrade(

            "Test Plugin",

            "2.0.0",

        )

        self.assertTrue(
            result
        )

        self.assertEqual(

            self.manager.version(
                "Test Plugin"
            ),

            "2.0.0",

        )

    def test_downgrade_higher_version(self):

        self.manager.register(
            self.plugin
        )

        self.assertFalse(

            self.manager.downgrade(

                "Test Plugin",

                "2.0.0",

            )

        )

    # -------------------------------------------------
    # Compatibility
    # -------------------------------------------------

    def test_compatible(self):

        self.manager.register(
            self.plugin
        )

        self.assertTrue(

            self.manager.compatible(

                "Test Plugin",

                "1.0.0",

            )

        )

        self.assertTrue(

            self.manager.compatible(

                "Test Plugin",

                "0.5.0",

            )

        )

        self.assertFalse(

            self.manager.compatible(

                "Test Plugin",

                "2.0.0",

            )

        )

    # -------------------------------------------------
    # Latest
    # -------------------------------------------------

    def test_latest(self):

        self.manager.register(
            self.plugin
        )

        plugins = self.manager.latest()

        self.assertEqual(

            len(plugins),

            1,

        )

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def test_export(self):

        self.manager.register(
            self.plugin
        )

        exported = self.manager.export()

        self.assertIn(
            "plugins",
            exported,
        )

        self.assertEqual(

            len(
                exported["plugins"]
            ),

            1,

        )

    # -------------------------------------------------
    # Unregister
    # -------------------------------------------------

    def test_unregister(self):

        self.manager.register(
            self.plugin
        )

        result = self.manager.unregister(
            "Test Plugin"
        )

        self.assertTrue(
            result
        )

        self.assertEqual(

            self.manager.count(),

            0,

        )

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    def test_empty(self):

        self.assertTrue(
            self.manager.empty()
        )

        self.manager.register(
            self.plugin
        )

        self.assertFalse(
            self.manager.empty()
        )

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def test_clear(self):

        self.manager.register(
            self.plugin
        )

        self.manager.clear()

        self.assertTrue(
            self.manager.empty()
        )

    # -------------------------------------------------
    # Dunder Methods
    # -------------------------------------------------

    def test_len(self):

        self.manager.register(
            self.plugin
        )

        self.assertEqual(

            len(self.manager),

            1,

        )

    def test_contains(self):

        self.manager.register(
            self.plugin
        )

        self.assertTrue(

            "Test Plugin"

            in self.manager

        )

    def test_iterator(self):

        self.manager.register(
            self.plugin
        )

        names = [

            plugin.metadata.name

            for plugin

            in self.manager

        ]

        self.assertEqual(

            names,

            ["Test Plugin"],

        )


if __name__ == "__main__":

    print(
        "\n=== Version Manager Test ===\n"
    )

    unittest.main(
        verbosity=2
    )