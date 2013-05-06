define([
  'views/base/collection_view',
  'views/supplier_row_view',
], function(CollectionView, SupplierRowView) {
  "use strict";

  var SuppliersView = CollectionView.extend({
    template: 'suppliers.html',
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
