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
      if (this.collection.num_pages > 1) {
        this.$('.first').text(this.collection.first().get('name').split(' ')[0]);
        this.$('.last').text(this.collection.last().get('name').split(' ')[0]);
        this.$('[name=prev-page]').prop('disabled', this.collection.page <= 1);
        this.$('[name=next-page]').prop('disabled', this.collection.page >= this.collection.num_pages);
        this.$el.show();
      } else {
        this.$el.hide();
      }
      return this;
    },

    prevPage: function() {
      this.$('[rel=tooltip]').tooltip('hide');
      this.collection.fetch({ data: $.param({
        page: this.collection.page - 1
      })});
    },

    nextPage: function() {
      this.$('[rel=tooltip]').tooltip('hide');
      this.collection.fetch({ data: $.param({
        page: this.collection.page + 1
      })});
    }
  });

})(window.jQuery);
// vim:sw=2
