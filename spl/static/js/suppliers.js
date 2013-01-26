/*
 * supplier models
 */

(function($, undefined) {

  var Supplier, Suppliers;

  /* supplier model definition */
  Supplier = Backbone.Model.extend({
    idAttribute: "_id",
    defaults: {
    },

    collection: Suppliers,

    url_html: function() {
    },

    render: function(model) {
    },

    display: function() {
    }
  });

  /* suppliers collection definition */
  Suppliers = new Backbone.Collection();
  Suppliers.url = '/api/suppliers/';
  Suppliers.model = Supplier;
  Suppliers.parse = function(response) {
    return response.objects;
  };
  Suppliers.comparator = function(d) {
  };


  AppView = Backbone.View.extend({
    initialize: function() {
    }
  });

  var appView = new AppView();
  window.Suppliers = Suppliers;
  window.appView = appView;

})(window.jQuery);

// vim:sw=2
