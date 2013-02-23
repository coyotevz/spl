define(['chaplin', 'spl/resize'], function(Chaplin) {
  var Application = Chaplin.Application.extend({

    title: 'SPL',

    initialize: function() {
      console.log("Application initialization...");
      this.initDispatcher();
      this.initLayout();
      this.initRouter();
    }
  });

  return Application;
});
// vim: sw=2
