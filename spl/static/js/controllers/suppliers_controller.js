define([
  'chaplin'
], function(Chaplin) {
  "use strict";

  var SuppliersController = Chaplin.Controller.extend({

    index: function(params) {
      console.log("supplier#index:", params);
    }

  });

  console.log("loading SuppliersController");
  return SuppliersController;
});

// vim:sw=2
