define([
  'jquery',
  'chaplin',
  'views/base/view',
  'text!templates/contact_row.html'
], function($, Chaplin, View, template) {
  "use strict";

  var ContactRowView = View.extend({
    
    template: template,
    tagName: 'tr',
    className: 'contact-row',
    selected: false,

    initialize: function() {
      ContactRowView.__super__.initialize(this, arguments);
      this.delegate('click', '.checkbox input[type=checkbox]', this.checked);
      this.delegate('click', 'td', this.open);
    },

    checked: function(evt) {
      this.selected = $(evt.target).is(':checked');
      this.$el.toggleClass('selected', this.selected);
      this.trigger('selected');
    },

    open: function(evt) {
      if ($(evt.target).is('.checkbox input[type=checkbox]')) return this.checked(evt);
      Chaplin.mediator.publish('!router:routeByName', 'contact', { id: this.model.id });
    }

  });

  return ContactRowView;
});
// vim:sw=2
