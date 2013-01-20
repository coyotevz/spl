# -*- coding: utf-8 -*-

from datetime import datetime
from flask.ext.mongokit import MongoKit, Document

db = MongoKit()


def configure_db(app):
    db.init_app(app)


class Model(Document):
    use_dot_notation = True
    use_schemaless = True
    use_autorefs = True


@db.register
class Contact(Model):
    __collection__ = 'contact'

    structure = {
        'name': basestring,
        'phone': basestring,
        'email': basestring,
    }

    required_fields = ['name']


@db.register
class Supplier(Model):
    __collection__ = 'supplier'

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
        'notes': unicode,
        'created_at': datetime,

        'contacts': [{
            'contact': Contact,
            'role': unicode,
        }],
    }
    required_fields = ['name']
    indexes = [{'fields': ['name']}]
    default_values = {
        'created_at': datetime.now,
    }


class PurchaseDocument(Model):
    pass

class PurchaseOrder(Model):
    pass
