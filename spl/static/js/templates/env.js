define([
  'nunjucks',
  'text',
  'templates/templates',
], function(nunjucks, text) {
  "use strict";

  var env;

  /* Check if have precompiled templates else use HttpLoader */
  if (!nunjucks.env) {
    var RequireLoader = nunjucks.require('object').extend({
      init: function(baseURL, neverUpdate) {
        console.log("[nunjucks] Warning: only use RequireLoader in " +
                    "development. Otherwise precompile your templates.");
        this.baseURL = baseURL || '';
        this.neverUpdate = neverUpdate;
      },

      getSource: function(name) {
        var tmpl_query = 'text!' + this.baseURL + '/' + name;
        console.log(tmpl_query);
        var src = require([tmpl_query]);
        console.log(src);
        var _this = this;

        if (!src) {
          return null;
        }

        return { src: src,
                 path: name,
                 upToDate: function() { return _this.neverUpdate; }};
      },
    });
    env = new nunjucks.Environment(
      //new nunjucks.HttpLoader('/static/js/templates', true)
      new RequireLoader('templates', true)
    );
  } else {
    env = nunjucks.env;
  }

  return env;
});
