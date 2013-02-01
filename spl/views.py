# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template

from spl.models import db
from spl.utils import Pagination

supplier = Blueprint('supplier', __name__)

@supplier.route('/')
def suppliers_list():
    suppliers = db.Supplier.find().sort('name')
    pagination = Pagination(suppliers, page=request.page,
                            per_page=request.per_page)
    return render_template('supplier/list.html', suppliers=suppliers, pagination=pagination)

@supplier.route('/<ObjectId:id>/')
def supplier_view(id):
    supplier = db.Supplier.get_or_404(id)
    return render_template('supplier/view.html', supplier=supplier)


@supplier.route('/orders/<int:id>/')
def supplier_order_view(id):
    order = PurchaseOrder.query.get_or_404(id)
    return render_template('supplier/order_view.html', order=order)


contact = Blueprint('contact', __name__)

@contact.route('/')
def contacts_list():
    contacts = db.Contact.find().sort('name')
    pagination = Pagination(contacts, page=request.page,
                            per_page=request.per_page)
    return render_template('contacts/list.html', pagination=pagination)


invoice = Blueprint('invoice', __name__)

@invoice.route('/')
def invoices_list():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 25))
    invoices = PurchaseDocument.query.order_by(PurchaseDocument.expiration_date.desc())
    expired = invoices.filter(PurchaseDocument.status==PurchaseDocument.STATUS_EXPIRED)
    pending = invoices.filter(PurchaseDocument.status==PurchaseDocument.STATUS_PENDING)
    paid = invoices.filter(PurchaseDocument.status==PurchaseDocument.STATUS_PAID)
    pagination = invoices.paginate(page, per_page=per_page)
    return render_template('invoice/list.html', pagination=pagination, expired=expired, pending=pending, paid=paid, page=page, per_page=per_page)

@invoice.route('/<int:id>/')
def invoice_view(id):
    invoice = PurchaseDocument.query.get_or_404(id)
    return render_template('invoice/view.html', invoice=invoice)


def configure_views(app):
    app.register_blueprint(supplier, url_prefix='/suppliers')
    app.register_blueprint(invoice, url_prefix='/invoices')
    app.register_blueprint(contact, url_prefix='/contacts')
