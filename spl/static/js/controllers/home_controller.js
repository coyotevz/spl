define([
  'chaplin',
], function(Chaplin) {
  "use strict";

  var HomeController = Chaplin.Controller.extend({

    index: function(params) {
      console.log("home#index:", params);
    }

  });

  return HomeController;

});
// vim:sw=2
