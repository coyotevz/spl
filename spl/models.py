# -*- coding: utf-8 -*-

from flask.ext.mongokit import MongoKit, Document

db = MongoKit()


def configure_db(app):
    db.init_app(app)

@db.register
class Supplier(Document):
    __collection__ = 'supplier'
    use_dot_notation = True

    FREIGHT_SUPPLIER = u'FREIGHT_SUPPLIER'
    FREIGHT_CUSTOMER = u'FREIGHT_CUSTOMER'

    _freight_types = {
        FREIGHT_SUPPLIER: u'Flete de proveedor',
        FREIGHT_CUSTOMER: u'Flete de cliente',
    }

    structure = {
        'name': unicode,
        'cuit': unicode,
        'iibb': unicode,
        'phone': unicode,
        'fax': unicode,
        'email': unicode,
        'web': unicode,
        'address': unicode,
        'zip_code': unicode,
        'term': int,
        'account_number': unicode,
        'freight_type': unicode, # TODO: use the right type
    }
    required_fields = ['name']
    indexes = [{'fields': ['name']}]
