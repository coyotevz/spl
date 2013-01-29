

(function($, undefined) {

  $('table tr .checkbox input').click(function() {
    $this = $(this);
    if ($this.is(':checked')) {
      $this.parents('tr').addClass('selected');
    } else {
      $this.parents('tr').removeClass('selected');
    }
  }).filter(':checked').parents('tr').addClass('selected');

})(window.jQuery);
