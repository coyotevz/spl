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

  $('input.autogrow').autogrow();

  $('input.voidable').on('input', function(e) {
    $(this).toggleClass('void', $(this).val() == '' ? true : false);
  }).each(function() {
    // check current state
    $(this).toggleClass('void', $(this).val() == '' ? true : false);
  });

})(window.jQuery);
// vim:sw=2
