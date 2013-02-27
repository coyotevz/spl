define([
  'chaplin',
], function(Chaplin) {

  var DashboardController = Chaplin.Controller.extend({

    initialize: function() {
      console.log("DashboardController.initialize()");
    },

    index: function(params) {
      console.log("dashboard#index:", params);
    }

  });

  console.log("loading DashboardController");
  return DashboardController;

});
// vim:sw=2
