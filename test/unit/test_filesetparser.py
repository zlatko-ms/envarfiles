import unittest
import unittest.mock
from unittest.mock import patch

from processor import FilesetParser, JsonFileParser, YamlFileParser, TextFileParser


class TestFilesetParser(unittest.TestCase):
    @patch.object(TextFileParser, "getVariablesDict")
    @patch.object(JsonFileParser, "getVariablesDict")
    @patch.object(YamlFileParser, "getVariablesDict")
    def test_001_filesetParsingMocked(self, mockTextgetVariablesDict, mockJsongetVariablesDict, mockYamlgetVariablesDict) -> None:
        # mock each of the parser getVariablesDict() method
        mockTextgetVariablesDict.return_value = {"textName": "text"}
        mockJsongetVariablesDict.return_value = {"jsonName": "json"}
        mockYamlgetVariablesDict.return_value = {"yamlName": "yaml"}
        # call the filesetparser with a text, json and yaml file
        # each parser will be called and will return the mocked value
        files: list = ["/mylocation/myfile.json", "/mylocation/myfile.yaml", "/mylocation/myfile.properties"]
        allVars: dict = FilesetParser.getVariablesDict(files)
        # ensure the fileset parser collects results from the underlying parsers
        self.assertTrue("textName" in allVars.keys(), "var from text parser was collected")
        self.assertTrue("jsonName" in allVars.keys(), "var from json parser was collected")
        self.assertTrue("yamlName" in allVars.keys(), "var from yaml parser was collected")
        self.assertEqual(allVars["yamlName"], "yaml", "value of yaml defined variable is accurate ")
        self.assertEqual(allVars["jsonName"], "json", "value of json defined variable is accurate ")
        self.assertEqual(allVars["textName"], "text", "value of text defined variable is accurate ")
