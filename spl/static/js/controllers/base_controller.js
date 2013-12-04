define([
  'chaplin',
  'models/sidebar',
  'views/sidebar_view',
  'views/toolbar_view',
], function(Chaplin, Sidebar, SidebarView, ToolbarView) {
  "use strict";

  var BaseController = Chaplin.Controller.extend({

    beforeAction: function() {
      console.log('BaseController#beforeAction');
      this.compose('sidebar', SidebarView, { model: new Sidebar() });
      this.compose('toolbar', ToolbarView, {});
    }

  });

  return BaseController;
});
