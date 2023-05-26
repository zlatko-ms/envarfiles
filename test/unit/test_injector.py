import unittest
import os
import tempfile

from processor import VarInjector


class TestVarInjector(unittest.TestCase):
    def test_001_variable_to_file_inject(self) -> None:
        # given a set of variables to inject
        varsToInject: dict = {"my_var_1": "val1", "my_var_2": "val2", "my_var_3": "val3"}
        # and given that the GH env file is available
        tempGHFileForTest = os.path.join(tempfile.mkdtemp(), "ghenvfile")
        os.environ["GITHUB_ENV"] = tempGHFileForTest
        # when we inject the variables
        VarInjector.injectVars(varsToInject)
        # then all the vars are availble in the file
        with open(tempGHFileForTest, "r") as ghfile:
            data = ghfile.read()
            for k, v in varsToInject.items():
                defToken = f"{k}={v}"
                self.assertTrue(defToken in data)
