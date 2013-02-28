define([
  'underscore',
  'chaplin',
  'templates/config'
], function(_, Chaplin) {
  "use strict";

  var View = Chaplin.View.extend({

    getTemplateFunction: function() {
      /* Template compilation
       * ~~~~~~~~~~~~~~~~~~~~
       *
       * We use underscore templates to render views.
       * The template is loaded with require.js and stored as string on
       * the view prototype. On rendering, it is compiled on the client-side.
       * The compiled template function replaces the string on the view
       * prototype.
       *
       * In the end we want to precompile the templates to JavaScript functions
       * on the server-side and just load the JavaScript code.
       */

      var template = this.template,
          templateFunc = null;

      if (typeof template === 'string') {
        templateFunc = _.template(template);
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
