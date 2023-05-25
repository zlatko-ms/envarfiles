import unittest

from processor import DictFlattner


class TestDictFlattener(unittest.TestCase):
    myprops: dict = {"version": {"major": "1", "minor": "2", "patch": "3", "build": {"tag": "latest"}}}

    def test_001_flatten_default_sep(self) -> None:
        flattened: dict = DictFlattner.flatten(self.myprops)
        self.assertEqual(flattened["version_major"], "1")
        self.assertEqual(flattened["version_minor"], "2")
        self.assertEqual(flattened["version_patch"], "3")
        self.assertEqual(flattened["version_build_tag"], "latest")

    def test_002_flatten_custom_sep(self) -> None:
        flattened: dict = DictFlattner.flatten(self.myprops, ".")
        self.assertEqual(flattened["version.major"], "1")
        self.assertEqual(flattened["version.minor"], "2")
        self.assertEqual(flattened["version.patch"], "3")
        self.assertEqual(flattened["version.build.tag"], "latest")
