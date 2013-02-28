define([
  'views/base/view',
  'text!templates/supplier_view.html'
], function(View, template) {
  "use strict";

  var SupplierView = View.extend({
    // Automatically render after initialize
    autoRender: true,

    tagName: 'p',
    className: 'test-name',

    // Automatically append to the DOM on render
    container: '#content',

    /* Save the template string in a prototype property.
     * This is overwritten with the compiled template function.
     * In the end you might want to used precompiled templates.
     */
    template: template
  });

  return SupplierView;
});
// vim:sw=2
