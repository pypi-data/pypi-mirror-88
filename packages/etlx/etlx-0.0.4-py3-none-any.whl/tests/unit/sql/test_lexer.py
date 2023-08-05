import unittest
from etlx.sql.parse.lexer import SQLLexer


class Test_sql_SQLLexer(unittest.TestCase):

    def test0_name(self):
        sql = "SELECT AbcZ_109"
        lexer = SQLLexer(sql)
        tokens = list(lexer)
        self.assertEqual(len(tokens), 3)
        x = tokens[0]
        self.assertEqual(x.ttype, 'NAME')
        self.assertEqual(x.value, 'SELECT')
        self.assertEqual(x.line, 1)
        self.assertEqual(x.col, 1)

        x = tokens[1]
        self.assertEqual(x.ttype, 'WHITESPACE')
        self.assertEqual(x.value, ' ')
        self.assertEqual(x.line, 1)
        self.assertEqual(x.col, 7)

        x = tokens[2]
        self.assertEqual(x.ttype, 'NAME')
        self.assertEqual(x.value, 'AbcZ_109')
        self.assertEqual(x.line, 1)
        self.assertEqual(x.col, 8)

    def test1_num(self):
        sql = """12 
        3.14 987654321"""
        lexer = SQLLexer(sql)
        tokens = list(lexer)
        self.assertEqual(len(tokens), 5)
        x = tokens[0]
        self.assertEqual(x.ttype, 'INT')
        self.assertEqual(x.value, '12')
        self.assertEqual(x.line, 1)
        self.assertEqual(x.col, 1)

        x = tokens[1]
        self.assertEqual(x.ttype,  'WHITESPACE')
        self.assertEqual(x.line,  1)
        self.assertEqual(x.col,  3)

        x = tokens[2]
        self.assertEqual(x.ttype,  'FLOAT')
        self.assertEqual(x.value, '3.14')
        self.assertEqual(x.line,  2)
        self.assertEqual(x.col,  9)

    def test2_num(self):
        sql = """12 -- AAA
        /* 3.14 98765
        4321*/"""
        lexer = SQLLexer(sql, False)
        tokens = list(lexer)
        self.assertEqual(len(tokens), 3)
        for x in tokens:
            print(x.ttype, x.value[:30])

    def test2_sample_01(self):
        sql = """
    SELECT FirstName, LastName, 
           OrderCount = (SELECT COUNT(O.Id) FROM [Order] O WHERE O.CustomerId = C.Id)
      FROM "Customer" C
      WHERE L<1 OR G>2 AND LE<=3 AND GE>=4 OR NE1!=5 OR NE2<>6
      ;""" 
        lexer = SQLLexer(sql, False)
        while True:
            x = next(lexer, None)
            if x is None:
                break
            if x.ttype == SQLLexer.WHITESPACE:
                continue
            if x.ttype == SQLLexer.NAME and x.value.upper() in ('FROM', 'JOIN'):
                prefix, name = None, None
                x = next(lexer, None)
                if x.ttype not in (SQLLexer.NAME, SQLLexer.QUOTED):
                    continue
                name = x.value
                x = next(lexer, None)
                if x.ttype == '.':
                    prefix = name
                    x = next(lexer, None)
                    if x.ttype not in (SQLLexer.NAME, SQLLexer.QUOTED):
                        raise ValueError(x.value[:30])
                    name = x.value
                print(x.line, x.col, prefix, name)
