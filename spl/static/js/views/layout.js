define([
  'jquery',
  'chaplin'
], function($, Chaplin) {
  "use strict";

  var Layout = Chaplin.Layout.extend({

    initialize: function() {
      Chaplin.Layout.prototype.initialize.apply(this, arguments);
      this.subscribeEvent('startupController', this.removeFallbackContent);
    },

    removeFallbackContent: function() {
      $('.accesible-fallback').remove();
      this.unsubscribeEvent('startupController', this.removeFallbackContent);
    }

  });

  return Layout;
});
// vim:sw=2
