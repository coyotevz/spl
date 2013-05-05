define([
  'views/base/view',
  'text!templates/supplier_view.html'
], function(View, template) {
  "use strict";

  var SupplierView = View.extend({
    id: 'supplier',
    container: '#content',
    autoRender: false,
    template: template,

    listen: {
      'change model': 'render',
    },

  });

  return SupplierView;
});
// vim:sw=2
