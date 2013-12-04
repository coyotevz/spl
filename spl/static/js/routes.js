define(function() {
  "use strict";

  /* The routes for the appication. This module returns a function.
   * `match` is match method of the Router
   */
  var routes = function(match) {
    match('', 'home#index', { name: 'index' });
//    match('dashboard', 'dashboard#index');

    /* suppliers controller */
    match('suppliers',            'suppliers#index', {name: 'suppliers'});
    match('suppliers/new',        'suppliers#new', {name: 'new_supplier'});
    match('suppliers/:id',        'suppliers#show', {name: 'supplier'});
//    match('suppliers/:id/edit',   'suppliers#edit');
//    match('suppliers/:id/delete', 'suppliers#delete');

    /* contacts controller */
    match('contacts',             'contacts#index', {name: 'contacts'});
//    match('contacts/new',         'contacts#new');
    match('contacts/:id',         'contacts#show', {name: 'contact'});
//    match('contacts/:id/edit',    'contacts#edit');
//    match('contacts/:id/delete',  'contacts#delete');
  };

  return routes;
});

// vim:sw=2
