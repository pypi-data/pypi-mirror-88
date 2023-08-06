#!/usr/bin/env python
from weboa import *
from weboa import __VERSION__
import sys

def runcli():
    print("Welcome to Weboa!")
    commands = {
        "version": ("--version", "-v"),
        "init": ("--init","-i"),
        "langs": ("--langs", "-l"),
        "start": ("--start", "-s"),
        "update": ("--update","-u")
    }

    args = sys.argv
    for i in range(len(args)):
        if args[i] in commands["version"]:
            print(f"Weboa version is {__VERSION__}")
        elif args[i] in commands["update"]:
            os.system("pip install weboa --upgrade")
            os.system("pip3 install weboa --upgrade")
        elif args[i] in commands["start"]:
            Processing.Save_Path(os.getcwd())
            Printer.info(f"Weboa is installed at {prepare.Package.stream}")

        elif args[i] in commands["init"]:
            _path = os.getcwd()
            Processing.Save_Path(_path)
            php=PHP(path="")
            php.BUILDFOLDER = "/"
            php.FS()
            php.index()
            php.language()
            php.project()
            php.libs()
            php.ico()
            php.css()
            php.robots()
            php.js()
            php.img()
            php.readme()
            php.gitignore()
            php.ico_langs()
            print(f"Langs {args[i+1]}")

if(__name__=="__main__"):
    runcli()