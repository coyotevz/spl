define([
  'chaplin',
  'views/toolbar_view',
], function(Chaplin, ToolbarView) {
  "use strict";

  var ToolbarController = Chaplin.Controller.extend({

    initialize: function() {
      ToolbarController.__super__.initialize.apply(this, arguments);
      this.view = new ToolbarView();
      this.subscribeEvent('toolbar:update', function() {
        console.log('emitted toolbar:update');
        this.view.update();
      });
    }

  });

  return ToolbarController;
});
