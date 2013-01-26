/*
 * Handle scroll events
 */

(function($, undefined) {

  "use strict"; // jshint ;_;

  $('#scroll_wrapper').scroll(function() {
    if ($('#scroll_wrapper').scrollTop() > 0) {
      $('section#main .toolbar').addClass('fixed');
    } else {
      $('section#main .toolbar').removeClass('fixed');
    }
  });

})(window.jQuery);
// vim: sw=2
