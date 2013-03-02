define([
  'jquery',
  'views/base/view',
  'text!templates/supplier_row.html'
], function($, View, template) {
  "use strict";

  var SupplierRowView = View.extend({
    
    template: template,
    tagName: 'tr',
    className: 'supplier-row',
    selected: false,

    initialize: function() {
      SupplierRowView.__super__.initialize(this, arguments);
      this.delegate('click', '.checkbox input[type=checkbox]', this.checked);
      this.delegate('click', 'td', this.open);
    },

    checked: function(evt) {
      this.selected = $(evt.target).is(':checked');
      this.$el.toggleClass('selected', this.selected);
      this.trigger('selected');
    },

    open: function(evt) {
      if ($(evt.target).is('.checkbox input[type=checkbox]')) return this.checked(evt);
      console.log("open:", this.model);
    }

  });

  return SupplierRowView;
});
// vim:sw=2
