require([
  'backbone',
], function(Backbone) {

  var Supplier = Backbone.Model.extend({

    idAttribute: '_id'

  });

  return Supplier;

});
