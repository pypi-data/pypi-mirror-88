from etlx import __version__ # noqa
from tests import TestCase


class TestFunc(TestCase):

    def test0_getTestDataPath(self):
        testDir = self.getTestDir()

        path = self.getTestDataPath()
        self.assertEqual(path, testDir+'/data')

        path = self.getTestDataPath('dummy.txt')
        self.assertEqual(path, testDir+'/data/dummy.txt')

    def test1_loadTestData(self):
        data = self.loadTestData('dummy.txt')
        self.assertEqual(data, 'DUMMY')
