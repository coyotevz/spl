define([
  'jquery',
  'underscore',
  'backbone',
  'models/supplier',
  'text!templates/supplier_row.html'
], function($, _, Backbone, Supplier, template) {

  var SupplierRow = Backbone.View.extend({

    tagName: 'tr',
    template: _.template(template),
    events: {
      'click td': 'open',
      'change [type=checkbox]': 'select'
    },

    open: function(e) {
    },

    select: function(e) {
    },

    render: function() {
    }

  });

  return SupplierRow;

});
