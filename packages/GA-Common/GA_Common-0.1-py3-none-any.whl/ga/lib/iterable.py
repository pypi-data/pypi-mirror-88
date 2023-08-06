class Iterable(object):
    """
    可迭代对象
    """
    def __iter__(self):
        return self

    def __next__(self):
        self.next()
