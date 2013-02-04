/*
 * Prevent :hover on parent
 */

(function($, undefined) {
  "use strict"; // jshint ;_;

  $('.nav-header div.caret-toggle').hover(
    function() {
      $(this).parent().addClass("no-hover");
    },
    function() {
      $(this).parent().removeClass("no-hover");
    }
  );

})(window.jQuery);
