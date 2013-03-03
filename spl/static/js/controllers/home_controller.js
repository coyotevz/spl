define([
  'chaplin',
], function(Chaplin) {
  "use strict";

  var HomeController = Chaplin.Controller.extend({

    initialize: function() {
      HomeController.__super__.initialize.apply(this, arguments);
      this.publishEvent('navigation:change', 'home');
    },

    index: function(params) {
      console.log("home#index:", params);
    }

  });

  return HomeController;

});
// vim:sw=2
