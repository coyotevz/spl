define([
  'chaplin',
  'views/layout',
  'routes'
], function(Chaplin, Layout, routes) {
  'use strict';

  var Application = Chaplin.Application.extend({

    title: 'SPL',

    initialize: function() {
      console.log("Application initialization...");
      this.initDispatcher();
      this.initLayout();
      this.initMediator();
      this.initControllers();
      this.initRouter(routes);

      // Freeze the application instance to prevent further changes
      if (Object.freeze) Object.freeze(this);
    },

    initLayout: function() {
      this.layout = new Layout({title: this.title});
    },

    initControllers: function() {
    },

    initMediator: function() {
      // Seal the mediator
      Chaplin.mediator.seal();
    }
  });

  return Application;
});
// vim: sw=2
