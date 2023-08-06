from collections import OrderedDict


class RowDict(OrderedDict):

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def update(self, *args, **kwargs):
        for seq in args:
            if isinstance(seq, dict):
                seq = seq.items()
            for key, value in seq:
                self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    def __getattr__(self, key):
        if key not in self:
            raise AttributeError(key)
        return self[key]


def rowExtract(x, columns):
    return RowDict((cname, x.get(cname)) for cname in columns)


def rowTuple(x, columns):
    return tuple(x.get(cname) for cname in columns)
