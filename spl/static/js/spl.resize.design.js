/*
 * resize routines
 */

(function($, undefined) {

  "use strict"; // jshint ;_;

  var resize = function() {
    var content_wrapper = $('#content_wrapper'),
        scroll_wrapper = $('#scroll_wrapper'),
        content_avl_width = $(window).width() - $('aside').width(),
        content_avl_height = $(window).height() - content_wrapper.position().top,
        edit_layout = $('.edit-layout', content_wrapper);

    content_wrapper.width(content_avl_width);
    content_wrapper.height(content_avl_height);
    scroll_wrapper.height(content_avl_height);

    if (edit_layout.length) {
      $('.edit-left-panel, .edit-right-panel', edit_layout)
          .outerWidth((edit_layout.width() - 1) / 2);
    }
  };

  $(window).resize(resize);
  $(window).focus(resize);
  resize();

})(window.jQuery);

// vim:sw=2
