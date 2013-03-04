define([
  'views/base/collection_view',
  'views/supplier_row_view',
  'text!templates/suppliers.html'
], function(CollectionView, SupplierRowView, template) {
  "use strict";

  var SuppliersView = CollectionView.extend({
    template: template,
    tagName: 'table',
    id: 'suppliers-list',
    className: 'list',

    container: '#content',
    listSelector: 'tbody',
    fallbackSelector: '.fallback',
    loadingSelector: '.loading',

    initItemView: function(item) {
      return new SupplierRowView({ model: item });
    }
  });

  return SuppliersView;
});
// vim:sw=2
