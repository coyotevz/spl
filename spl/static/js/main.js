// Configure the AMD module loader
require.config({

  // Path where JavaScript root modules are located
  baseUrl: "/static/js",

  paths: {
    // Specify the paths of vendor libraries
    'json':       'vendor/json2',
    'jquery':     'vendor/jquery-1.9.1',
    'jquery-dotimeout': 'vendor/jquery.dotimeout-1.0',
    'moment':     'vendor/moment-2.0.0',
    'underscore': 'vendor/underscore-1.4.4',
    'backbone':   'vendor/backbone-0.9.10',
    'chaplin':    'vendor/chaplin-0.7.0',
    'text':       'vendor/text-2.0.5'
  },

  // For not AMD-capable per default, declare dependencies
  shim: {
    'underscore': {
      exports: '_'
    },
    'backbone': {
      deps: ['json', 'jquery', 'underscore'],
      exports: 'Backbone'
    }
  }

  // For easier development, disable broser caching
  // Of course, this sould be remove in a production environment
  ,urlArgs: 'ver=' + (new Date()).getTime()
});

// Bootsrap the application
require(['application'], function(Application) {
  var app = new Application();
  app.run();
});
