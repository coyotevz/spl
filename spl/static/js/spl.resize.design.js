/*
 * resize routines
 */

(function($, undefined) {

  "use strict"; // jshint ;_;

  var resize = function() {
    var contentWrapper = $('#content_wrapper'),
        scrollWrapper = $('#scroll_wrapper'),
        contentAvlWidth = $(window).width() - $('aside').width(),
        contentAvlHeight = $(window).height() - contentWrapper.position().top,
        editLayout = $('.edit-layout', contentWrapper);

    contentWrapper.width(contentAvlWidth);
    contentWrapper.height(contentAvlHeight);
    scrollWrapper.height(contentAvlHeight);

    if (editLayout.length) {
      var panelWidth = (editLayout.width() - 1) / 2;
      var maxWidth = panelWidth - (102 + 29 + 17 + 10);
      $('.edit-left-panel, .edit-right-panel', editLayout)
          .outerWidth(panelWidth);
      $('.edit-row-title + .edit-row-value input', editLayout).css({
        'max-width': maxWidth
      });
    }
  };

  $(window).resize(resize);
  $(window).focus(resize);
  resize();

})(window.jQuery);

// vim:sw=2
