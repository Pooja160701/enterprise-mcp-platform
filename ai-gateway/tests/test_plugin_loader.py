import shutil
import tempfile
import unittest
from pathlib import Path

from app.plugins.models import (
    PluginMetadata,
    PluginStatus,
)
from app.plugins.plugin_loader import PluginLoader


class TestPluginLoader(unittest.TestCase):

    def setUp(self):

        self.loader = PluginLoader()

        self.temp_dir = tempfile.mkdtemp()

        self.plugin_file = Path(
            self.temp_dir
        ) / "sample_plugin.py"

        self.plugin_file.write_text(
            """
from app.plugins.models import PluginMetadata

PLUGIN_METADATA = PluginMetadata(
    name="Sample Plugin",
    version="1.0.0",
    author="Pooja",
    description="Enterprise Test Plugin",
)

TOOLS = [
    "hello",
    "goodbye",
]

def hello():
    return "hello"

def goodbye():
    return "goodbye"
"""
        )

    def tearDown(self):

        self.loader.clear()

        shutil.rmtree(
            self.temp_dir,
            ignore_errors=True,
        )

    # -------------------------------------------------
    # Discovery
    # -------------------------------------------------

    def test_discover_plugins(self):

        plugins = self.loader.discover(
            self.temp_dir
        )

        self.assertEqual(
            len(plugins),
            1,
        )

        self.assertTrue(
            plugins[0].endswith(
                "sample_plugin.py"
            )
        )

    # -------------------------------------------------
    # Load
    # -------------------------------------------------

    def test_load_file(self):

        plugin = self.loader.load_file(
            str(self.plugin_file)
        )

        self.assertEqual(
            plugin.metadata.name,
            "Sample Plugin",
        )

        self.assertEqual(
            plugin.status,
            PluginStatus.LOADED,
        )

        self.assertEqual(
            len(plugin.tools),
            2,
        )

    def test_plugin_exists(self):

        self.loader.load_file(
            str(self.plugin_file)
        )

        self.assertTrue(
            self.loader.has_plugin(
                "Sample Plugin"
            )
        )

    def test_get_plugin(self):

        self.loader.load_file(
            str(self.plugin_file)
        )

        plugin = self.loader.plugin(
            "Sample Plugin"
        )

        self.assertIsNotNone(plugin)

        self.assertEqual(
            plugin.metadata.version,
            "1.0.0",
        )

    def test_get_module(self):

        self.loader.load_file(
            str(self.plugin_file)
        )

        module = self.loader.module(
            "Sample Plugin"
        )

        self.assertTrue(
            hasattr(
                module,
                "hello",
            )
        )

    # -------------------------------------------------
    # Reload
    # -------------------------------------------------

    def test_reload(self):

        self.loader.load_file(
            str(self.plugin_file)
        )

        plugin = self.loader.reload(
            "Sample Plugin"
        )

        self.assertEqual(
            plugin.status,
            PluginStatus.LOADED,
        )

    # -------------------------------------------------
    # Unload
    # -------------------------------------------------

    def test_unload(self):

        self.loader.load_file(
            str(self.plugin_file)
        )

        result = self.loader.unload(
            "Sample Plugin"
        )

        self.assertTrue(result)

        plugin = self.loader.plugin(
            "Sample Plugin"
        )

        self.assertEqual(
            plugin.status,
            PluginStatus.UNLOADED,
        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def test_statistics(self):

        self.loader.load_file(
            str(self.plugin_file)
        )

        stats = self.loader.statistics()

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

        self.loader.load_file(
            str(self.plugin_file)
        )

        exported = self.loader.export()

        self.assertIn(
            "plugins",
            exported,
        )

        self.assertEqual(
            len(exported["plugins"]),
            1,
        )

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def test_clear(self):

        self.loader.load_file(
            str(self.plugin_file)
        )

        self.loader.clear()

        self.assertEqual(
            len(
                self.loader.plugins()
            ),
            0,
        )


if __name__ == "__main__":

    print("\n=== Plugin Loader Test ===\n")

    unittest.main(
        verbosity=2
    )