define([
  'views/base/view',
  'text!templates/supplier_row.html'
], function(View, template) {
  "use strict";

  var SupplierRowView = View.extend({
    
    template: template,
    tagName: 'tr',
    className: 'supplier-row'

  });

  return SupplierRowView;
});
// vim:sw=2
