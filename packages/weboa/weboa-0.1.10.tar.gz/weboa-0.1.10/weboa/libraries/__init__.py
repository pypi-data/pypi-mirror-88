class Library:
    def __init__(self):
        self.name = ""

    def load_script(self):
        return self.js

    def load_script(self):
        return self.js

    def load_link(self):
        return self.css

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return other+self.__str__()

    def __radd__(self, other):
        return other+self.__str__()

from .MDB5 import *
from .Umbrella import *
from .Fonts import *