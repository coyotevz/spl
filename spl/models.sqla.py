# -*- coding: utf-8 -*-

from sqlalchemy import func
from sqlalchemy.ext.associationproxy import association_proxy
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def configure_db(app):
    db.init_app(app)


class Supplier(db.Model):
    __tablename__ = 'supplier'

    FREIGHT_SUPPLIER = u'FREIGHT_SUPPLIER'
    FREIGHT_CUSTOMER = u'FREIGHT_CUSTOMER'

    _freight_types = {
        FREIGHT_SUPPLIER: u'Flete de proveedor',
        FREIGHT_CUSTOMER: u'Flete de cliente',
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    cuit = db.Column(db.UnicodeText(13))
    iibb = db.Column(db.Unicode)
    phone = db.Column(db.Unicode, default=None)
    fax = db.Column(db.Unicode, default=None)
    email = db.Column(db.Unicode, default=None)
    web = db.Column(db.Unicode, default=None)
    address = db.Column(db.Unicode, default=None)
    zip_code = db.Column(db.Unicode)
    term = db.Column(db.Integer) # due days
    account_number = db.Column(db.Unicode)
    freight_type = db.Column(db.Enum(*_freight_types.keys(),
                             name='freight_type'), default=FREIGHT_CUSTOMER)
    notes = db.Column(db.UnicodeText)
    created_at = db.Column(db.DateTime, default=func.now())

    supplier_contacts = db.relationship('SupplierContact',
                                        cascade='all,delete-orphan',
                                        backref='supplier', lazy='dynamic')
    contacts = association_proxy('supplier_contacts', 'contact')


    def add_contact(self, contact, role=None):
        self.supplier_contacts.append(SupplierContact(contact, role))

    @property
    def freight_str(self):
        return self._freight_types[self.freight_type]


class PurchaseDocument(db.Model):
    __tablename__ = 'document'

    TYPE_FACTURA_A   = u'TYPE_FACTURA_A'
    TYPE_PRESUPUESTO = u'TYPE_PRESUPUESTO'

    _doc_type = {
        TYPE_FACTURA_A: u'Factura A',
        TYPE_PRESUPUESTO: u'Presupuesto',
    }

    STATUS_PENDING = u'STATUS_PENDING'
    STATUS_EXPIRED = u'STATUS_EXPIRED'
    STATUS_PAID    = u'STATUS_PAID'

    _doc_status = {
        STATUS_PENDING: u'Pendiente',
        STATUS_EXPIRED: u'Vencida',
        STATUS_PAID: u'Pagada',
    }

    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.Enum(*_doc_type.keys(), name='doc_type'),
                              default=TYPE_FACTURA_A)
    document_ps = db.Column(db.Integer) # invoice point of sale part number
    document_number = db.Column(db.Integer)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    notes = db.Column(db.UnicodeText)
    creation_date = db.Column(db.DateTime)
    issue_date = db.Column(db.Date)
    receipt_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    status = db.Column(db.Enum(*_doc_status.keys(), name='doc_status'),
                       default=STATUS_PENDING)

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'),
                            nullable=False)
    supplier = db.relationship(Supplier, backref=db.backref('documents', lazy='dynamic'))

    @property
    def type_str(self):
        return self._doc_type[self.document_type]

    @property
    def status_str(self):
        return self._doc_status[self.status]

    @property
    def number_display(self):
        retval = "%08d" % self.document_number
        if self.document_ps:
            retval = "%04d-%s" % (self.document_ps, retval)
        return retval

class Bank(db.Model):
    __tablename__ = 'bank'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)


class BankAccount(db.Model):
    __tablename__ = 'bank_account'

    TYPE_CC_PESOS = u'TYPE_CC_PESOS'
    TYPE_CC_USD   = u'TYPE_CC_USD'
    TYPE_CA_PESOS = u'TYPE_CA_PESOS'
    TYPE_CA_USD   = u'TYPE_CA_USD'
    TYPE_UNIQUE   = u'TYPE_UNIQUE'

    _account_type = {
        TYPE_CC_PESOS: u'Cuenta Corriente en Pesos',
        TYPE_CC_USD: u'Cuenta Correinte en Dólares',
        TYPE_CA_PESOS: u'Caja de Ahorro en Pesos',
        TYPE_CA_USD: u'Caja de Ahorro en Dólares',
        TYPE_UNIQUE: u'Cuenta Única',
    }

    id = db.Column(db.Integer, primary_key=True)
    bank_branch = db.Column(db.Unicode)
    account_type = db.Column(db.Enum(*_account_type.keys(),
                             name='account_type'), default=TYPE_CC_PESOS)
    account_number = db.Column(db.Unicode)
    account_cbu = db.Column(db.Unicode)
    account_owner = db.Column(db.Unicode)

    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'))
    bank = db.relationship(Bank, backref='accounts')

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    supplier = db.relationship(Supplier, backref='bank_accounts')


class Contact(db.Model):
    __tablename__ = 'contact'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    phone = db.Column(db.Unicode)
    email = db.Column(db.Unicode)


class SupplierContact(db.Model):
    __tablname__ = 'supplier_contact'

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'),
                            primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'),
                           primary_key=True)
    role = db.Column(db.Unicode, default=None)

    # 'supplier' attribute is supplied bye Supplier.supplier_contacts
    # relationship

    contact = db.relationship(Contact, lazy='joined',
                              backref='supplier_contact')

    def __init__(self, contact, role=None):
        self.contact = contact
        self.role = role


class PurchaseOrder(db.Model):
    __tablename__ = 'order'

    STATUS_CANCELLED = u'STATUS_CANCELLED'
    STATUS_QUOTING   = u'STATUS_QUOTING'
    STATUS_PENDING   = u'STATUS_PENDING'
    STATUS_PARTIAL   = u'STATUS_PARTIAL'
    STATUS_CONFIRMED = u'STATUS_CONFIRMED'
    STATUS_CLOSED    = u'STATUS_CLOSED'
    STATUS_DRAFT     = u'STATUS_DRAFT'

    _order_status = {
        STATUS_CANCELLED: u'Cancelada',
        STATUS_QUOTING: u'Presupuestando',
        STATUS_PENDING: u'Pendiente',
        STATUS_PARTIAL: u'Parcial',
        STATUS_CONFIRMED: u'Confirmada',
        STATUS_CLOSED: u'Cerrada',
        STATUS_DRAFT: u'Borrador',
    }

    METHOD_EMAIL      = u'METHOD_EMAIL'
    METHOD_FAX        = u'METHOD_FAX'
    METHOD_PHONE      = u'METHOD_PHONE'
    METHOD_PERSONALLY = u'METHOD_PERSONALLY'

    _order_methods = {
        METHOD_EMAIL: u'Correo Electronico',
        METHOD_FAX: u'Fax',
        METHOD_PHONE: u'Telefónico',
        METHOD_PERSONALLY: u'Personalmente',
    }

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    status = db.Column(db.Enum(*_order_status.keys(), name='order_status'),
                       default=STATUS_DRAFT)
    notes = db.Column(db.UnicodeText)
    creation_date = db.Column(db.DateTime)
    order_method = db.Column(db.Enum(*_order_methods.keys(),
                             name='order_method'), default=METHOD_EMAIL)

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    supplier = db.relationship(Supplier, backref=db.backref('orders', lazy='dynamic'))

    @property
    def status_str(self):
        return self._order_status[self.status]

    @property
    def method_str(self):
        return self._order_method[self.order_method]


class PurchaseOrderItem(db.Model):
    __tablename__ = 'orderitem'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.Unicode(20)) # código de producto
    description = db.Column(db.Unicode(60))
    quantity = db.Column(db.Integer)
    received_quantity = db.Column(db.Integer, default=0)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order = db.relationship(PurchaseOrder, backref='items')
