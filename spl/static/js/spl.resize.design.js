/*
 * resize routines
 */

(function($, undefined) {

  "use strict"; // jshint ;_;

  var resize = function() {
    var table_avl_width = $(window).width() - $('aside').width() - 17,
        content_wrapper = $('#content_wrapper'),
        scroll_wrapper = $('#scroll_wrapper'),
        content_avl_height = $(window).height() - content_wrapper.position().top;

    content_wrapper.width(table_avl_width);
    content_wrapper.height(content_avl_height);
    scroll_wrapper.height(content_avl_height);
  };

  $(window).resize(resize);
  $(window).focus(resize);
  resize();

})(window.jQuery);

// vim:sw=2
