define([
  'views/base/view',
], function(View) {
  "use strict";

  var SupplierView = View.extend({
    id: 'supplier',
    container: '#content',
    autoRender: false,
    template: 'supplier_view.html',

    listen: {
      'change model': 'render',
    },

  });

  return SupplierView;
});
// vim:sw=2
