#!/usr/bin/env python
import subprocess
from flask.ext.script import Manager

from src.app import app

app.debug = True
manager = Manager(app)


@manager.command
def test():
    """test the webapplication"""
    import nose
    nose.runmodule()

if __name__ == "__main__":
    manager.run()
