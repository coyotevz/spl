/*
 * AutoGrow input resizer
 * Based on: https://github.com/rkivalin/jquery-autogrow
 */

(function($, undefined) {

  "use strict"; // jshint ;_;

  var inherit = ['font', 'font-family', 'font-weight', 'font-size', 'letter-spacing'];
  var test_subject;

  var get_test_subject = function() {
    if (!test_subject)
      test_subject = $('<span id="autogrow-tester"/>').appendTo('body');
    return test_subject;
  };

  $.fn.autogrow = function(options) {
    return this.each(function() {
      var check, set_css, input, test_subject, styles, prop;

      input = $(this);
      input._original_width = input.width();
      styles = {
        position: 'absolute',
        top: -99999,
        left: -99999,
        width: 'auto',
        visibility: 'hidden'
      };
      test_subject = get_test_subject();
      $.each(inherit, function(i, prop) {
        styles[prop] = input.css(prop);
      });

      set_css = function() {
        test_subject.css(styles);
      };
      
      check = function() {
        test_subject.html(input.val().replace(/ /g, '&nbsp;'));
        if (!input.val()) {
          return input.width(input._original_width);
        } else {
          return input.width(test_subject.width() + 3);
        }
      };

      input.on('input.autogrow', check);
      input.on('focus', set_css);

    });
  };

})(window.jQuery);
// vim:sw=2
