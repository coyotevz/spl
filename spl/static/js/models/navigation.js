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
        },
        {
          name: 'orders',
          title: 'Pedidos',
        },
        {
          name: 'suppliers',
          href: '#/suppliers',
          title: 'Proveedores'
        },
        {
          name: 'contacts',
          href: '#/contacts',
          title: 'Contactos'
        }
      ]
    }
  });

  return Navigation;
});
// vim:sw=2
