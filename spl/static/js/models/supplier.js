define([
  'models/base/model'
], function(Model) {

  var Supplier = Model.extend({

    urlRoot: '/api/suppliers/',

    defaults: {
      phone: '',
      email: ''
    },

  });

  return Supplier;

});
// vim:sw=2
