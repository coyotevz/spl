define([
  'chaplin',
  'views/layout',
  'controllers/navigation_controller',
  'routes',
  'ui/main'
], function(Chaplin, Layout, NavigationController, routes) {
  'use strict';

  var Application = Chaplin.Application.extend({

    title: 'SPL',

    initialize: function() {
      // call the parent constructor
      Application.__super__.initialize.apply(this, arguments);

      /* Initialize core components */
      this.initDispatcher();
      this.initLayout();
      this.initMediator();

      /* Application-specific scaffold */
      this.initControllers();

      /* Register all routes and start routing */
      this.initRouter(routes, { pushState: false, root: '/spl/' });
      /* You might pass Router/History options as the second parameter. */
      // this.initRouter(routers, { pushState: false, root: '/subdir/' });

      /* Freeze the application instance to prevent further changes */
      if (Object.freeze) Object.freeze(this);
    },

    initLayout: function() {
      this.layout = new Layout({ title: this.title });
    },

    /* Instantiate common controllers */
    initControllers: function() {
      /* This controllers are active during the whole application runtime.
       * You don't need to instantiate all controllers here, only special
       * controllers which do not to respond to routes. They may govern models
       * and views which are needed the whole time, for example header, footer
       * or navigation views.
       */
      new NavigationController();
    },

    /* Create additional mediator properties */
    initMediator: function() {
      // Create a user property
      Chaplin.mediator.user = null;
      // Add additional application-specific properties and methods
      // Seal the mediator
      Chaplin.mediator.seal();
    }

  });

  return Application;
});
// vim: sw=2
