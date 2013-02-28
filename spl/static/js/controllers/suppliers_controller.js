define([
  'chaplin',
  'models/supplier',
  'views/supplier_view',
  'collections/suppliers',
  'views/suppliers_collection_view'
], function(Chaplin, Supplier, SupplierView, Suppliers, SuppliersCollectionView) {
  "use strict";

  var SuppliersController = Chaplin.Controller.extend({

    index: function(params) {
      console.log("supplier#index:", params);
      this.collection = Suppliers;
      this.view = new SuppliersCollectionView({ collection: this.collection });
      this.collection.fetch();
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
