# -*- coding: utf-8 -*-

"""
Migration script for old database.
"""

import sys
from datetime import date, datetime
from sqlalchemy import func

spl_path = '..'
today = date.today()

sys.path.append(spl_path)

# old app
from proveedores_table import (
    configure_session, Proveedor, Factura, PedidoSub, Pedido, Comentario,
    CuentaBanco,
)

# new app
from spl import create_app
from spl.models import db

# fancy
import ui

OLD_DB_URL = 'mysql://augusto@localhost/gp1'

def _(s):
    return unicode(s.decode('utf-8')) if s else None

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

def clean_dict(dct):
    return dict((k, v) for k, v in dct.iteritems() if (v != '' and v is not None))

def migrar_proveedores(s):
    tot = s.query(func.count(Proveedor.id)).scalar()
    bar = ui.PacmanProgress(u'migrando proveedores', tot, color='BOLD', sec_color='BLUE')
    c = 0
    for p in s.query(Proveedor):
        c += 1
        freight = db.Supplier.FREIGHT_SUPPLIER \
                    if p.flete.startswith(u'A Cargo del Proveedor')\
                    else db.Supplier.FREIGHT_CUSTOMER
        notes = s.query(Comentario).filter(Comentario.id_coment_proveedor==p.id).value('comentario')
        fecha_de_ingreso = check_year(p.fecha_de_ingreso)

        supplier = db.Supplier(clean_dict({
            'name': _(p.nombre),
            'cuit': _(p.cuit),
            'iibb': _(p.ingresosBrutos),
            'phone': _(p.telefono),
            'fax': _(p.fax),
            'email': _(p.email),
            'web': _(p.web),
            'address': _(p.direccion),
            'zip_code': _(p.codigo_postal),
            'std_payment_term': int(p.plazo),
            'account_number': _(p.numeroCuenta),
            'freight_type': freight,
            'created_at': datetime.fromordinal(fecha_de_ingreso.toordinal()),
            'notes': _(notes),
            'contacts': [],
        }))

        if p.nombre_contacto:
            contact = db.Contact(clean_dict({
                'name': _(p.nombre_contacto),
                'phone': _(p.telefono_contacto),
                'email': _(p.email_contacto),
            }))
            contact.save()
            supplier.contacts.append({'contact': contact})

        supplier.save()

        bar.update_state(c)
    bar.finish()

if __name__ == '__main__':
    session = configure_session(OLD_DB_URL)
    app = create_app()
    with app.app_context():
        #reenumerar_pedidos(session)
        migrar_proveedores(session)
