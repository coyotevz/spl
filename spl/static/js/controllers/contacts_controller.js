define([
  'chaplin'
], function(Chaplin) {
  "use strict";

  var ContactsController = Chaplin.Controller.extend({

    index: function(params) {
      console.log("contacts#index:", params);
    },

    new: function(params) {
      console.log("contacts#new:", params);
    },

    show: function(params) {
      console.log("contacts#view", params);
    },

    edit: function(params) {
      console.log("contacts#edit:", params);
    },

    delete: function(params) {
      console.log("contacts#delete", params);
    }

  });

  return ContactsController;

});

// vim:sw=2
