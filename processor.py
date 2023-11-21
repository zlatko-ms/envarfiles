#!/usr/bin/python3

import sys
import re
import os.path
from itertools import chain, starmap
import json
import yaml


class ParamParser(object):
    CHECK_FOR_LISTS = ["paths", "select"]

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
                if isinstance(params[v], str):
                    newlist: list = list()
                    newlist.append(params[v])
                    params[v] = newlist
            else:
                params[v] = list()
        return params


class FileHelper(object):
    """Contains file utlility methods"""

    @classmethod
    def filterExistingFilesOnly(cts, fileList: list) -> list:
        ret: list = list()
        for fname in fileList:
            stripped = fname.lstrip().rstrip().strip()
            if os.path.isfile(stripped):
                ret.append(stripped)
        return ret


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


class VariableSelector(object):
    """Filters variables based on a seclection"""

    @classmethod
    def filter(ctx, allVars: dict, selection: list) -> dict:
        if len(selection) == 0:
            return allVars
        selectedVars = dict()
        for varName in selection:
            if varName in allVars.keys():
                selectedVars[varName] = allVars[varName]
        return selectedVars


class FileParserBase(object):
    """Base class for file format parsers"""

    @classmethod
    def accepts(cts, filePath: str) -> bool:
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
    def accepts(cts, filePath: str) -> bool:
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
    def accepts(cts, filePath: str) -> bool:
        return filePath.endswith(".json")

    @classmethod
    def getVariablesDict(cts, filePath: str, nestedsep: str = "_", fencoding: str = "utf-8") -> dict:
        with open(filePath, encoding=fencoding) as f:
            readdict: dict = json.load(f)
            return DictFlattner.flatten(readdict, nestedsep)


class YamlFileParser(FileParserBase):
    """Handles the parsing of YAML files"""

    @classmethod
    def accepts(cts, filePath: str) -> bool:
        return filePath.endswith(".yml") or filePath.endswith(".yaml")

    @classmethod
    def getVariablesDict(cts, filePath: str, nestedsep: str = "_", fencoding: str = "utf-8") -> dict:
        with open(filePath, encoding=fencoding) as f:
            readdict: dict = yaml.safe_load(f)
            return DictFlattner.flatten(readdict, nestedsep)


class FilesetParser(object):
    """Handles the parsing of a list of file, regardless of the file format"""

    ALL_PARSERS = [TextFileParser, JsonFileParser, YamlFileParser]

    @classmethod
    def getVariablesDict(cts, files: list, nestedsep: str = "_", fencoding: str = "utf-8") -> dict:
        allVars: dict = dict()
        for file in files:
            for parser in cts.ALL_PARSERS:
                if parser.accepts(file):
                    fileDict = parser.getVariablesDict(file, nestedsep, fencoding)
                    allVars.update(fileDict)
        return allVars


class OverrideManager(object):
    """Handles filtering for override behaviour"""

    @classmethod
    def filterVars(cts, override: bool, allVarDefs: dict) -> dict:
        if override:
            return allVarDefs
        varDefs: dict = dict()
        for k in allVarDefs.keys():
            if k not in os.environ:
                varDefs[k] = allVarDefs[k]
        return varDefs


class VarInjector(object):
    """Handles the injection of variables into github job variables"""

    @classmethod
    def injectVars(cts, varDefs: dict) -> None:
        ghEnvFileName = os.getenv("GITHUB_ENV")
        with open(ghEnvFileName, "a") as ghfile:
            for k in varDefs.keys():
                ghfile.write(f"{k}={varDefs[k]}\n")


def main():
    # deal with params
    passedArgs: dict = ParamParser.getParameters(" ".join(sys.argv[1:]))
    allFiles: list = passedArgs["paths"]
    varSelection: list = passedArgs["select"]
    varSeparator: list = passedArgs["separator"]
    overrideVars: bool = passedArgs["override"].lower() == "true"
    # parse all valid files with the matching parser
    overallVars: dict = FilesetParser.getVariablesDict(FileHelper.filterExistingFilesOnly(allFiles), varSeparator)
    # filter selection, if any provided
    fileredVars: dict = VariableSelector.filter(overallVars, varSelection)
    # filter depending on the override behaviour
    varsToInject: dict = OverrideManager.filterVars(overrideVars, fileredVars)
    # inject the vars
    VarInjector.injectVars(varsToInject)


if __name__ == "__main__":
    main()
