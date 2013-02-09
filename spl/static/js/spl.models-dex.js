/*
 * SPL models definitions
 */

(function($, undefined) {

  "use strict"; // jshint ;_;

  var Supplier, Suppliers, SuppliersCollection, SupplierRow, SuppliersListView,
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

  SupplierRow = Backbone.View.extend({
    tagName: 'tr',
    template: _.template($('#supplier-row-template').html()),

    events: {
      'click td': 'open',
      'change [type=checkbox]': 'select',
    },

    initialize: function() {
      _.bindAll(this, 'open', 'select', 'remove', 'render');
    },

    open: function(e) {
      if ($(e.target).is('[type=checkbox]')) return;
      console.log("TODO: go to supplier view");
    },

    select: function() {
      var checked = this.$('[type=checkbox]').is(':checked');
      this.$el.toggleClass('selected', checked);
      this.trigger('selected', checked);
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
    },
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
  SuppliersCollection = Backbone.PaginatedCollection.extend({
    model: Supplier,

    url: '/api/suppliers/',

    comparator: function(d) {
      return d.get('name') && d.get('name').toLowerCase();
    }

  });

  Suppliers = new SuppliersCollection;

  /* Suppliers list view */
  SuppliersListView = Backbone.View.extend({
    el: $('table tbody'),
    collection: Suppliers,

    events: {
    },

    initialize: function() {
      _.bindAll(this, 'render', 'selectionChange');
      this.collection.bind('reset', this.render);
    },

    addSupplier: function(supplier) {
      supplier.rowView = new SupplierRow({model: supplier});
      supplier.rowView.bind('selected', this.selectionChange);
      this.$el.append(supplier.rowView.render().el);
    },

    render: function(suppliers) {
      var self = this;
      suppliers.each(function(supplier) {
        self.addSupplier(supplier);
      });
    },

    selected: function() {
      return this.collection.filter(function(s) {
        return s.rowView.$el.hasClass('selected');
      });
    },

    unselected: function() {
      return this.collection.without.apply(this.collection, this.selected());
    },

    selectionChange: function() {
      console.log("selection changed to %s selected", this.selected().length);
    }

  });


  AppView = Backbone.View.extend({
    initialize: function() {
      this.list_view = new SuppliersListView();
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
