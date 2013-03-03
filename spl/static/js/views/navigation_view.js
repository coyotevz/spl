define([
  'views/base/view',
  'text!templates/navigation.html',
  'ui/dropdown'
], function(View, template) {
  "use strict";

  var NavigationView = View.extend({
    template: template,
    className: 'title dropdown',
    container: 'aside .sidenav',
    autoRender: false,

    initialize: function() {
      NavigationView.__super__.initialize.apply(this, arguments);
      this.listenTo(this.model, 'change', this.render);
    }
  });

  return NavigationView;
});

// vim:sw=2
