/*
 * SPL Supplier model definitions
 */

(function($, undefined) {

  "use strict"; // jshint ;_;

  var Supplier, SuppliersCollection, Suppliers;
  var SupplierRow, SuppliersView;

  /* supplier model */
  Supplier = Backbone.Model.extend({
    idAttribute: "_id",
    collection: Suppliers,
    defaults: {
      phone: '',
      email: ''
    },
  });

  SuppliersCollection = SPL.PaginatedCollection.extend({
    model: Supplier, 
    url: '/api/suppliers/',

    comparator: function(d) {
      return d.get('name') && d.get('name').toLowerCase();
    }
  });

  /* collection instance */
  Suppliers = new SuppliersCollection();

  SupplierRow = Backbone.View.extend({
    tagName: 'tr',
    //template: _.template($('#supplier-row-template').html()),

    events: {
      'click td': 'open',
      'change [type=checkbox]': 'select'
    },

    initialize: function() {
      this.template = _.template($('#supplier-row-template').html());
    },

    open: function(e) {
      if ($(e.target).is('[type=checkbox]')) return;
      if (this.model.id) {
        window.location.href = "/suppliers/" + this.model.id + "/";
      } else {
        console.warning("this model dosn't have id attribute");
      }
    },

    select: function() {
      var checked = this.$('[type=checkbox]').is(':checked');
      this.$el.toggleClass('selected', checked);
      this.trigger('selected', checked);
    },

    render: function() {
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    }
  });

  /* suppliers view */
  SuppliersView = Backbone.View.extend({
    el: $('div#page'),
    collection: Suppliers,

    events: {
      'click #new-supplier': 'newSupplierView'
    },

    initialize: function() {
      _.bindAll(this, 'render', 'renderCollection', 'selectionChange');
      this.collection.on('reset', this.renderCollection);
      this.pager = new SPL.Pager({collection: this.collection});
      this.table = this.$('table tbody');
      this.toolbar = this.$('.toolbar');
    },

    // Re-rendering the app just means refreshing pager and statistics -- the
    // rest of the app doesn't change
    render: function() {
      this.pager.render();
    },

    // Re-rendering collection and then the rest
    renderCollection: function(suppliers) {
      this.table.find('tr').remove(':not(.hide)');
      var self = this;
      if (suppliers.length) {
        this.$('#empty-supplier-message').hide();
        suppliers.each(function(supplier) {
          self.addSupplier(supplier);
        });
      } else {
        this.$('#empty-supplier-message').show();
      }
      this.render();
    },

    addSupplier: function(supplier) {
      supplier.rowView = new SupplierRow({model: supplier});
      supplier.rowView.on('selected', this.selectionChange);
      this.table.append(supplier.rowView.render().el);
    },

    selectionChange: function() {
      /* this.render(); */
    },

    // TODO: move this to global app view
    newSupplierView: function() {
      window.location.href = "/suppliers/new/";
    }
  });

  window.Supplier = Supplier;
  window.Suppliers = Suppliers;
  window.SuppliersView = SuppliersView;

})(window.jQuery);
// vim:sw=2
