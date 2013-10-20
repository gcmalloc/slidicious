#!/usr/bin/env python
import subprocess
from flask.ext.script import Manager

from src.app import app

manager = Manager(app)

@manager.command
def test():
    """test the webapplication"""
    import nose
    nose.runmodule()

@manager.command
def bower_install(*options):
    bower_bin = app.config.get("BOWER_BIN", "bower")
    packages = app.config[ "BOWER_PACKAGE" ]
    bower_root = app.config.get("BOWER_ROOT", app.static_folder)
    proc = subprocess.Popen(
    [bower_bin, 'install'] + list(options) + list(packages),
    cwd=bower_root,
    )
    proc.wait()

if __name__ == "__main__":
    manager.run()
