/*
 * SPL application code
 */

(function($, undefined) {

  $('#category-toggle').click(function() {
    $(this).toggleClass('open');
    $('.sub.category').toggle();
  });

})(window.jQuery);
