import unittest

from processor import TextFileParser


class TestTextParser(unittest.TestCase):
    shellCommentedFile = "test/fixtures/unit/commented.shell.properties"
    javaCommentedFile = "test/fixtures/unit/commented.java.properties"
    validFile = "test/fixtures/unit/example.properties"

    def test_001_file_pattern_accetance(self) -> None:
        filesNotParsable = ["conf.json", "conf.yaml", "conf.yml"]
        for f in filesNotParsable:
            self.assertFalse(TextFileParser.isFileSupported(f))
        filesParsable = ["conf.properties", "conf.cfg", "conf"]
        for f in filesParsable:
            self.assertTrue(TextFileParser.isFileSupported(f), f"text file {f} supported")

    def test_002_shell_comments_ignored(self) -> None:
        lines: list = TextFileParser.readFile(self.shellCommentedFile)
        # ensure a single line was read, others were ignored
        self.assertEqual(len(lines), 1, "exact number of valid lines read from shell commented file")
        # ensure we have the correct line read
        self.assertEqual("MyVar = Defined", lines[0], "exact valid line read from shell commented file")

    def test_003_java_comments_ignored(self) -> None:
        lines: list = TextFileParser.readFile(self.javaCommentedFile)
        # ensure a single line was read, others were ignored
        self.assertEqual(len(lines), 1, "exact number of valid lines read from java commented file")
        # ensure we have the correct line read
        self.assertEqual("MyVar = Defined", lines[0], "exact valid line read from java commented file")

    def test_004_var_declaration_strip_spaces(self) -> None:
        defLine = "  myvar  =    myval"
        line = TextFileParser._stripVarLine(defLine)
        self.assertEqual(line, "myvar=myval", "var declaration with spaces correctly stripped")

    def test_004_var_declaration_strip_nospaces(self) -> None:
        defLine = "myvar=myval"
        line = TextFileParser._stripVarLine(defLine)
        self.assertEqual(line, "myvar=myval", "var declaration without spaces correctly stripped")

    def test_005_variables_read(self) -> None:
        vars: dict = TextFileParser.getVariablesDict(self.validFile)
        # ensure we get two keys
        self.assertEqual(len(vars.keys()), 2)
        # assert we got the correct keys
        expectedVarNames = ["MyVar", "my.property"]
        for e in expectedVarNames:
            self.assertTrue(e in vars.keys(), f"asserting var {e} found in the file")
        # assert we got the correct values
        self.assertEqual(vars["MyVar"], "Defined", "value of variable 'MyVar' is 'Defined'")
        self.assertEqual(vars["my.property"], "myvalue", "value of variable 'my.property' is myvalue'")
