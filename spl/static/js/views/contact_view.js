define([
  'views/base/view',
  'text!templates/contact_view.html'
], function(View, template) {
  "use strict";

  var ContactView = View.extend({
    id: 'contact',
    container: '#content',
    autoRender: false,
    template: template,

    listen: {
      'change model': 'render',
    },

  });

  return ContactView;
});
// vim:sw=2
