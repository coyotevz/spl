/*
 * strongly based on bootstrap-dropdown.js v2.2.2
 * Copyright 2012 Twitter, Inc.
 */

define(['jquery'], function($) {

  "use strict"; // jshint ;_;

  /* Dropdown class definition */

  var toggle = '[data-toggle=dropdown]',
      Dropdown;

  Dropdown = function(element) {
    var $el = $(element).on('click.dropdown.data-api', this.toggle);
    $('html').on('click.dropdown.data-api', function() {
      $el.parent().removeClass('open');
    });
  };

  Dropdown.prototype = {

    constructor: Dropdown,

    toggle: function(e) {
      var $this = $(this),
          $parent,
          isActive;

      if ($this.is('.disabled, :disabled')) return;

      $parent = getParent($this);
      isActive = $parent.hasClass('open');

      clearMenus();

      if (!isActive) {
        $parent.toggleClass('open');
      }
      $this.focus();

      return false;
    },

    keydown: function(e) {
      var $this,
          $items,
          $active,
          $parent,
          isActive,
          index;

      if (!/(38|40|27)/.test(e.keyCode)) return;

      $this = $(this);
      e.preventDefault();
      e.stopPropagation();

      if ($this.is('.disabled, :disabled')) return;
      $parent = getParent($this);
      isActive = $parent.hasClass('open');
      if (!isActive || (isActive && e.keyCode == 27)) {
        if (e.which == 27) $parent.find(toggle).focus();
        return $this.click();
      }
      $items = $('[role=menu] li:not(.divider):visible a', $parent);

      if (!$items.length) return;

      index = $items.index($items.filter(':focus'));
      if (e.keyCode == 38 && index > 0) index--;                    // up
      if (e.keyCode == 40 && index < $items.length - 1) index++;    // down
      if (!~index) index = 0;

      $items
        .eq(index)
        .focus();
    },
  };

  function clearMenus() {
    $(toggle).each(function() {
      getParent($(this)).removeClass('open');
    });
  }

  function getParent($this) {
    var selector = $this.attr('data-target'),
        $parent;

    if (!selector) {
      selector = $this.attr('href');
      selector = selector && /#/.test(selector) && selector.replace(/.*(?=#[^\s]*$)/, '');
    }

    $parent = selector && $(selector);
    if (!$parent || !$parent.length) $parent = $this.parent();

    return $parent;
  }


  /* Dropdown plugin definition */

  var old = $.fn.dropdown;

  $.fn.dropdown = function(option) {
    return this.each(function() {
      var $this = $(this),
          data = $this.data('dropdown');
      if (!data) $this.data('dropdown', (data = new Dropdown(this)));
      if (typeof option == 'string') data[option].call($this);
    });
  };

  $.fn.dropdown.Constructor = Dropdown;

  /* Dropdown no conflict */

  $.fn.dropdown.noConflict = function() {
    $.fn.dropdown = old;
    return this;
  };

  /* Apply to standard dropdown elements */

  $(document)
    .on('click.dropdown.data-api', clearMenus)
    .on('click.dropdown', '.dropdown form', function(e) { e.stopPropagation() })
    .on('click.dropdown.data-api', toggle, Dropdown.prototype.toggle)
    .on('keydown.dropdown.data-api', toggle + ', [role=menu]', Dropdown.prototype.keydown);

});
// vim:sw=2
