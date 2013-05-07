define([
  'chaplin',
  'models/sidebar',
  'views/sidebar_view',
], function(Chaplin, Sidebar, SidebarView) {
  "use strict";

  var SidebarController = Chaplin.Controller.extend({

    title: 'Sidebar',

    initialize: function() {
      SidebarController.__super__.initialize(this, arguments);
      this.model = new Sidebar();
      this.view = new SidebarView({ model: this.model });
      this.subscribeEvent('sidebar:change', function(current) {
        this.model.set({'current': current});
      })
    }

  });

  return SidebarController;
});
// vim:sw=2
