define([
  'models/base/model'
], function(Model) {
  "use strict";

  var Supplier = Model.extend({

    urlRoot: '/api/suppliers/',

    defaults: {
      phone: '',
      email: ''
    },

    initialize: function(attributes, options) {
      Supplier.__super__.initialize.apply(this, arguments);
      if (options && options.loadDetails) {
        this.fetch();
      }
    }
  });

  return Supplier;

});
// vim:sw=2
