require.config({
  baseUrl: "/static/js/vendor",
  shim: {
    'vendor/underscore': {
      exports: '_'
    },
    'vendor/backbone': {
      deps: ['vendor/underscore', 'jquery'],
      exports: 'Backbone'
    }
  }
});

require([
  "jquery",
  "underscore",
  "backbone",
], function($, _, Backbone) {
});
