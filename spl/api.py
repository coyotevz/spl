# -*- coding: utf-8 -*-

from flask.ext.restless import APIManager

from spl.models import db, Supplier


def configure_api(app):
    manager = APIManager(app, flask_sqlalchemy_db=db)

    exclude = ['documents', 'orders', 'supplier_contacts']

    manager.create_api(Supplier, collection_name='suppliers',
                       exclude_columns=exclude)
