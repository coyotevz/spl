define([
  'chaplin',
  'models/base/model'
], function(Chaplin, Model) {
  "use strict";

  var PaginatedCollection = Chaplin.Collection.extend({
    model: Model,

    parse: function(resp, options) {
      this.page = resp.page || 1;
      this.num_pages = resp.num_pages || 1;
      this.num_results = resp.num_results || 0;
      return resp.objects;
    }
  });

  return PaginatedCollection;

});
