# -*- coding: utf-8 -*-

"""
    spl.commands
    ~~~~~~~~~~~~

    :copyright: 2013 by Augusto Roccasalva
    :license: BSD
"""

from flask import current_app
from flask.ext.script import Manager, Shell, prompt_bool
from flask.ext.assets import ManageAssets

from spl import create_app
from spl.models import db

manager = Manager(create_app)
manager.add_command("assets", ManageAssets())

@manager.command
def dropdb():
    """Drops database"""
    if prompt_bool("Are you sure? You will lose all your data!"):
        if not db.connected:
            db.connect()
        db.connection.drop_database(current_app.config['MONGODB_DATABASE'])

def shell_make_context():
    from datetime import datetime
    from decimal import Decimal
    return dict(app=current_app, db=db, Decimal=Decimal, datetime=datetime)

manager.add_command("shell", Shell(make_context=shell_make_context))

def main():
    manager.run()
