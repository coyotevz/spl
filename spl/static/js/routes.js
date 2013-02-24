define(function() {
  'use strict';

  var routes = function(match) {
    match('', 'helloWorld#show');
  };

  return routes;
});
// vim: sw=2
