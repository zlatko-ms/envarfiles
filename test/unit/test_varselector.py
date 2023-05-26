import unittest

from processor import VariableSelector


class TestVarSelector(unittest.TestCase):
    allVarDefs: dict = {"var1": "val1", "var2": "val2", "var3": "val3", "var4": "val4"}

    def test_001_empty_selector(self) -> None:
        selector: list = ()
        filteredDefs = VariableSelector.filter(self.allVarDefs, selector)
        self.assertEqual(len(filteredDefs.keys()), len(self.allVarDefs), "empty selector returns all vars")
        for v in self.allVarDefs.keys():
            self.assertTrue(v in filteredDefs.keys(), f"var {v} has been selected")
            self.assertEqual(filteredDefs[v], self.allVarDefs[v], f"value of var {v} is exact")

    def test_002_non_empty_selector(self) -> None:
        selector: list = ("var1", "var2")
        filteredDefs = VariableSelector.filter(self.allVarDefs, selector)
        self.assertEqual(len(filteredDefs.keys()), 2, "only the 2 selected vars are returned by the filter")
        for v in selector:
            self.assertTrue(v in filteredDefs.keys(), f"var {v} is in selection")
            self.assertEquals(filteredDefs[v], self.allVarDefs[v], f"var {v} had exect value")

    def test_003_non_empty_selector_no_overlap(self) -> None:
        selector: list = ("var42", "var84")
        filteredDefs = VariableSelector.filter(self.allVarDefs, selector)
        self.assertEqual(len(filteredDefs.keys()), 0, "none of the collected variables is matching filter")
