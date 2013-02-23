define(['backbone'], function(Backbone) {
  var Application = Backbone.View.extend({

    initialize: function() {
      console.log("Application initialization...");
    },

    run: function() {
      console.log("Application running...");
    }
  });

  return Application;
});
// vim: sw=2
