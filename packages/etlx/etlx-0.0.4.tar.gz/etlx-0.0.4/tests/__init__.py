import unittest
import os
import inspect


class TestCase(unittest.TestCase):
    """Base class for unittest style tests"""

    DATA_DIR_NAME = 'data'

    @classmethod
    def getTestDir(cls) -> str:
        """Returns director of the source file"""
        return os.path.dirname(inspect.getfile(cls))

    @classmethod
    def getTestDataPath(cls, relativePath=None) -> str:
        """Returns full path to data bound to TestCase.
        The path is based on location of the source file:
        path = dir(file(class)/data/<relativePath>
        """
        testDir = cls.getTestDir()
        testDataDir = os.path.join(testDir, cls.DATA_DIR_NAME)
        if not relativePath:
            return testDataDir
        return os.path.join(testDataDir, relativePath)

    @classmethod
    def loadTestData(cls, relativePath):
        path = cls.getTestDataPath(relativePath)
        with open(path, 'r') as f:
            return f.read()
