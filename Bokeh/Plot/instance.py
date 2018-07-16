"""
Singleton class for data set and its information
"""


class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Instance(metaclass=Singleton):
    """
        Singleton class
    """
    def __init__(self, data, attr_values, attr_list, attr_values_dict, attr_dict, cmap):
        self.data = data
        self.attr_values = attr_values
        self.attr_list = attr_list
        self.attr_values_dict = attr_values_dict
        self.attr_dict = attr_dict
        self.cmap = cmap

    def update(self, a):
        """
        :param a:
        :return:
        """
        self.a = a



