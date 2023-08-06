from .Console_Color import *

class Printer:

    @staticmethod
    def warning(text):
        color = Console_Color("warning").color
        print(color, "[Warning]", text)

    @staticmethod
    def log(text):
        color = Console_Color("log").color
        print(color, "[Log]", text)

    @staticmethod
    def info(text):
        color = Console_Color("info").color
        print(color, "[Info]", text)