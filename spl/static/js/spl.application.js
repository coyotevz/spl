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

  // Add a simple model to view to test it!
  var c = $('table tbody'),
      s = new Supplier({
              id: 'test',
              name: 'Augusto Roccasalva',
              email: 'augusto@rioplomo.com.ar',
              phone: 4251600}),
      sr = new SupplierRow({model: s});

  c.append(sr.$el.html(sr.template({
    id: s.get('id'),
    name: s.get('name'),
    email: s.get('email'),
    phone: s.get('phone')
  })));

})(window.jQuery);
