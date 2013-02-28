define([
  'chaplin'
], function(Chaplin) {
  "use strict";

  var Model = Chaplin.Model.extend({
    idAttribute: '_id'
  });

  return Model;
});
