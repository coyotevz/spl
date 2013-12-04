define([
  'views/base/view',
  'ui/dropdown',
], function(View) {
  "use strict";

  var ToolbarView = View.extend({
    template: 'toolbar.html',
    el: 'section#main div.toolbar',
    //autoRender: false,

    initialize: function() {
      ToolbarView.__super__.initialize.apply(this, arguments);
      this.render();
      this.delegate('click', 'button[name=next-page]', this.nextPage);
      this.delegate('click', 'button[name=prev-page]', this.prevPage);
    },

    update: function() {
      console.log("Tollbar.update()");
    },

    getTemplateData: function() {
      return {}
    },

    nextPage: function(evt) {
      console.log("ToolbarView.nextPage()", evt);
    },

    prevPage: function() {
      console.log("ToolbarView.prevPage()", arguments);
    },

  });

  return ToolbarView;
});
