define([
  'chaplin',
  'models/supplier', 'views/supplier_view',
  'models/suppliers', 'views/suppliers_view',
  'views/supplier_edit_view'
], function(Chaplin,
            Supplier, SupplierView,
            Suppliers, SuppliersView,
            SupplierEditView) {
  "use strict";

  var SuppliersController = Chaplin.Controller.extend({

    title: 'Suppliers',

    initialize: function() {
      SuppliersController.__super__.initialize.apply(this, arguments);
      this.publishEvent('sidebar:change', 'suppliers');
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
    },

    'new': function(params) {
      console.log("#new");
      this.view = new SupplierEditView();
    },

    edit: function(params) {
      console.log("#edit");
      this.view = new SupplierEditView();
    },
  });

  return SuppliersController;

});

// vim:sw=2
