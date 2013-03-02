define([
  'jquery',
  'underscore',
  'chaplin'
], function($, _, Chaplin) {
  "use strict";

  var Layout = Chaplin.Layout.extend({

    title: 'SPL Application',

    initialize: function(options) {
      options = _.extend(options, {
         titleTemplate: _.template("[%= subtitle %] – [%= title %]"),
      });
    Layout.__super__.initialize(this, arguments);
      this.subscribeEvent('startupController', this.removeFallbackContent);
    },

    removeFallbackContent: function(opts) {
      opts.controller.adjustTitle(opts.controller.title);
      $('.accesible-fallback').remove();
      this.unsubscribeEvent('startupController', this.removeFallbackContent);
    }

  });

  return Layout;
});
// vim:sw=2
