define([
  'models/base/model'
], function(Model) {
  "use strict";

  var Navigation = Model.extend({
    defaults: {
      current: 'suppliers',
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
    },

    checkCurrent: function() {
      console.log('checking current');
    },

    initialize: function() {
      Navigation.__super__.initialize.apply(this, arguments);
      _.bindAll(this, 'checkCurrent');
      this.on('change:current', this.checkCurrent);
    }
  });

  return Navigation;
});
// vim:sw=2
