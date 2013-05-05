define([
  'views/base/view',
  'ui/dropdown'
], function(View) {
  "use strict";

  var NavigationView = View.extend({
    template: 'navigation.html',
    className: 'title dropdown',
    container: 'aside header',
    autoRender: false,

    initialize: function() {
      NavigationView.__super__.initialize.apply(this, arguments);
      this.listenTo(this.model, 'change', this.render);
    },

    getTemplateData: function() {
      var data = this.model.getAttributes();
      data.current_title = 'NaN';
      _.each(data.items, function(nav) {
        if (data.current == nav.name) data.current_title = nav.title;
      });
      return data;
    }
  });

  return NavigationView;
});

// vim:sw=2
