#!/usr/bin/python3

import sys
import re
import os.path
from itertools import chain, starmap
import json
import yaml


class ParamParser(object):
    CHECK_FOR_LISTS = ["paths"]

    """Parses the parameter with the specific/unorthodox ways of passing lists from the gh action call"""

    @classmethod
    def getParameters(cls, paramLine: str) -> dict:
        params: dict = dict()
        tokens = re.split(r"(\w+)=", paramLine)
        keyFound: bool = False
        key: str = None
        for t in tokens:
            if len(t) > 0:
                if not keyFound:
                    key = t
                    keyFound = True
                elif key is not None:
                    z = t.rstrip()
                    if " " in z:
                        params[key] = z.split()
                    else:
                        params[key] = z
                    keyFound = False
                    key = None

        for v in cls.CHECK_FOR_LISTS:
            if v in params.keys():
                if type(params[v]) == str:
                    newlist: list = list()
                    newlist.append(params[v])
                    params[v] = newlist
        return params


class FileHelper(object):
    @classmethod
    def filterExistingFilesOnly(cts, fileList: list) -> list:
        ret: list = list()
        for fname in fileList:
            stripped = fname.lstrip().rstrip().strip()
            if os.path.isfile(stripped):
                ret.append(stripped)
        return ret

    @classmethod
    def varDictToFile(cts, vars: dict, filePath: str) -> None:
        with open(filePath, "w") as outfile:
            for k in vars.keys():
                outfile.write(f"{k}={vars[k]}\n")


class DictFlattner(object):
    """Flattens a dict with nested values, adapted from https://gist.github.com/alinazhanguwo/03206c554c1a8fcbe42a7d971efc7b26#file-flatten_json_iterative_solution-py, courtesy of Alina Zhang"""

    @classmethod
    def flatten(ctx, dictionary, separator="_"):
        """Flatten a nested json file"""

        def unpack(parent_key, parent_value):
            """Unpack one level of nesting in json file"""
            # Unpack one level only!!!

            if isinstance(parent_value, dict):
                for key, value in parent_value.items():
                    temp1 = parent_key + separator + key
                    yield temp1, value
            elif isinstance(parent_value, list):
                i = 0
                for value in parent_value:
                    temp2 = parent_key + separator + str(i)
                    i += 1
                    yield temp2, value
            else:
                yield parent_key, parent_value

        # Keep iterating until the termination condition is satisfied
        while True:
            # Keep unpacking the json file until all values are atomic elements (not dictionary or list)
            dictionary = dict(chain.from_iterable(starmap(unpack, dictionary.items())))
            # Terminate condition: not any value in the json file is dictionary or list
            if not any(isinstance(value, dict) for value in dictionary.values()) and not any(isinstance(value, list) for value in dictionary.values()):
                break

        return dictionary


class FileParserBase(object):
    """Base class for file format parsers"""

    @classmethod
    def isFileSupported(cts, filePath: str) -> bool:
        """Returns True if the file is supported by this parser"""
        pass

    @classmethod
    def getVariablesDict(cts, filePath: str, nestedsep: str, fencoding: str) -> dict:
        """Returns a dict with variable name as key and variable value as value"""
        pass


class TextFileParser(FileParserBase):
    """Handles the parsing of various key/value test files"""

    UNSUPPORTED_EXTENSIONS: list = ("json", "yml", "yaml")
    IGNORED_LINE_STARTS = ["#", "//", "*", "/*", "/**", "*/", " */", " *"]

    @classmethod
    def __stripLine(cts, line: str) -> str:
        return line.lstrip().rstrip().strip()

    @classmethod
    def __isValidLine(cts, line: str) -> bool:
        if len(line) == 0:
            return False
        for ignore in cts.IGNORED_LINE_STARTS:
            if line.startswith(ignore):
                return False
        return True

    @classmethod
    def readFile(cts, filePath: str, fencoding: str = "utf-8") -> list:
        validLines: list = list()
        with open(filePath, encoding=fencoding) as fileToRead:
            readLines = fileToRead.readlines()
            for readLine in readLines:
                strippedLine = cts.__stripLine(readLine)
                if cts.__isValidLine(strippedLine):
                    validLines.append(strippedLine)
        return validLines

    @classmethod
    def isFileSupported(cts, filePath: str) -> bool:
        for ue in cts.UNSUPPORTED_EXTENSIONS:
            if filePath.endswith(f".{ue}"):
                return False
        return True

    @classmethod
    def _stripVarLine(cts, line: str) -> str:
        stripped = line.lstrip().rstrip().strip()
        equalLStrip = re.sub(r"(\s)+=", "=", stripped)
        return re.sub(r"=(\s)+", "=", equalLStrip)

    @classmethod
    def getVariablesDict(cts, filePath: str, nestedsep: str = "_", fencoding: str = "utf-8") -> dict:
        ret: dict = dict()
        lines = cts.readFile(filePath, fencoding)
        for line in lines:
            stripped = cts._stripVarLine(line)
            if len(stripped) > 0:
                tokens = stripped.split("=")
                key = cts.__stripLine(tokens[0])
                value = tokens[1]
                ret[key] = value
        return ret


class JsonFileParser(FileParserBase):
    """Handles the parsing of JSON files"""

    @classmethod
    def isFileSupported(cts, filePath: str) -> bool:
        return filePath.endswith(".json")

    @classmethod
    def getVariablesDict(cts, filePath: str, nestedsep: str = "_", fencoding: str = "utf-8") -> dict:
        with open(filePath, encoding=fencoding) as f:
            readdict: dict = json.load(f)
            return DictFlattner.flatten(readdict, nestedsep)


class YamlFileParser(FileParserBase):
    """Handles the parsing of YAML files"""

    @classmethod
    def isFileSupported(cts, filePath: str) -> bool:
        return filePath.endswith(".yml") or filePath.endswith(".yaml")

    @classmethod
    def getVariablesDict(cts, filePath: str, nestedsep: str = "_", fencoding: str = "utf-8") -> dict:
        with open(filePath, encoding=fencoding) as f:
            readdict: dict = yaml.safe_load(f)
            return DictFlattner.flatten(readdict, nestedsep)


def main():
    overallVars: dict = dict()
    parsers = [TextFileParser, JsonFileParser, YamlFileParser]
    passedArgs: dict = ParamParser.getParameters(" ".join(sys.argv[1:]))
    allFiles: list = passedArgs["paths"]
    outfile: str = passedArgs["outfile"]

    # filter only readable/accessabe files
    files = FileHelper.filterExistingFilesOnly(allFiles)
    # parse files with correct parser and update global var definitions
    for file in files:
        for parser in parsers:
            if parser.isFileSupported(file):
                fileDict: dict = parser.getVariablesDict(file)
                overallVars.update(fileDict)
    # dump the variables to the specified file
    FileHelper.varDictToFile(overallVars, outfile)


if __name__ == "__main__":
    main()
