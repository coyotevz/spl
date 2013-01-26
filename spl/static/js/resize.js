
/* Correct widths and height based on window size
*/

(function($, undefined) {

  "use strict"; // jshint ;_;

  var resize = function() {
    var height = $(window).height() - $('#header').height() - 5,
        width = $(window).outerWidth(),
        page_content = $('#page-content'),
        left_panel = $('#left'),
        right_panel = $('#right'),
        content = $('.content'),
        table_container = $('div.content > div');

    /* page_content.css({height: height + 'px'}); */
    page_content.outerHeight(height);
    right_panel.css({width: width - left_panel.width() + 'px'});
    content.height(page_content.outerHeight() - $('.toolbar-container').outerHeight() - 2);

    /* risize table columns */
    /* col0: 2px
     * col1: 30px
     */
    console.log('table_container.width():', table_container.width(), 'right_panel.width():', right_panel.width());
    var table_width = table_container.width() - 32 - 722;
    $('col.col2').width(Math.min(Math.floor(155 + table_width*0.18), 240));
    $('col.col3').width($('col.col2').width());
    $('col.col4').width(Math.min(Math.floor(183 + table_width*0.12), 240));
    $('col.col5').width(Math.max(Math.floor(table_container.width() - 32 - $('col.col2').width() - $('col.col3').width() - $('col.col4').width()), 229));

    $('table td div:not(.extra)').each(function(i, e) {
      var $e = $(e), gap;
      if ($e.next().is('.extra')) {
        gap = 14 + 23;
      } else {
        gap = 4;
      }
      $e.css({'max-width': $e.parent().width() - gap + 'px'});
    });

  };

  $(window).resize(resize);
  $(window).focus(resize);
  resize();

})(window.jQuery); 

// vim:sw=2
