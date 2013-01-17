# -*- coding: utf-8 -*-

"""
    spl.commands
    ~~~~~~~~~~~~

    :copyright: 2013 by Augusto Roccasalva
    :license: BSD
"""

from flask import current_app
from flask.ext.script import Manager, Shell, prompt_bool

from spl import create_app
from spl.models import db

manager = Manager(create_app)

@manager.command
def initdb():
    """Creates database tables"""
    db.create_all()

@manager.command
def dropdb():
    """Drops all database tables"""
    if prompt_bool("Are you sure? You will lose all your data!"):
        db.drop_all()

def shell_make_context():
    from datetime import datetime
    from decimal import Decimal
    return dict(app=current_app, db=db, Decimal=Decimal, datetime=datetime)

manager.add_command("shell", Shell(make_context=shell_make_context))

def main():
    manager.run()
