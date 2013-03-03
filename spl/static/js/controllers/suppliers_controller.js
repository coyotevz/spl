define([
  'chaplin',
  'models/supplier',
  'views/supplier_view',
  'models/suppliers',
  'views/suppliers_view'
], function(Chaplin, Supplier, SupplierView, Suppliers, SuppliersView) {
  "use strict";

  var SuppliersController = Chaplin.Controller.extend({

    title: 'Suppliers',

    initialize: function() {
      SuppliersController.__super__.initialize.apply(this, arguments);
      this.publishEvent('navigation:change', 'suppliers');
    },

    historyURL: function(params) {
      if (params.id) {
        return "suppliers/" + params.id;
      } else {
        return '';
      }
    },

    index: function(params) {
      this.suppliers = new Suppliers();
      this.view = new SuppliersView({
        collection: this.suppliers
      });
    },

    show: function(params) {
      this.supplier = new Supplier({ _id: params.id }, { loadDetails: true });
      this.view = new SupplierView({ model: this.supplier });
    }
  });

  return SuppliersController;

});

// vim:sw=2
