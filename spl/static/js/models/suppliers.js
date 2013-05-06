define([
  'models/base/paginated_collection',
  'models/supplier'
], function(PaginatedCollection, Supplier) {
  "use strict";

  var Suppliers = PaginatedCollection.extend({

    model: Supplier,
    url: '/api/suppliers/',

    initialize: function() {
      Suppliers.__super__.initialize.apply(this, arguments);
      this.fetch();
    },

    comparator: function(d) {
      return d.get('name') && d.get('name').toLowerCase();
    }

  });

  return Suppliers;

});
// vim:sw=2
