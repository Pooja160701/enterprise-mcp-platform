import shutil
import tempfile
import unittest
from pathlib import Path

from app.plugins.dynamic_loader import DynamicLoader
from app.plugins.models import PluginStatus


class TestDynamicLoader(unittest.TestCase):

    def setUp(self):

        self.loader = DynamicLoader()

        self.temp_dir = tempfile.mkdtemp()

        self.plugin1 = Path(self.temp_dir) / "plugin_one.py"

        self.plugin2 = Path(self.temp_dir) / "plugin_two.py"

        self.plugin1.write_text(
            """
from app.plugins.models import PluginMetadata

PLUGIN_METADATA = PluginMetadata(
    name="Plugin One",
    version="1.0.0",
    author="Pooja",
    description="Plugin One",
)

TOOLS=["tool1"]

def tool1():
    return "tool1"
"""
        )

        self.plugin2.write_text(
            """
from app.plugins.models import PluginMetadata

PLUGIN_METADATA = PluginMetadata(
    name="Plugin Two",
    version="1.0.0",
    author="Pooja",
    description="Plugin Two",
)

TOOLS=["tool2"]

def tool2():
    return "tool2"
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

    def test_discover(self):

        files = self.loader.discover(
            self.temp_dir
        )

        self.assertEqual(
            len(files),
            2,
        )

    # -------------------------------------------------
    # Exists
    # -------------------------------------------------

    def test_exists(self):

        self.assertTrue(

            self.loader.exists(
                self.temp_dir
            )

        )

    # -------------------------------------------------
    # Load Single
    # -------------------------------------------------

    def test_load(self):

        plugin = self.loader.load(
            str(self.plugin1)
        )

        self.assertEqual(

            plugin.metadata.name,

            "Plugin One",

        )

        self.assertEqual(

            plugin.status,

            PluginStatus.LOADED,

        )

        self.assertEqual(

            self.loader.count(),

            1,

        )

    # -------------------------------------------------
    # Load All
    # -------------------------------------------------

    def test_load_all(self):

        plugins = self.loader.load_all(
            self.temp_dir
        )

        self.assertEqual(

            len(plugins),

            2,

        )

        self.assertEqual(

            self.loader.count(),

            2,

        )

    # -------------------------------------------------
    # Plugin Lookup
    # -------------------------------------------------

    def test_plugin(self):

        self.loader.load(
            str(self.plugin1)
        )

        plugin = self.loader.plugin(
            "Plugin One"
        )

        self.assertIsNotNone(
            plugin
        )

        self.assertEqual(

            plugin.metadata.version,

            "1.0.0",

        )

    def test_plugins(self):

        self.loader.load_all(
            self.temp_dir
        )

        plugins = self.loader.plugins()

        self.assertEqual(

            len(plugins),

            2,

        )

    # -------------------------------------------------
    # Reload
    # -------------------------------------------------

    def test_reload(self):

        self.loader.load(
            str(self.plugin1)
        )

        plugin = self.loader.reload(
            "Plugin One"
        )

        self.assertEqual(

            plugin.status,

            PluginStatus.LOADED,

        )

    # -------------------------------------------------
    # Unload
    # -------------------------------------------------

    def test_unload(self):

        self.loader.load(
            str(self.plugin1)
        )

        result = self.loader.unload(
            "Plugin One"
        )

        self.assertTrue(
            result
        )

        self.assertEqual(

            self.loader.count(),

            0,

        )

    # -------------------------------------------------
    # Refresh
    # -------------------------------------------------

    def test_refresh(self):

        self.loader.load(
            str(self.plugin1)
        )

        loaded = self.loader.refresh(
            self.temp_dir
        )

        self.assertEqual(

            len(loaded),

            1,

        )

        self.assertEqual(

            self.loader.count(),

            2,

        )

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def test_export(self):

        self.loader.load_all(
            self.temp_dir
        )

        exported = self.loader.export()

        self.assertIn(
            "plugins",
            exported,
        )

        self.assertEqual(

            len(
                exported["plugins"]
            ),

            2,

        )

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    def test_empty(self):

        self.assertTrue(
            self.loader.empty()
        )

        self.loader.load(
            str(self.plugin1)
        )

        self.assertFalse(
            self.loader.empty()
        )

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def test_clear(self):

        self.loader.load_all(
            self.temp_dir
        )

        self.loader.clear()

        self.assertTrue(
            self.loader.empty()
        )

        self.assertEqual(
            self.loader.count(),
            0,
        )


if __name__ == "__main__":

    print(
        "\n=== Dynamic Loader Test ===\n"
    )

    unittest.main(
        verbosity=2
    )