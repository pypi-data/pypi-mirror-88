from collections import deque


class SQLToken:

    def __init__(self, lexer, ttype, value=''):
        self.line = lexer.line
        self.col = lexer.col
        self.ttype = ttype
        self.value = value


class SQLLexer:

    WHITESPACE = 'WHITESPACE'
    COMMENT = 'COMMENT'
    NAME = 'NAME'
    QUOTED = 'QUOTED'
    INT = 'INT'
    FLOAT = 'FLOAT'
    CHAR = 'CHAR'
    COMMA = ','
    DOT = '.'
    EOS = ';'

    def __init__(self, sql, whitespaces=True):
        self.itr = iter(sql)
        self.buffer = deque()
        self.line = 1
        self.col = 1
        self.whitespaces = whitespaces

    def load_buffer(self):
        while len(self.buffer) < 3:
            c = next(self.itr, None)
            self.buffer.append(c)
        return self.buffer[0]

    def read_char(self):
        self.load_buffer()
        c = self.buffer.popleft()
        if not c:
            return None
        self.col += 1
        if c == '\n':
            self.line += 1
            self.col = 1
        return c

    def push(self, c):
        self.buffer.appendleft(c)
        self.col -= 1

    def is_whitespace(self, c):
        return c and c in (' ', '\t', '\n')

    def is_alpha(self, c):
        return c and ((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_')

    def is_digit(self, c):
        return c and c >= '0' and c <= '9'

    def read_whitespace(self):
        x = SQLToken(self,  self.WHITESPACE)
        c = self.read_char()
        while self.is_whitespace(c):
            x.value += c
            c = self.read_char()
        self.push(c)
        return x

    def read_name(self):
        x = SQLToken(self,  self.NAME)
        c = self.read_char()
        while self.is_alpha(c) or self.is_digit(c):
            x.value += c
            c = self.read_char()
        self.push(c)
        return x

    def read_number(self):
        x = SQLToken(self,  self.INT)
        c = self.read_char()
        while self.is_digit(c):
            x.value += c
            c = self.read_char()
        if c != '.':
            self.push(c)
            return x
        x.ttype = self.FLOAT
        x.value += c
        c = self.read_char()
        while self.is_digit(c):
            x.value += c
            c = self.read_char()
        self.push(c)
        return x

    def read_comment_single(self):
        x = SQLToken(self,  self.COMMENT)
        c = self.read_char()
        while c and c != '\n':
            x.value += c
            c = self.read_char()
        self.push(c)
        return x

    def read_comment_multi(self):
        x = SQLToken(self,  self.COMMENT)
        c = self.read_char()
        while c and x.value[-2:] != '*/':
            x.value += c
            c = self.read_char()
        self.push(c)
        return x

    def read_quoted(self):
        q = self.read_char()
        x = SQLToken(self, self.CHAR if q == "'" else self.QUOTED)
        while True:
            c = self.read_char()
            if c != q:
                x.value += c
            elif c == q:
                c1 = self.read_char()
                if c1 == q:
                    x.value += q
                    c = self.read_char()
                else:
                    self.push(c1)
                    break
        return x

    def __iter__(self):
        return self

    def __next__(self):
        self.load_buffer()
        if self.buffer[0] is None:
            raise StopIteration()
        if self.is_whitespace(self.buffer[0]):
            token = self.read_whitespace()
            if self.whitespaces:
                return token
        if self.buffer[0] == '#':
            return self.read_comment_single()
        if (self.buffer[0], self.buffer[1]) == ('-', '-'):
            return self.read_comment_single()
        if (self.buffer[0], self.buffer[1]) == ('/', '*'):
            return self.read_comment_multi()
        if self.is_alpha(self.buffer[0]):
            return self.read_name()
        if self.buffer[0] == '[':
            self.read_char()
            token = self.read_name()
            if self.buffer[0] != ']':
                raise ValueError(f"{self.line}: {self.buffer[0]}")
            self.read_char()
            return token
        if self.is_digit(self.buffer[0]):
            return self.read_number()
        if self.buffer[0] in ("'", '"', '`'):
            return self.read_quoted()
        if self.buffer[0] in ('(', ')'):
            token = SQLToken(self, self.buffer[0], self.buffer[0])
            self.read_char()
            return token
        if (self.buffer[0], self.buffer[1]) in (('<', '='), ('>', '='), ('!', '='), ('<', '>'), ('+', '=')):
            v = self.buffer[0]+self.buffer[1]
            token = SQLToken(self, v, v)
            self.read_char()
            self.read_char()
            return token
        if self.buffer[0] in (".", ',', ';', '+', '-', '/', '*', '<', '>', '=', '|'):
            v = self.buffer[0]
            token = SQLToken(self, v, v)
            self.read_char()
            return token
        raise ValueError(f"{self.line}: {self.buffer[0]}")
