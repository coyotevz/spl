define([
  'chaplin',
  'models/navigation',
  'views/navigation_view',
], function(Chaplin, Navigation, NavigationView) {
  "use strict";

  var NavigationController = Chaplin.Controller.extend({

    title: 'Navigation',

    initialize: function() {
      NavigationController.__super__.initialize(this, arguments);
      this.model = new Navigation();
      this.view = new NavigationView({ model: this.model });
      this.subscribeEvent('navigation:change', function(current) {
        this.model.set({'current': current});
      })
    }

  });

  return NavigationController;
});
// vim:sw=2
