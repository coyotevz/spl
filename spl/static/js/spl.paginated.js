/*
 * SPL paginated collections bases
 */

var SPL = SPL || {};

(function($, undefined) {

  _.templateSettings = {
    evaluate    : /\[%([\s\S]+?)%\]/g,
    interpolate : /\[%=([\s\S]+?)%\]/g,
    escape      : /\[%-([\s\S]+?)%\]/g
  };

  SPL.PaginatedCollection = Backbone.Collection.extend({
    parse: function(resp, options) {
      this.page = resp.page || 1;
      this.num_pages = resp.num_pages || 1;
      this.num_results = resp.num_results || 0;
      return resp.objects;
    },
  });

  SPL.Pager = Backbone.View.extend({
    el: $('.toolbar .pager'),

    events: {
      'click button[name=prev-page]': 'prevPage',
      'click button[name=next-page]': 'nextPage'
    },

    render: function() {
      this.$('.prev').text('Prev');
      this.$('.next').text('Next');
      /*
      this.$el.html(this.template({
        first: this.collection.first().get('name').split(' ')[0],
        last: this.collection.last().get('name').split(' ')[0],
      })); */
      return this;
    },

    prevPage: function() {
      console.log('go to prev page');
    },

    nextPage: function() {
      console.log('go to next page');
    }
  });

})(window.jQuery);
// vim:sw=2
