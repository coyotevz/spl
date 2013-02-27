define(function() {
  "use strict";

  /* The routes for the appication. This module returns a function.
   * `match` is match method of the Router
   */
  var routes = function(match) {
    match('', 'main#index');
  };

  return routes;
});

// vim:sw=2
