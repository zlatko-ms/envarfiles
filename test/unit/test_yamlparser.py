import unittest

from processor import YamlFileParser


class TestYAMLParser(unittest.TestCase):
    simpleFile = "test/fixtures/unit/simple.yaml"
    nestedFile = "test/fixtures/unit/nested.yaml"

    def test_001_file_pattern_accetance(self) -> None:
        self.assertTrue(YamlFileParser.accepts("/no/path/file.yaml"), ".yaml extension is supported")
        self.assertTrue(YamlFileParser.accepts("/no/path/file.yml"), ".yml extension is supported")
        self.assertFalse(YamlFileParser.accepts("/no/path/file"), "files without extensions are not supported")
        self.assertFalse(YamlFileParser.accepts("/no/path/file.txt"), "only yaml and yml extensions are supported")

    def test_002_simple_file(self) -> None:
        props: dict = YamlFileParser.getVariablesDict(self.simpleFile)
        self.assertEqual(len(props.keys()), 2, "simple file has 2 variables")
        self.assertTrue("major" in props.keys(), "simple contains variable major")
        self.assertTrue("minor" in props.keys(), "simple contains variable minor")
        self.assertEqual(props["major"], "1", "variable major has the expected value")
        self.assertEqual(props["minor"], "2", "variable minor has the expected value")

    def test_003_nested_file(self) -> None:
        props: dict = YamlFileParser.getVariablesDict(self.nestedFile)
        self.assertTrue("build_version_minor" in props.keys(), "nested contains variable build_version_minor")
        self.assertTrue("build_version_major" in props.keys(), "nested contains variable build_version_major")
        self.assertEqual(props["build_version_major"], "1", "variable build_version_major has the expected value")
        self.assertEqual(props["build_version_minor"], "2", "variable build_version_minor has the expected value")

    def test_004_nested_file_custom_se(self) -> None:
        props: dict = YamlFileParser.getVariablesDict(self.nestedFile, ".")
        self.assertEqual(len(props.keys()), 2, "nested file has 2 variables")
        self.assertTrue("build.version.minor" in props.keys(), "nested contains variable build.version.minor")
        self.assertTrue("build.version.major" in props.keys(), "nested contains variable build.version.major")
        self.assertEqual(props["build.version.major"], "1", "variable build.version.major has the expected value")
        self.assertEqual(props["build.version.minor"], "2", "variable build.version.minor has the expected value")
