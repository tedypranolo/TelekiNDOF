class ItemAccess:
    def __getitem__(self, key):
        if isinstance(key, str):
            return getattr(self, key)
        else:
            return super().__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(key, str):
            setattr(self, key, value)
        else:
            super().__setitem__(key, value)
