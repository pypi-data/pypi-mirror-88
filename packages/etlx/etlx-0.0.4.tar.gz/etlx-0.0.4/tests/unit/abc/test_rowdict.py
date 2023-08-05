from etlx.abc import RowDict
import unittest


class Test_abc_RowDict(unittest.TestCase):

    def test01_interface_obj(self):
        x = RowDict()
        x['A'] = 'A'
        v = x.A
        self.assertEqual(v, 'A')

    def test02_interface_dict(self):
        x = RowDict()
        x['B'] = 'B'
        v = x['B']
        self.assertEqual(v, 'B')

    def test11_update_kwargs(self):
        x = RowDict()
        x.update(A='A', B='B')
        self.assertEqual(x.A, 'A')
        self.assertEqual(x.B, 'B')

    def test12_update_seq(self):
        x = RowDict()
        x.update([('A', 'A'), ('B', 'B')])
        self.assertEqual(x.A, 'A')
        self.assertEqual(x.B, 'B')

    def test13_update_dict(self):
        x = RowDict()
        x.update({'A': 'A', 'B': 'B'})
        self.assertEqual(x.A, 'A')
        self.assertEqual(x.B, 'B')


if __name__ == "__main__":
    unittest.main()    