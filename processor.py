#!/usr/bin/python3

import sys
import re
from numpy import loadtxt


class ParamParser(object):
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
        return params


class FileParserBase(object):
    """Base class for file format parsers"""

    @classmethod
    def isFileSupported(cts, filePath: str) -> bool:
        """Returns True if the file is supported by this parser"""
        pass

    @classmethod
    def getVariablesDict(cts, filePath: str) -> dict:
        """Returns a dict with variable name as key and variable value as value"""
        pass


# text parser class
class TextFileParser(FileParserBase):
    """Handles the parsing of various key/value test files"""

    UNSUPPORTED_EXTENSIONS: list = ("json", "yml", "yaml")
    IGNORED_LINE_STARTS = ["#", "//", "*", "/*", "/**", "*/", " */", " *"]

    @classmethod
    def readFile(cts, filePath: str) -> list:
        lines = loadtxt(
            filePath,
            comments=cts.IGNORED_LINE_STARTS,
            delimiter=",",
            dtype=str,
            unpack=False,
        )
        return lines.tolist()

    @classmethod
    def isFileSupported(cts, filePath: str) -> bool:
        for ue in cts.UNSUPPORTED_EXTENSIONS:
            if filePath.endswith(f".{ue}"):
                return False
        return True

    @classmethod
    def getVariablesDict(cts, filePath: str) -> dict:
        ret: dict = dict()
        lines = cts.readFile(filePath)
        for line in lines:
            stripped = line.rstrip().strip()
            nospace = re.sub(r"(\s)=(\s)", "=", stripped)
            if len(nospace) > 0:
                tokens = nospace.split("=")
                key = tokens[0]
                value = tokens[1]
                ret[key] = value
        return ret


def main():
    passedArgs: dict = ParamParser.getParameters(" ".join(sys.argv[1:]))
    print(passedArgs)
    file = "test/fixtures/release.comments.properties"
    vars: dict = TextFileParser.getVariablesDict(file)
    for k in vars.keys():
        print(f"{k}=>{vars[k]}")


if __name__ == "__main__":
    main()
