define([
  'collections/base/paginated',
  'models/supplier'
], function(PaginatedCollection, Supplier) {
  "use strict";

  var Suppliers = PaginatedCollection.extend({

    model: Supplier,

    url: '/api/suppliers/',

    comparator: function(d) {
      return d.get('name') && d.get('name').toLowerCase();
    }

  });

  // Returns a new Suppliers collection instance
  return new Suppliers();

});
// vim:sw=2
