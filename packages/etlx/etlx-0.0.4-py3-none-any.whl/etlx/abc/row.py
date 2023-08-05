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
        return self[key]

