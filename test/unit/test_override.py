import unittest
import os

from processor import OverrideManager


class TestOverrideManager(unittest.TestCase):
    def test_001_override_set_existing_defined(self) -> None:
        # given a set of variables to inject
        varsToInject: dict = {"my_var_1": "val1", "my_var_2": "val2", "my_var_3": "val3"}
        # given one of the variable already exists in the evironnement
        os.environ["my_var_1"] = "oldVal"
        # when filtering the variables to inject
        vars: dict = OverrideManager.filterVars(False, varsToInject)
        # then only the not defined variables are returned
        self.assertTrue("my_var_2" in vars.keys())
        self.assertTrue("my_var_3" in vars.keys())
        self.assertFalse("my_var_1" in vars.keys())
        # and the values are correct
        self.assertEqual(varsToInject["my_var_2"], vars["my_var_2"])
        self.assertEqual(varsToInject["my_var_3"], vars["my_var_3"])

    def test_002_override_not_set_existing_defined(self) -> None:
        # given a set of variables to inject
        varsToInject: dict = {"my_var_10": "val1", "my_var_20": "val2", "my_var_30": "val3"}
        # given one of the variable already exists in the evironnement
        os.environ["my_var_10"] = "oldVal"
        # when filtering the variables to inject with override flag
        vars: dict = OverrideManager.filterVars(True, varsToInject)
        # then all the vars are updated
        for k in varsToInject.keys():
            self.assertTrue(k in vars.keys())
            self.assertEqual(vars[k], varsToInject[k])

    def test_002_override_not_set_existing_not_defined(self) -> None:
        # given a set of variables to inject
        varsToInject: dict = {"my_var_100": "val1", "my_var_200": "val2", "my_var_300": "val3"}
        # when filtering the variables to inject with override flag
        vars: dict = OverrideManager.filterVars(True, varsToInject)
        # then all the vars are updated
        for k in varsToInject.keys():
            self.assertTrue(k in vars.keys())
            self.assertEqual(vars[k], varsToInject[k])
