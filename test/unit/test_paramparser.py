import unittest

from processor import ParamParser


class TestParamParser(unittest.TestCase):
    paramLineCombined: str = "single=a mutiple=1 2 3 4 mutiple2=5 6 7 8 single2=b"
    paramLineSingleStringVal: str = "single=somestring"
    paramLineSingleListVal: str = "multple=a b c"
    paramLineSpecifics: str = "paths=a"

    def test_001_single_param_parsing(self) -> None:
        params: dict = ParamParser.getParameters(self.paramLineSingleStringVal)
        # assert single is found in the param list
        self.assertTrue("single" in params.keys())
        # assert value of single param is a string
        self.assertTrue(type(params["single"]) is str)
        # assert value of single param is a string
        self.assertEqual(params["single"], "somestring")

    def test_002_list_param_parsing(self) -> None:
        params: dict = ParamParser.getParameters(self.paramLineSingleListVal)
        # assert multiple is found in the param list
        self.assertTrue("multple" in params.keys())
        # assert value of single param is a string
        self.assertTrue(type(params["multple"]) is list)
        # assert all the values are present in the array
        for token in ["a", "b", "c"]:
            self.assertTrue(token in params["multple"])

    def test_003_combined_param_parsing(self) -> None:
        params: dict = ParamParser.getParameters(self.paramLineCombined)
        # assert multiples are found in the param list
        multiples = ["mutiple", "mutiple2"]
        for m in multiples:
            self.assertTrue(m in params.keys())
        # assert values for multiples are lists
        for m in multiples:
            self.assertTrue(type(params[m]) is list)
        # assert singles are found in the param list
        singles = ["single", "single2"]
        for s in singles:
            self.assertTrue(s in params.keys())
        # assert values for signles are strings
        for s in singles:
            self.assertTrue(type(params[s]) is str)
        # assert singles values are correct
        self.assertEqual(params[singles[0]], "a")
        self.assertEqual(params[singles[1]], "b")
        # assert multuple values are correct
        mvalues1 = ["1", "2", "3", "4"]
        for mval in mvalues1:
            self.assertTrue(mval in params[multiples[0]])
        mvalues2 = ["5", "6", "7", "8"]
        for mval in mvalues2:
            self.assertTrue(mval in params[multiples[1]])

    def test_004_sepecicifc_param_fixing(self) -> None:
        params: dict = ParamParser.getParameters(self.paramLineSpecifics)
        # assert that param 'paths' is always retuened as a list
        self.assertEqual(type(params["paths"]), list, "param paths is adjusted to list even if provided as string")
        self.assertEqual(len(params["paths"]), 1, "param paths has a single string value")
