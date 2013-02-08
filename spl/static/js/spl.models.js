/*
 * SPL models definitions
 */

(function($, undefined) {

  "use strict"; // jshint ;_;

  var Supplier, Suppliers, SupplierRow, SuppliersListView,
      SupplierControls, AppView;

  _.templateSettings = {
    evaluate    : /\[%([\s\S]+?)%\]/g,
    interpolate : /\[%=([\s\S]+?)%\]/g,
    escape      : /\[%-([\s\S]+?)%\]/g
  }

  /* supplier model */
  Supplier = Backbone.Model.extend({
    idAttribute: "_id",
    collection: Suppliers
  });

  Backbone.PaginatedCollection = Backbone.Collection.extend({
    parse: function(resp, options) {
      this.page = resp.page;
      this.num_pages = resp.num_pages;
      this.num_results = resp.num_results;
      return resp.objects;
    },
  });

  /* suppliers collection */
  Suppliers = Backbone.PaginatedCollection.extend({
    model: Supplier,
    url: '/api/suppliers/',
    comparator: function(d) {
      return d.get('name') && d.get('name').toLowerCase();
    }
  });

  SupplierRow = Backbone.View.extend({
    tagName: 'tr',
    events: {
      'click td': 'open',
      'change [type=checkbox]': 'checked',
    },
    template: _.template($('#supplier-row-template').html()),
    initialize: function() {
      _.bindAll(this, 'open', 'checked', 'remove', 'render');
    },
    open: function(e) {
      if ($(e.target).is('[type=checkbox]')) return;
    },
    checked: function() {
      this.$el.toggleClass('selected', this.$('[type=checkbox]').is(':checked'));
    },
    remove: function() {
    },
    render: function() {
      this.$el.html(this.template({
        id: this.model.id,
        name: this.model.get('name'),
        email: this.model.get('email'),
        phone: this.model.get('phone')
      }));
      return this;
    }
  });

  /* Suppliers list view */
  SuppliersListView = Backbone.View.extend({
    el: $('table tbody'),
    collection: Suppliers,

    events: {
    },

    initialize: function() {
      _.bindAll(this, 'render');
      this.collection.bind('reset', this.render);
    },

    addSupplier: function(supplier) {
      supplier.rowView = new SupplierRow({model: supplier});
      this.$el.append(supplier.rowView.render().el);
    },

    render: function(suppliers) {
      var self = this;
      console.log(suppliers);
      suppliers.each(function(supplier) {
        self.addSupplier(supplier);
      });
    }

  });


  AppView = Backbone.View.extend({
    initialize: function() {
      this.supplier_list = new SuppliersListView;
    }
  });

  var appView = new AppView();
  window.appView = appView;
  window.Supplier = Supplier;
  window.Suppliers = Suppliers;
  window.SupplierRow = SupplierRow;
  window.SuppliersListView = SuppliersListView;

})(window.jQuery);
// vim:sw=2
