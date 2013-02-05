

(function($, undefined) {

  $('table tr .checkbox input').click(function() {
    $this = $(this);
    if ($this.is(':checked')) {
      $this.parents('tr').addClass('selected');
    } else {
      $this.parents('tr').removeClass('selected');
    }
  }).filter(':checked').parents('tr').addClass('selected');

  $('#select_all').click(function(e) {
    $this = $(this);
    e.stopPropagation();
    if ($this.is(':checked')) {
      $('table tr .checkbox input:not(:checked)').click();
    } else {
      $('table tr .checkbox input:checked').click();
    }
  });

})(window.jQuery);
// vim:sw=2
