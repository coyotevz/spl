# -*- coding: utf-8 -*-

"""
Migration script for old database.
"""

from os import path
import sys
from datetime import date
from sqlalchemy import func, Table
spl_path = '..'
today = date.today()

sys.path.append(spl_path)
db_path = path.abspath(path.join(spl_path, 'development_data.db'))

# old app
from proveedores_table import (
    configure_session, Proveedor, Factura, PedidoSub, Pedido, Comentario,
    CuentaBanco,
)

# new app
from spl import create_app
from spl.models import (
    db, Supplier, Contact, PurchaseDocument,
    PurchaseOrder, PurchaseOrderItem,
    Bank, BankAccount,
)

# fancy
from ui import ProgressBar

# NOTE
# ~~~~
# PedidoSub --> PurchaseOrder
# Pedido    --> PurchaseOrderItem

OLD_DB_URL = 'mysql://augusto@localhost/gp1'

def _(s):
    return unicode(s.decode('utf-8'))

def _reenum_pedidos(s, number, pedidos_query, bar):
    n = number
    for pedido in pedidos_query:
        n += 1
        items_query = s.query(Pedido).filter(Pedido.numero_pedido==pedido.numero_pedido)\
                                     .filter(Pedido.id_proveedor==pedido.id_proveedor)
        items_count = items_query.update({'numero_pedido': n})
        bar.update_state(n-number)
        pedido.numero_pedido = n
        s.commit()


def reenumerar_pedidos(s):
    pedidos = s.query(PedidoSub).order_by(PedidoSub.fecha_de_pedido.asc(), PedidoSub.numero_pedido.asc())
    bar = ProgressBar(u'enumerando pedidos 1ra pasada', s.query(func.count(PedidoSub.numero_pedido)).scalar())
    _reenum_pedidos(s, 10000, pedidos, bar)
    bar.finish()
    pedidos = s.query(PedidoSub).order_by(PedidoSub.numero_pedido.asc())
    bar = ProgressBar(u'enumerando pedidos 2da pasada', s.query(func.count(PedidoSub.numero_pedido)).scalar())
    _reenum_pedidos(s, 0, pedidos, bar)
    bar.finish()


def check_year(date):
    if date.year < 2000:
        return date.replace(year=(2000+date.year))
    return date


po_status_map = {
    u'Pedido sin Pendientes': PurchaseOrder.STATUS_CLOSED,
    u'Articulos Pendientes': PurchaseOrder.STATUS_PARTIAL,
    u'Pendiente de Entrega': PurchaseOrder.STATUS_CONFIRMED,
    u'No Realizado': PurchaseOrder.STATUS_DRAFT
}

po_method_map = {
    u'Fax': PurchaseOrder.METHOD_FAX,
    u'Personalmente': PurchaseOrder.METHOD_PERSONALLY,
    u'e-mail': PurchaseOrder.METHOD_EMAIL
}

def migrar_pedido(s, p, supplier):
    fecha_de_pedido = check_year(p.fecha_de_pedido)
    po = PurchaseOrder(number=p.numero_pedido,
                       status=po_status_map[_(p.estado_de_pedido)],
                       notes=_(p.comentario),
                       creation_date=fecha_de_pedido,
                       order_method=po_method_map[_(p.medio_de_pedido)],
                       supplier=supplier)

    items = s.query(Pedido).filter(Pedido.id_proveedor==p.id_proveedor)\
                           .filter(Pedido.numero_pedido==p.numero_pedido)
    for item in items:
        poi = PurchaseOrderItem(sku=_(item.codigo),
                                description=_(item.descripcion),
                                quantity=item.cantidad,
                                received_quantity=item.cantidad_recibida,
                                order=po)
    db.session.add(po)

pd_type_map = {
    u'Factura A': PurchaseDocument.TYPE_FACTURA_A,
    u'Presupuesto': PurchaseDocument.TYPE_PRESUPUESTO,
}

def migrar_factura(s, f, supplier):
    doc_status = PurchaseDocument.STATUS_PENDING if not f.estado_fiscal else PurchaseDocument.STATUS_PAID
    if not f.estado_fiscal and f.fecha_de_vencimiento < today:
        doc_status = PurchaseDocument.STATUS_EXPIRED
    fecha_de_emision = check_year(f.fecha_de_emision)
    fecha_de_recepcion = check_year(f.fecha_de_recepcion)
    fecha_de_vencimiento = check_year(f.fecha_de_vencimiento)
    fecha_de_ingreso = check_year(f.fecha_de_ingreso)
    pd = PurchaseDocument(issue_date=fecha_de_emision,
                          receipt_date=fecha_de_recepcion,
                          expiration_date=fecha_de_vencimiento,
                          creation_date=fecha_de_ingreso,
                          amount=f.monto,
                          notes=_(f.descripcion) if f.hay_coment == 'Si' else None,
                          document_type=pd_type_map[_(f.tipo_Factura)],
                          document_ps=1,
                          document_number=f.numero_factura,
                          status=doc_status,
                          supplier=supplier)
    db.session.add(pd)

ba_type_map = {
    u'Cuenta Corriente en Pesos': BankAccount.TYPE_CC_PESOS,
    u'Caja de Ahorro en Pesos': BankAccount.TYPE_CA_PESOS,
}

def migrar_cuenta_banco(s, cb, supplier):
    bank_name, owner, acc_type, acc_number = [c.split(': ', 1)[-1] for c in cb.cuenta.split(' >  ')]
    b = db.session.query(Bank).filter(Bank.name==_(bank_name)).first()
    if not b:
        b = Bank(name=_(bank_name))
        db.session.add(b)
        db.session.commit()
    account = BankAccount(account_type=ba_type_map[_(acc_type)],
                          account_number=_(acc_number),
                          account_owner=_(owner),
                          bank=b,
                          supplier=supplier)
    db.session.add(account)

def migrar_proveedores(s):
    tot = s.query(func.count(Proveedor.id)).scalar()
    bar = ProgressBar(u'proveedores', tot)
    c = 0
    for p in s.query(Proveedor):
        c += 1
        freight = Supplier.FREIGHT_SUPPLIER \
                    if p.flete.startswith(u'A Cargo del Proveedor')\
                    else Supplier.FREIGHT_CUSTOMER
        notes = s.query(Comentario).filter(Comentario.id_coment_proveedor==p.id).value('comentario')
        fecha_de_ingreso = check_year(p.fecha_de_ingreso)
        supplier = Supplier(name=_(p.nombre),
                            cuit=_(p.cuit),
                            iibb=_(p.ingresosBrutos),
                            phone=_(p.telefono),
                            fax=_(p.fax),
                            web=_(p.web),
                            address=_(p.direccion),
                            zip_code=_(p.codigo_postal),
                            term=p.plazo,
                            account_number=_(p.numeroCuenta),
                            freight_type=freight,
                            created_at=fecha_de_ingreso,
                            notes=_(notes) if notes else None)

        if p.nombre_contacto:
            contact = Contact(name=_(p.nombre_contacto),
                              phone=_(p.telefono_contacto),
                              email=_(p.email_contacto))
            supplier.add_contact(contact)
        for factura in s.query(Factura).filter(Factura.id_proveedor==p.id):
            migrar_factura(s, factura, supplier)
        for pedido in s.query(PedidoSub).filter(PedidoSub.id_proveedor==p.id):
            migrar_pedido(s, pedido, supplier)
        for cuenta_banco in s.query(CuentaBanco).filter(CuentaBanco.id_proveedor==p.id):
            migrar_cuenta_banco(s, cuenta_banco, supplier)
        # TODO migrar notas de credito
        db.session.add(supplier)
        bar.update_state(c)
    db.session.commit()
    bar.finish()


class CONF(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % db_path

if __name__ == '__main__':
    session = configure_session(OLD_DB_URL)
    app = create_app(config=CONF)
    with app.app_context():
        #reenumerar_pedidos(session)
        migrar_proveedores(session)
