#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy import Integer, ForeignKey, Text, Date, Numeric, Boolean, String, Float, Unicode
from sqlalchemy.orm import mapper, sessionmaker, relationship, backref

metadata = MetaData()

comentarios_table = Table('comentarios', metadata,
    Column('id_coment_proveedor', Integer, primary_key=True, autoincrement=False),
    Column('comentario', Text),

    mysql_engine='InnoDB',
    mysql_charset='latin1',
)

class Comentario(object):
    pass

mapper(Comentario, comentarios_table)

cuentas_banco_table = Table('cuentas_banco', metadata,
    Column('id_proveedor', Integer, primary_key=True, autoincrement=False),
    Column('cuenta', String(300), default=None),

    mysql_engine='InnoDB',
    mysql_charset='latin1',
)

class CuentaBanco(object):
    pass

mapper(CuentaBanco, cuentas_banco_table)

facturas_table = Table('facturas', metadata,
    Column('id_proveedor', Integer, nullable=False),
    Column('descripcion', String(1000), default=None),
    Column('fecha_de_ingreso', Date, nullable=False),
    Column('fecha_de_emision', Date, nullable=False),
    Column('fecha_de_recepcion', Date, nullable=False),
    Column('fecha_de_vencimiento', Date, nullable=False),
    Column('estado_fiscal', Boolean, nullable=False),
    Column('monto', Float, default=None),
    Column('numero_factura', Integer, default=None),
    Column('tipo_Factura', String(60), default=None),
    Column('hay_coment', String(3), default=None),
    Column('interno', Integer, primary_key=True),
    Column('nota_credito', Float, default=None),
    Column('parcial', Float, default=None),
    Column('pendiente', Float, default=None),

    mysql_engine='InnoDB',
    mysql_charset='latin1',
    mysql_auto_increment='4832',
)

class Factura(object):

    def __repr__(self):
        return "<Factura('%d', '%d', '%d', '%s') de %s>" % (self.numero_factura, self.estado_fiscal, self.monto, self.fecha_de_emision, self.proveedor.nombre)

mapper(Factura, facturas_table)

relacion_factura_nota_table = Table('relacion_factura_nota', metadata,
    Column('id_proveedor', Integer, primary_key=True),
    Column('numero_factura', Integer, default=None, primary_key=True),
    Column('parcial', Float, default=None),
    Column('numero_nota_int', Integer, default=None),

    mysql_engine='InnoDB',
    mysql_charset='latin1',
)

notas_credito_table = Table('notas_credito', metadata,
    Column('id_proveedor', Integer, default=None),
    Column('descripcion', String(1500), default=None),
    Column('numero', Integer, default=None),
    Column('usado', Boolean, default=None),
    Column('fecha', Date, default=None),
    Column('monto', Float, default=None),
    Column('interno', Integer, primary_key=True),
    Column('disponible', Float, default=None),

    mysql_engine='InnoDB',
    mysql_auto_increment='69',
    mysql_charset='latin1',
)

class NotaCredito(object):
    pass

mapper(NotaCredito, notas_credito_table)


pedidos_table = Table('pedidos', metadata,
    Column('codigo', String(50), primary_key=True),
    Column('descripcion', String(500), default=None),
    Column('fecha_de_ingreso', Date, default=None),
    Column('cantidad', Integer, default=None),
    Column('id_proveedor', Integer, primary_key=True, autoincrement=False),
    Column('numero_pedido', Integer, primary_key=True, autoincrement=False),
    Column('cantidad_recibida', Integer, default=None),

    mysql_engine='InnoDB',
    mysql_charset='latin1',
)

class Pedido(object):

    def __repr__(self):
        return "<Pedido (%s|%s), c=%s, d=%s, q=%s de '%s'>" %\
               (self.numero_pedido, self.fecha_de_ingreso.isoformat(),
                self.codigo, self.descripcion, self.cantidad,
                self.proveedor.nombre)

mapper(Pedido, pedidos_table)

pedidos_sub_table = Table('pedidos_sub', metadata,
    Column('comentario', String(1000), default=None),
    Column('numero_pedido', Integer, primary_key=True),
    Column('medio_de_pedido', String(30), default=None),
    Column('id_proveedor', Integer, primary_key=True, autoincrement=False),
    Column('fecha_de_pedido', Date, default=None),
    Column('estado_de_pedido', String(100), nullable=False),
    Column('relizado', Integer, nullable=False),

    mysql_engine='InnoDB',
    mysql_charset='latin1',
)

class PedidoSub(object):
    pass

mapper(PedidoSub, pedidos_sub_table)


relacion_rubro_proveedor_table = Table('relacion_rubro_proveedor', metadata,
    Column('id_proveedor', Integer, ForeignKey('proveedor.id', onupdate='cascade', ondelete='cascade'), primary_key=True),
    Column('id_rubro', Integer, ForeignKey('rubros.id_rubro', onupdate='cascade', ondelete='cascade'), primary_key=True),

    mysql_engine='InnoDB',
    mysql_charset='latin1',
)

rubros_table = Table('rubros', metadata,
    Column('id_rubro', Integer, primary_key=True),
    Column('rubro', String(60), nullable=True),

    mysql_engine='InnoDB',
    mysql_charset='latin1',
    mysql_auto_increment='5',
)

class Rubro(object):
    pass

mapper(Rubro, rubros_table)


proveedor_table = Table('proveedor', metadata,
    Column('nombre', String(100), default=None),
    Column('telefono', String(150), default=None),
    Column('id', Integer, primary_key=True, autoincrement=False),
    Column('fecha_de_ingreso', Date, default=None),
    Column('nombre_contacto', String(150), default=None),
    Column('email', String(150), default=None),
    Column('telefono_contacto', String(150), default=None),
    Column('direccion', String(200), default=None),
    Column('email_contacto', String(150), default=None),
    Column('flete', String(60), default=None),
    Column('web', String(100), default=None),
    Column('fax', String(60), default=None),
    Column('codigo_postal', String(10), default=None),
    Column('plazo', Integer, default=None),
    Column('cuit', String(30), default=None),
    Column('numeroCuenta', String(50), default=None),
    Column('ingresosBrutos', String(50), default=None),

    mysql_engine='InnoDB',
    mysql_charset='latin1',
)

class Proveedor(object):

    def __repr__(self):
        return "<Proveedor(id=%d, '%s')>" % (self.id, self.nombre)

mapper(Proveedor, proveedor_table, properties={
    'facturas': relationship(Factura, backref='proveedor',
                             order_by=facturas_table.c.fecha_de_emision,
                             primaryjoin=facturas_table.c.id_proveedor==proveedor_table.c.id,
                             foreign_keys=[facturas_table.c.id_proveedor],
                             lazy='dynamic'),
    'pedidos': relationship(Pedido, backref='proveedor',
                            order_by=pedidos_table.c.fecha_de_ingreso,
                            primaryjoin=pedidos_table.c.id_proveedor==proveedor_table.c.id,
                            foreign_keys=[pedidos_table.c.id_proveedor],
                            lazy='dynamic'),
    'pedidos_sub': relationship(PedidoSub, backref='proveedor',
                                order_by=pedidos_sub_table.c.fecha_de_pedido,
                                primaryjoin=pedidos_sub_table.c.id_proveedor==proveedor_table.c.id,
                                foreign_keys=[pedidos_sub_table.c.id_proveedor],
                                lazy='dynamic'),
    'cuentas_banco': relationship(CuentaBanco, backref='proveedor',
                                  primaryjoin=cuentas_banco_table.c.id_proveedor==proveedor_table.c.id,
                                  foreign_keys=[cuentas_banco_table.c.id_proveedor],
                                  lazy='dynamic'),
    'comentarios': relationship(Comentario, backref='proveedor',
                                primaryjoin=comentarios_table.c.id_coment_proveedor==proveedor_table.c.id,
                                foreign_keys=[comentarios_table.c.id_coment_proveedor],
                                lazy='dynamic'),

    'rubros': relationship(Rubro,
                           backref=backref('proveedores', lazy='dynamic',
                                           passive_deletes=True,
                                           passive_updates=True),
                           secondary=relacion_rubro_proveedor_table,
                           lazy='dynamic',
                           passive_deletes=True, passive_updates=True)
})

# Session

def configure_session(url, debug=False):
    engine = create_engine(url, echo=debug)
    metadata.bind = engine
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata.create_all()
    return session


if __name__ == '__main__':
    session = configure_session('mysql://augusto@localhost/gp1')
