class TwoWayDict(dict):
    def __init__(self, my_dict):
        dict.__init__(self, my_dict)
        self.rev_dict = {v : k for k,v in my_dict.items()}

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self.rev_dict.__setitem__(value, key)

    def pop(self, key):
        self.rev_dict.pop(self[key])
        dict.pop(self, key)