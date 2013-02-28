define([
  'chaplin'
], function(Chaplin) {
  "use strict";

  var SuppliersController = Chaplin.Controller.extend({

    index: function(params) {
      console.log("supplier#index:", params);
    },

    new: function(params) {
      console.log("suppliers#new:", params);
    },

    show: function(params) {
      console.log("suppliers#show:", params);
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
