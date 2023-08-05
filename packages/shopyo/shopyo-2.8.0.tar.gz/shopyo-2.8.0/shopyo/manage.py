import subprocess

import click

from app import app

from shopyoapi.cmd import clean
from shopyoapi.cmd import create_module
from shopyoapi.cmd import initialise
from shopyoapi.database import autoload_models
from shopyoapi.init import db


def runserver():
    app.run(host="0.0.0.0")


@click.command()
@click.argument("args", nargs=-1)
def process(args):
    if args[0] == "initialise":
        autoload_models()
        initialise()
    elif args[0] == "clean":
        clean()
    elif args[0] == "runserver":
        runserver()
    elif args[0] == "rundebug":
        app.run(debug=True, host="0.0.0.0")
        try:
            if args[1]:
                app.run(debug=True, host="0.0.0.0", port=int(args[1]))
        except IndexError as e:
            raise e
    elif args[0] == "test":
        print("test ok")
    elif args[0] == "startapp" and args[1]:
        create_module(args[1])
    elif args[0] == "db":
        try:
            autoload_models()
            if args[1] == "migrate":
                subprocess.run(["flask", "db", "migrate"])
            elif args[1] == "upgrade":
                subprocess.run(["flask", "db", "upgrade"])
            elif args[1] == "init":
                subprocess.run(["flask", "db", "init"])
        except IndexError as e:
            print("db requires more options")
            raise e
    else:
        print("Command not recognised")


if __name__ == "__main__":
    process()
