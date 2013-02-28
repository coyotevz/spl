define([
  'chaplin',
  'models/supplier',
  'views/supplier_view'
], function(Chaplin, Supplier, SupplierView) {
  "use strict";

  var SuppliersController = Chaplin.Controller.extend({

    index: function(params) {
      console.log("supplier#index:", params);
    },

    new: function(params) {
      console.log("suppliers#new:", params);
    },

    show: function(params) {
      this.model = new Supplier({ _id: params.id });
      this.view = new SupplierView({ model: this.model });
      this.model.fetch();
    },

    edit: function(params) {
      console.log("suppliers#edit:", params);
    },

    delete: function(params) {
      console.log("suppliers#delete:", params);
    }

  });

  return SuppliersController;

});

// vim:sw=2
