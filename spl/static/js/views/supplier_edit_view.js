define([
  'views/base/view',
], function(View) {
  "use strict";

  var SupplierEditView = View.extend({
    autoRender: false,
    template: 'supplier_edit.html',
  });

  return SupplierEditView;
});
// vim:sw=2
