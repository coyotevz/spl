/*
 * Backbone-Nested
 */

(function($, _, Backbone) {

  "use strict";

  Backbone.NestedModel = Backbone.Model.extend({

    get: function(attsStrOrPath) {
    },

    has: function(attr) {
    },

    set: function(key, value, opts) {
    },

    clear: function(options) {
    },

    add: function(options) {
    },

    remove: function(attrStr, opts) {
    },

    toJSON: function() {
    },

    // privated
    _delayedTrigger: function() {
    },

    _delayedChange: function(atrStr, newVal) {
    },

    _runDelayedTriggers: function() {
    },

    _setAttr: function(newAttrs, attrPath, newValue, opts) {
    },


  }, {
    // class methods
    
    attrPath: function(attrStrOrPath) {
      var path;

      if (_.isString(attrStrOrPath)) {
        path = (attrStrOrPath === '') ? [''] : attrStrOrPath.match(/[^\.\[\]]/g);
        path = _.map(path, function(val);
            // TODO: contninue heres
      } else {
      }

      return path;
    },

    createAttrStr: function(attrPath) {
      var attrStr = attrPath[0];
      _.each(_.rest(attrPath), function(attr) {
        attrStr += _.isNumber(attr) ? ('[' + attr + ']') : ('.'  + attr);
      });

      return attrStr;
    },

    deepClone: function(obj) {
      return $.extend(true, {}, obj);
    },

    walkPath = function(obj, attrPath, callback, scope) {
    }

  });

})(jQuery, _, Backbone);
