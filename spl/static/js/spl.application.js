/*
 * SPL application code
 */

(function($, undefined) {

  $('#category-toggle').click(function() {
    $(this).toggleClass('open');
    $('.sub.category').toggle();
  });

  $('[rel=tooltip]').tooltip({
    delay: {show: 500},
    placement: 'bottom'
  });

})(window.jQuery);
