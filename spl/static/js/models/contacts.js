define([
  'models/base/paginated_collection',
  'models/contact'
], function(PaginatedCollection, Contact) {
  "use strict";

  var Contacts = PaginatedCollection.extend({

    model: Contact,
    url: '/api/contacts/',

    initialize: function() {
      Contacts.__super__.initialize.apply(this, arguments);
      this.fetch();
    },

    comparator: function(d) {
      return d.get('name') && d.get('name').toLowerCase();
    }

  });

  return Contacts;

});
// vim:sw=2
