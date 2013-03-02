define([
  'chaplin',
  'models/suppliers',
  'views/suppliers_view'
], function(Chaplin, Suppliers, SuppliersView) {
  "use strict";

  var SuppliersController = Chaplin.Controller.extend({

    title: 'Suppliers',

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
      console.log("suppliers#show to implement");
    }
  });

  return SuppliersController;

});

// vim:sw=2
