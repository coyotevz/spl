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

  // Reset caret position to 0 on focus out
  $('input').on('blur', function(e) {
    $(this).val($(this).val());
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
