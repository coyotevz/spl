define([
  'views/base/collection_view',
  'views/contact_row_view',
], function(CollectionView, ContactRowView) {
  "use strict";

  var ContactsView = CollectionView.extend({
    template: 'contacts.html',
    tagName: 'table',
    id: 'contacts-list',
    className: 'list',

    container: '#content',
    listSelector: 'tbody',
    fallbackSelector: '.fallback',
    loadingSelector: '.loading',

    initItemView: function(item) {
      return new ContactRowView({ model: item });
    }
  });

  return ContactsView;
});
// vim:sw=2
