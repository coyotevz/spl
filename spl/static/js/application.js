define([
  'backbone',
  'views/supplierrow',
  'ui/main'
], function(Backbone, SupplierRow) {
  'use strict';

  var Application = Backbone.Router.extend({

    routes: {
      '': 'index',
      'suppliers': 'showSuppliers',
      'contacts': 'showContacts',
    },

    initialize: function() {
      console.log("Application initialization...");
      this.sr = new SupplierRow();
    },

    run: function() {
      console.log("Application running...");
      Backbone.history.start();
    },

    index: function() {
      console.log("index method");
    },

    showSuppliers: function() {
      console.log("showSuppliers method");
    },

    showContacts: function() {
      console.log("showContacts method");
    }
  });

  return Application;
});
// vim: sw=2
