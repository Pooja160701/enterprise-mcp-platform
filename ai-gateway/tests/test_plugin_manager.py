import shutil
import tempfile
import unittest
from pathlib import Path

from app.plugins.models import (
    PluginPermission,
    PluginStatus,
)
from app.plugins.plugin_manager import PluginManager


class TestPluginManager(unittest.TestCase):

    def setUp(self):

        self.manager = PluginManager()

        self.temp_dir = tempfile.mkdtemp()

        self.plugin_file = (
            Path(self.temp_dir)
            / "sample_plugin.py"
        )

        self.plugin_file.write_text(
            """
from app.plugins.models import PluginMetadata, PluginPermission

PLUGIN_METADATA = PluginMetadata(
    name="Sample Plugin",
    version="1.0.0",
    author="Pooja",
    description="Plugin Manager Test",
)

PERMISSIONS=[
    PluginPermission.FILESYSTEM,
    PluginPermission.TOOLS,
]

TOOLS=["hello"]

def hello():
    return "hello world"
"""
        )

    def tearDown(self):

        self.manager.clear()

        shutil.rmtree(
            self.temp_dir,
            ignore_errors=True,
        )

    # -------------------------------------------------
    # Discovery
    # -------------------------------------------------

    def test_discover(self):

        plugins = self.manager.discover(
            self.temp_dir
        )

        self.assertEqual(
            len(plugins),
            1,
        )

    # -------------------------------------------------
    # Load
    # -------------------------------------------------

    def test_load(self):

        plugin = self.manager.load(
            str(self.plugin_file)
        )

        self.assertEqual(
            plugin.metadata.name,
            "Sample Plugin",
        )

        self.assertEqual(
            self.manager.count(),
            1,
        )

        self.assertTrue(
            self.manager.exists(
                "Sample Plugin"
            )
        )

    # -------------------------------------------------
    # Load All
    # -------------------------------------------------

    def test_load_all(self):

        plugins = self.manager.load_all(
            self.temp_dir
        )

        self.assertEqual(
            len(plugins),
            1,
        )

        self.assertEqual(
            self.manager.count(),
            1,
        )

    # -------------------------------------------------
    # Lookup
    # -------------------------------------------------

    def test_plugin(self):

        self.manager.load(
            str(self.plugin_file)
        )

        plugin = self.manager.plugin(
            "Sample Plugin"
        )

        self.assertIsNotNone(
            plugin
        )

        self.assertEqual(
            plugin.metadata.version,
            "1.0.0",
        )

    def test_plugins(self):

        self.manager.load(
            str(self.plugin_file)
        )

        plugins = self.manager.plugins()

        self.assertEqual(
            len(plugins),
            1,
        )

    # -------------------------------------------------
    # Version
    # -------------------------------------------------

    def test_version(self):

        self.manager.load(
            str(self.plugin_file)
        )

        self.assertEqual(

            self.manager.version(
                "Sample Plugin"
            ),

            "1.0.0",

        )

    def test_upgrade(self):

        self.manager.load(
            str(self.plugin_file)
        )

        self.assertTrue(

            self.manager.upgrade(
                "Sample Plugin",
                "2.0.0",
            )

        )

        self.assertEqual(

            self.manager.version(
                "Sample Plugin"
            ),

            "2.0.0",

        )

    def test_downgrade(self):

        self.manager.load(
            str(self.plugin_file)
        )

        self.manager.upgrade(
            "Sample Plugin",
            "2.0.0",
        )

        self.assertTrue(

            self.manager.downgrade(
                "Sample Plugin",
                "1.5.0",
            )

        )

    # -------------------------------------------------
    # Permissions
    # -------------------------------------------------

    def test_permission(self):

        self.manager.load(
            str(self.plugin_file)
        )

        self.assertTrue(

            self.manager.has_permission(

                "Sample Plugin",

                PluginPermission.FILESYSTEM,

            )

        )

        self.assertFalse(

            self.manager.has_permission(

                "Sample Plugin",

                PluginPermission.NETWORK,

            )

        )

    # -------------------------------------------------
    # Execute
    # -------------------------------------------------

    def test_execute(self):

        self.manager.load(
            str(self.plugin_file)
        )

        result = self.manager.execute(

            "Sample Plugin",

            ["echo", "plugin"],

        )

        self.assertEqual(
            result.returncode,
            0,
        )

    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    def test_enable_disable(self):

        self.manager.load(
            str(self.plugin_file)
        )

        self.manager.disable(
            "Sample Plugin"
        )

        self.assertEqual(

            self.manager.status(
                "Sample Plugin"
            ),

            PluginStatus.DISABLED,

        )

        self.manager.enable(
            "Sample Plugin"
        )

        self.assertEqual(

            self.manager.status(
                "Sample Plugin"
            ),

            PluginStatus.LOADED,

        )

    # -------------------------------------------------
    # Reload
    # -------------------------------------------------

    def test_reload(self):

        self.manager.load(
            str(self.plugin_file)
        )

        plugin = self.manager.reload(
            "Sample Plugin"
        )

        self.assertEqual(

            plugin.metadata.name,

            "Sample Plugin",

        )

    # -------------------------------------------------
    # Refresh
    # -------------------------------------------------

    def test_refresh(self):

        self.manager.load(
            str(self.plugin_file)
        )

        plugins = self.manager.refresh(
            self.temp_dir
        )

        self.assertEqual(
            len(plugins),
            0,
        )

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def test_export(self):

        self.manager.load(
            str(self.plugin_file)
        )

        exported = self.manager.export()

        self.assertIn(
            "registry",
            exported,
        )

        self.assertIn(
            "versions",
            exported,
        )

        self.assertIn(
            "sandbox",
            exported,
        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def test_statistics(self):

        self.manager.load(
            str(self.plugin_file)
        )

        stats = self.manager.statistics()

        self.assertIn(
            "registry",
            stats,
        )

        self.assertIn(
            "versions",
            stats,
        )

        self.assertIn(
            "sandbox",
            stats,
        )

    # -------------------------------------------------
    # Unload
    # -------------------------------------------------

    def test_unload(self):

        self.manager.load(
            str(self.plugin_file)
        )

        self.assertTrue(

            self.manager.unload(
                "Sample Plugin"
            )

        )

        self.assertEqual(
            self.manager.count(),
            0,
        )

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def test_clear(self):

        self.manager.load(
            str(self.plugin_file)
        )

        self.manager.clear()

        self.assertTrue(
            self.manager.empty()
        )

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    def test_empty(self):

        self.assertTrue(
            self.manager.empty()
        )

        self.manager.load(
            str(self.plugin_file)
        )

        self.assertFalse(
            self.manager.empty()
        )

    # -------------------------------------------------
    # Dunder
    # -------------------------------------------------

    def test_len(self):

        self.manager.load(
            str(self.plugin_file)
        )

        self.assertEqual(
            len(self.manager),
            1,
        )

    def test_contains(self):

        self.manager.load(
            str(self.plugin_file)
        )

        self.assertIn(
            "Sample Plugin",
            self.manager,
        )

    def test_iterator(self):

        self.manager.load(
            str(self.plugin_file)
        )

        names = [

            plugin.metadata.name

            for plugin

            in self.manager

        ]

        self.assertEqual(
            names,
            ["Sample Plugin"],
        )


if __name__ == "__main__":

    print(
        "\n=== Plugin Manager Test ===\n"
    )

    unittest.main(
        verbosity=2,
    )