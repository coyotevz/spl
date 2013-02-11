/*
 * AutoGrow input resizer
 * Based on: https://github.com/rkivalin/jquery-autogrow
 */

(function($, undefined) {

  "use strict"; // jshint ;_;

  var inherit = ['font', 'letter-spacing'];
  var test_subject;

  var get_test_subject = function() {
    if (test_subject) return test_subject;
    test_subject = $('<span id="autogrow-tester"/>').appendTo('body');
    return test_subject;
  };

  $.fn.autogrow = function(options) {
    return this.each(function() {
      var check, input, test_subject, styles, prop;

      input = $(this);
      test_subject = get_test_subject();
      for (prop in inherit) {
        styles[prop] = input.css(prop);
      }
      test_subject.css(styles);
    });
  };

})(window.jQuery);
// vim:sw=2
