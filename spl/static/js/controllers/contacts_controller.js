define([
  //'chaplin',
  'controllers/base_controller',
  'models/contact',
  'views/contact_view',
  'models/contacts',
  'views/contacts_view'
], function(BaseController, Contact, ContactView, Contacts, ContactsView) {
  "use strict";

  var ContactsController = BaseController.extend({

    title: 'Contacts',

    initialize: function() {
      ContactsController.__super__.initialize.apply(this, arguments);
      this.publishEvent('sidebar:change', 'contacts');
    },

    index: function(params) {
      this.contacts = new Contacts();
      this.view = new ContactsView({
        collection: this.contacts
      });
    },

    show: function(params) {
      this.contact = new Contact({ _id: params.id }, { loadDetails: true });
      this.view = new ContactView({ model: this.contact });
    }
  });

  return ContactsController;

});

// vim:sw=2
