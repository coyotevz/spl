define([
  'underscore',
  'chaplin',
  'models/base/model'
], function(_, Chaplin, Model) {
  "use strict";

  var PaginatedCollection = Chaplin.Collection.extend(_({
    model: Model,

    parse: function(resp, options) {
      this.page = resp.page || 1;
      this.num_pages = resp.num_pages || 1;
      this.num_results = resp.num_results || 0;
      return resp.objects;
    },

    fetch: function(options) {
      this.beginSync();
      var options = options ? _.clone(options) : {};
      var success = options.success;
      options.success = _.bind(function() {
        var args = _.values(arguments);
        if (success) success.apply(null, args);
        this.finishSync();
      }, this);
      PaginatedCollection.__super__.fetch.call(this, options);
    }
  }).extend(Chaplin.SyncMachine));

  return PaginatedCollection;

});
// vim:sw=2
