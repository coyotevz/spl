require([
  'backbone',
  'models/supplier'
], function(Backbone, Supplier) {

  var Suppliers = Backbone.Collection.extend({

    model: Supplier,

    url: '/api/suppliers/',

    comparator: function(d) {
      return d.get('name') && d.get('name').toLowerCase();
    }

  });

  // Returns a new Suppliers collection instance
  return new Suppliers();

});
