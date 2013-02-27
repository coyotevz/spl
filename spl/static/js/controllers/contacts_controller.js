define([
  'chaplin'
], function(Chaplin) {
  "use strict";

  var ContactsController = Chaplin.Controller.extend({

    index: function(params) {
      console.log("contacts#index:", params);
    },

    edit: function(params) {
      console.log("contacts#edit:", params);
    }

  });

  console.log("loading ContactsController");
  return ContactsController;
});

// vim:sw=2
