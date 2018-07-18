"""
Singleton class for data set and its information
"""
import os

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

    @classmethod
    def clear_instance(cls):
        """ Delete the instance """
        del cls._instance


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
        self.data_set = None

    def update(self, data, attr_values, attr_list, attr_values_dict, attr_dict, cmap):
        """
            Update Singleton instance values
        """
        self.data = data
        self.attr_values = attr_values
        self.attr_list = attr_list
        self.attr_values_dict = attr_values_dict
        self.attr_dict = attr_dict
        self.cmap = cmap

    def update_data_set(self, file_name):
        """
            Updated uploaded data set and remove previous one
        """
        if not self.data_set and file_name not in ["car", "lens"]:
            self.data_set = file_name
        else:
            if self.data_set not in ["car", "lens"]:
                cwd = os.getcwd()
                file_path = cwd + "/../Bokeh/Data/" + self.data_set
                os.remove(file_path)
                self.data_set = file_name
