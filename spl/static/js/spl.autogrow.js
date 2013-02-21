/*
 * AutoGrow input resizer
 * Based on: https://github.com/rkivalin/jquery-autogrow
 */

(function($, undefined) {

  "use strict"; // jshint ;_;

  var inherit = ['font', 'font-family', 'font-weight', 'font-size', 'letter-spacing'];

  var testSubject;

  var getTestSubject = function() {
    if (!testSubject)
      testSubject = $('<span id="autogrow-tester"/>').appendTo('body');
    return testSubject;
  };

  $.fn.autogrow = function(options) {
    return this.each(function() {
      var check, input, styles, prop;

      input = $(this);
      input._originalWidth = input.width();
      styles = {
        position: 'absolute',
        top: -99999,
        left: -99999,
        width: 'auto',
        visibility: 'hidden'
      };
      $.each(inherit, function(i, prop) {
        styles[prop] = input.css(prop);
      });
      
      check = function() {
        var ts = getTestSubject();
        ts.css(styles);
        ts.html(input.val().replace(/ /g, '&nbsp;'));
        if (!input.val()) {
          return input.width(input._originalWidth);
        } else {
          return input.width(ts.width() + 3);
        }
      };

      input.on('input.autogrow', check);

    });
  };

})(window.jQuery);
// vim:sw=2
