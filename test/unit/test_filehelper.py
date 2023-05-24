import unittest

from processor import FileHelper


class TestFileHelper(unittest.TestCase):
    def test_001_filterNonExisting(self) -> None:
        files: list = ["./test/fixtures/unit/example.properties", "xyz", "zdbg.zdbg"]
        filteredFiles: list = FileHelper.filterExistingFilesOnly(files)
        # assert single file foud
        self.assertEqual(len(filteredFiles), 1, "filter removes non accessible/readable files")
        # assert valid single file
        self.assertEqual(filteredFiles[0], files[0], f"only {files[0]} exist and is kept in the list")
