define([
  'underscore',
  'chaplin'
], function(_, Chaplin) {
  "use strict";

  var Model = Chaplin.Model.extend(_({
    idAttribute: '_id',

    fetch: function(options) {
      this.beginSync();
      var options = options ? _.clone(options) : {};
      var success = options.success;
      options.success = _.bind(function() {
        var args = _.values(arguments);
        if (success) success.apply(null, args);
        this.finishSync();
      }, this);
      Model.__super__.fetch.call(this, options);
    }
  }).extend(Chaplin.SyncMachine));

  return Model;
});
// vim:sw=2
