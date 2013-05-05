define([
  'underscore',
  'chaplin',
  'templates/env'
], function(_, Chaplin, env) {
  "use strict";

  var View = Chaplin.View.extend({

    getTemplateFunction: function() {
      /* Template compilation
       * ~~~~~~~~~~~~~~~~~~~~
       *
       * We use nunjucks templates to render views.
       * The templates is loaded with nunjucks.HttpLoader. On rendering, it is
       * compiled on the client-side.
       * The compiled template function replaces the string on the view
       * prototype.
       *
       * In the end we want to precompile the templates to JavaScript functions
       * on the server-side and just load the JavaScript code.
       */
      var template = this.template,
          templateFunc = null;

      if (typeof template === 'string') {
        templateFunc = env.getTemplate(template).render;
        this.constructor.prototype.template = templateFunc;
      } else {
        templateFunc = template;
      }

      return templateFunc;
    },
  });

  return View;
});
// vim:sw=2
