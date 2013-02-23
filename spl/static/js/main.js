// Configure the AMD module loader
require.config({

  // Path where JavaScript root modules are located
  baseUrl: "/static/js",

  // Specify the paths of vendor libraries
  paths: {
    'jquery': 'vendor/jquery',
    'underscore': 'vendor/underscore',
    'backbone': 'vendor/backbone',
    'chaplin': 'vendor/chaplin'
  },

  // For not AMD-capable per default, declare dependencies
  shim: {
    'underscore': {
      deps: ['jquery'],
      exports: '_'
    },
    'backbone': {
      deps: ['underscore'],
      exports: 'Backbone'
    }
  }

  // For easier development, disable broser caching
  // Of course, this sould be remove in a production environment
  // urlArgs: 'ver=' + (new Date()).getTime()
});

// Bootsrap the application
require(['application'], function(Application) {
  var app = new Application();
  app.run();
});
