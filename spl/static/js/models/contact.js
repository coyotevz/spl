define([
  'models/base/model'
], function(Model) {
  "use strict";

  var Contact = Model.extend({

    urlRoot: '/api/contacts/',

    defaults: {
      phone: '',
      email: ''
    },

    initialize: function(attributes, options) {
      Contact.__super__.initialize.apply(this, arguments);
      if (options && options.loadDetails) {
        this.fetch();
      }
    }
  });

  return Contact;

});
// vim:sw=2
