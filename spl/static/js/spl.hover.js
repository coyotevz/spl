/*
 * Prevent :hover on parent
 */

(function($, undefined) {
  "use strict"; // jshint ;_;

  $('.nav-header div.caret').hover(
    function() {
      $(this).parent().addClass("no-hover");
    },
    function() {
      $(this).parent().removeClass("no-hover");
    }
  );

})(window.jQuery);
