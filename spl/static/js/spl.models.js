/*
 * SPL models definitions
 */

(function($, undefined) {

  "use strict"; // jshint ;_;

  var Supplier, Suppliers, SupplierRow, SuppliersList,
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

  /* suppliers collection */
  Suppliers = Backbone.Collection.extend({
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
      'click input[type=checkbox]': 'checked'
    },
    template: _.template($('#supplier-row-template').html()),
    initialize: function() {
      _.bindAll(this, 'open', 'checked', 'remove', 'render');
    },
    open: function() {
      window.console.log("open:", this);
    },
    checked: function() {
      var $checkbox = this.$('input[type=checkbox]');
      if ($checkbox.is(':checked')) {
        console.log("checkbox is checked");
        this.$el.addClass('selected');
      } else {
        console.log("checkbox is not checked");
        this.$el.removeClass('selected');
      }
      window.console.log("checked:", this, this.$el, this.$('input[type=checkbox]').is(':checked'));
      // handle checkbox
    },
    remove: function() {
      window.console.log("remove:", this);
    },
    render: function() {
      window.console.log("render:", this);
    }
  });

  window.Supplier = Supplier;
  window.SupplierRow = SupplierRow;

})(window.jQuery);
// vim:sw=2
