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
    'backbone':   'vendor/backbone-1.0.0',
    'chaplin':    'vendor/chaplin-0.9.0',
    'nunjucks':   'vendor/nunjucks-dev',
  },

  // For not AMD-capable per default, declare dependencies
  shim: {
    'underscore': {
      exports: '_'
    },
    'backbone': {
      deps: ['json', 'jquery', 'underscore'],
      exports: 'Backbone'
    },
    'nunjucks': {
      exports: 'nunjucks'
    },
  }

  // For easier development, disable broser caching
  // Of course, this sould be remove in a production environment
  ,urlArgs: 'ver=' + (new Date()).getTime()
});

// Bootsrap the application
require(['application'], function(Application) {
  var app = new Application();
  app.initialize();
});
