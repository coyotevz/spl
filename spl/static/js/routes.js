define(function() {
  "use strict";

  /* The routes for the appication. This module returns a function.
   * `match` is match method of the Router
   */
  var routes = function(match) {
    match('', 'dashboard#index');
    match('dashboard', 'dashboard#index');
    match('suppliers', 'suppliers#index');
    match('contacts', 'contacts#index');
    match('contacts/:id/edit', 'contacts#edit');
  };

  return routes;
});

// vim:sw=2
