# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template

from spl.models import db, Supplier, PurchaseDocument, PurchaseOrder

supplier = Blueprint('supplier', __name__)

@supplier.route('/')
def suppliers_list():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 25))
    suppliers = Supplier.query.order_by(Supplier.name)
    pagination = suppliers.paginate(page, per_page=per_page)
    return render_template('supplier_list.html', pagination=pagination)

@supplier.route('/<int:id>/')
def supplier_view(id):
    supplier = Supplier.query.get_or_404(id)
    return render_template('supplier_view.html', supplier=supplier)


@supplier.route('/orders/<int:id>/')
def supplier_order_view(id):
    order = PurchaseOrder.query.get_or_404(id)
    return render_template('supplier_order_view.html', order=order)


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
    return render_template('invoice_list.html', pagination=pagination, expired=expired, pending=pending, paid=paid, page=page, per_page=per_page)

@invoice.route('/<int:id>/')
def invoice_view(id):
    invoice = PurchaseDocument.query.get_or_404(id)
    return render_template('invoice_view.html', invoice=invoice)


def configure_views(app):
    app.register_blueprint(supplier, url_prefix='/suppliers')
    app.register_blueprint(invoice, url_prefix='/invoices')
