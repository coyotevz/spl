define([
  'models/base/model'
], function(Model) {
  "use strict";

  var Navigation = Model.extend({
    defaults: {
      current: '',
      items: [
        {
          name: 'invoices',
          title: 'Facturas',
          action: 'Nueva Factura',
        },
        {
          name: 'orders',
          title: 'Pedidos',
          action: 'Nuevo Pedido',
        },
        {
          name: 'suppliers',
          href: '#/suppliers',
          title: 'Proveedores',
          action: 'Nuevo Proveedor',
        },
        {
          name: 'contacts',
          href: '#/contacts',
          title: 'Contactos',
          action: 'Nuevo Contacto',
        }
      ]
    }
  });

  return Navigation;
});
// vim:sw=2
