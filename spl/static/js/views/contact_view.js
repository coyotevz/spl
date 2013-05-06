define([
  'views/base/view',
], function(View) {
  "use strict";

  var ContactView = View.extend({
    id: 'contact',
    container: '#content',
    autoRender: false,
    template: 'contact_view.html',

    listen: {
      'change model': 'render',
    },

  });

  return ContactView;
});
// vim:sw=2
