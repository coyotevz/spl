define([
  'views/base/collection_view',
  'views/supplier_view'
], function(CollectionView, SupplierView) {
  "use strict";

  var SuppliersCollectionView = CollectionView.extend({
    className: 'suppliers',
    itemView: SupplierView
  });

  return SuppliersCollectionView;
});
