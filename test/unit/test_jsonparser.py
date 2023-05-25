import unittest

from processor import JsonFileParser


class TestJsonParser(unittest.TestCase):
    simpleFile = "test/fixtures/unit/simple.json"
    nestedFile = "test/fixtures/unit/nested.json"

    def test_001_file_pattern_accetance(self) -> None:
        self.assertTrue(JsonFileParser.accepts("/no/path/file.json"), ".json extensions are supported")
        self.assertFalse(JsonFileParser.accepts("/no/path/file"), "no extensions are not supported")
        self.assertFalse(JsonFileParser.accepts("/no/path/file.txt"), "only json extensions are not supported")

    def test_002_simple_file(self) -> None:
        props: dict = JsonFileParser.getVariablesDict(self.simpleFile)
        self.assertEqual(len(props.keys()), 2, "simple file has 2 variables")
        self.assertTrue("major" in props.keys(), "simple contains variable major")
        self.assertTrue("minor" in props.keys(), "simple contains variable minor")
        self.assertEqual(props["major"], "1", "variable major has the expected value")
        self.assertEqual(props["minor"], "2", "variable minor has the expected value")

    def test_003_nested_file(self) -> None:
        props: dict = JsonFileParser.getVariablesDict(self.nestedFile)
        self.assertTrue("build_version_minor" in props.keys(), "nested contains variable build_version_minor")
        self.assertTrue("build_version_major" in props.keys(), "nested contains variable build_version_major")
        self.assertEqual(props["build_version_major"], "1", "variable build_version_major has the expected value")
        self.assertEqual(props["build_version_minor"], "2", "variable build_version_minor has the expected value")

    def test_003_nested_file_custom_se(self) -> None:
        props: dict = JsonFileParser.getVariablesDict(self.nestedFile, ".")
        self.assertEqual(len(props.keys()), 2, "nested file has 2 variables")
        self.assertTrue("build.version.minor" in props.keys(), "nested contains variable build.version.minor")
        self.assertTrue("build.version.major" in props.keys(), "nested contains variable build.version.major")
        self.assertEqual(props["build.version.major"], "1", "variable build.version.major has the expected value")
        self.assertEqual(props["build.version.minor"], "2", "variable build.version.minor has the expected value")
