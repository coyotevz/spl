define([
  'jquery',
  './resize',
  './tooltip',
  './autogrow'
], function($) {
  "use strict";

  /* side view category */
  /* TODO: move to side view */
  $('#category-toggle').on('click', function() {
    $(this).toggleClass('open');
    $('.sub.category').toggle();
  });

  /* global tooltip plugin configuration */
  $('[rel=tooltip]').tooltip({
    delay: {show: 500},
    placement: 'bottom'
  });

  /* reset cursor position to 0 on focus out */
  /* TODO: move to base editor view */
  $('input').on('blur', function(e) {
    $(this).val($(this).val());
  });

  /* global autogrow plugin configuration */
  $('input.autogrow').autogrow();

  /* global voidable configuration */
  /* TODO: move to base editor view */
  $('input.voidable').on('input', function(e) {
    $(this).toggleClass('void', $(this).val() == '');
  }).each(function() {
    /* check current state of voidables */
    $(this).toggleClass('void', $(this).val() == '');
  });

});
// vim:sw=2
