import unittest

from app.plugins.models import (
    Plugin,
    PluginConfig,
    PluginMetadata,
    PluginStatistics,
    PluginStatus,
)
from app.plugins.plugin_registry import PluginRegistry


class TestPluginRegistry(unittest.TestCase):

    def setUp(self):

        self.registry = PluginRegistry()

        self.plugin = Plugin(

            metadata=PluginMetadata(
                name="Test Plugin",
                version="1.0.0",
                author="Pooja",
                description="Registry Test Plugin",
            ),

            config=PluginConfig(),

            entrypoint="plugins.test",

            status=PluginStatus.UNLOADED,

        )

    # -------------------------------------------------
    # Register
    # -------------------------------------------------

    def test_register(self):

        plugin = self.registry.register(
            self.plugin
        )

        self.assertEqual(
            plugin.metadata.name,
            "Test Plugin",
        )

        self.assertEqual(
            len(self.registry),
            1,
        )

    def test_duplicate_register(self):

        self.registry.register(
            self.plugin
        )

        with self.assertRaises(
            ValueError
        ):

            self.registry.register(
                self.plugin
            )

    def test_register_overwrite(self):

        self.registry.register(
            self.plugin
        )

        plugin = self.registry.register(
            self.plugin,
            overwrite=True,
        )

        self.assertEqual(
            plugin.metadata.version,
            "1.0.0",
        )

    # -------------------------------------------------
    # Lookup
    # -------------------------------------------------

    def test_exists(self):

        self.registry.register(
            self.plugin
        )

        self.assertTrue(
            self.registry.exists(
                "Test Plugin"
            )
        )

    def test_get(self):

        self.registry.register(
            self.plugin
        )

        plugin = self.registry.get(
            "Test Plugin"
        )

        self.assertIsNotNone(
            plugin
        )

        self.assertEqual(
            plugin.metadata.author,
            "Pooja",
        )

    def test_all(self):

        self.registry.register(
            self.plugin
        )

        plugins = self.registry.all()

        self.assertEqual(
            len(plugins),
            1,
        )

    # -------------------------------------------------
    # Enable / Disable
    # -------------------------------------------------

    def test_disable(self):

        self.registry.register(
            self.plugin
        )

        self.registry.disable(
            "Test Plugin"
        )

        plugin = self.registry.get(
            "Test Plugin"
        )

        self.assertFalse(
            plugin.config.enabled
        )

        self.assertEqual(
            plugin.status,
            PluginStatus.DISABLED,
        )

    def test_enable(self):

        self.registry.register(
            self.plugin
        )

        self.registry.disable(
            "Test Plugin"
        )

        self.registry.enable(
            "Test Plugin"
        )

        plugin = self.registry.get(
            "Test Plugin"
        )

        self.assertTrue(
            plugin.config.enabled
        )

    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    def test_set_status(self):

        self.registry.register(
            self.plugin
        )

        self.registry.set_status(

            "Test Plugin",

            PluginStatus.LOADED,

        )

        self.assertEqual(

            self.registry.status(
                "Test Plugin"
            ),

            PluginStatus.LOADED,

        )

    # -------------------------------------------------
    # Filters
    # -------------------------------------------------

    def test_loaded_plugins(self):

        self.plugin.status = (
            PluginStatus.LOADED
        )

        self.registry.register(
            self.plugin
        )

        self.assertEqual(

            len(
                self.registry.loaded()
            ),

            1,

        )

    def test_enabled_plugins(self):

        self.registry.register(
            self.plugin
        )

        self.assertEqual(

            len(
                self.registry.enabled()
            ),

            1,

        )

    def test_disabled_plugins(self):

        self.registry.register(
            self.plugin
        )

        self.registry.disable(
            "Test Plugin"
        )

        self.assertEqual(

            len(
                self.registry.disabled()
            ),

            1,

        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def test_statistics(self):

        self.plugin.status = (
            PluginStatus.LOADED
        )

        self.registry.register(
            self.plugin
        )

        stats = self.registry.statistics()

        self.assertIsInstance(
            stats,
            PluginStatistics,
        )

        self.assertEqual(
            stats.plugins,
            1,
        )

        self.assertEqual(
            stats.loaded,
            1,
        )

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def test_export(self):

        self.registry.register(
            self.plugin
        )

        exported = self.registry.export()

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

        self.registry.register(
            self.plugin
        )

        result = self.registry.unregister(
            "Test Plugin"
        )

        self.assertTrue(
            result
        )

        self.assertEqual(
            len(self.registry),
            0,
        )

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def test_clear(self):

        self.registry.register(
            self.plugin
        )

        self.registry.clear()

        self.assertTrue(
            self.registry.empty()
        )

    # -------------------------------------------------
    # Contains
    # -------------------------------------------------

    def test_contains(self):

        self.registry.register(
            self.plugin
        )

        self.assertTrue(
            "Test Plugin"
            in self.registry
        )

    # -------------------------------------------------
    # Iterator
    # -------------------------------------------------

    def test_iterator(self):

        self.registry.register(
            self.plugin
        )

        names = [

            plugin.metadata.name

            for plugin

            in self.registry

        ]

        self.assertEqual(
            names,
            ["Test Plugin"],
        )


if __name__ == "__main__":

    print(
        "\n=== Plugin Registry Test ===\n"
    )

    unittest.main(
        verbosity=2
    )