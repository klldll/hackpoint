;(function ($, window, undefined) {
  'use strict';

  var $doc = $(document),
      Modernizr = window.Modernizr;

  $(document).ready(function() {

    $.fn.placeholder                ? $('input, textarea').placeholder() : null;

    $('form#register_full').validate(
    '/validate/userprofileform/', {
      callback: function(data, form) {
        $(form).find('small.error').remove();
        $.each(data.errors, function(key, val)  {
          $('#' + key).removeClass('error');
          $('#' + key).after('');

          if (!data.valid) {
            $('#' + key).addClass('error');
            $('#' + key).after('<small class="error">' + val + '</small>');
          }
        });
      }
    });

    $('form#register_simple').validate(
    '/validate/registrationformuniqueemail/', {
      callback: function(data, form) {
        $(form).find('small.error').remove();
        $.each(data.errors, function(key, val)  {
          $('#' + key).removeClass('error');
          $('#' + key).after('');

          if (!data.valid) {
            $('#' + key).addClass('error');
            $('#' + key).after('<small class="error">' + val + '</small>');
          }
        });
      }
    });

    $('form#register_simple').on('form:validate', function (e) {
      $.ajax({
        url: '/accounts/register/',
        data: { email: $(this).find('input[id=id_email]').val()},
        type: 'POST',
        success : function(data, status) {
          $('#registerModal').foundation('reveal', 'open');
        }
      });
      $(this).find('small.error').remove();
      $(this).find('input').removeClass('error');
      $(this).hide();
      return false;
    });

    $('form#register_full').on('form:validate', function (e) {
      var data = {
        username: $(this).find('[id=id_username]').val(),
        email: $('#id_email').val(),
        user_skills: $(this).find('[id=id_user_skills]').val(),
        user_role: $(this).find('[id=id_user_role]').val(),
        has_idea: $(this).find('[id=id_has_idea]:checked').val() || false,
      };
      $.ajax({
        url: '/accounts/register/',
        data: data,
        type: 'POST',
        success : function(data, status) {
          $('#registerModal').foundation('reveal', 'open');
        }
      });
      $(this).find('small.error').remove();
      $(this).find('input').removeClass('error');
      $(this).remove();
      return false;
    });
    $(document).foundation();
  });

  // UNCOMMENT THE LINE YOU WANT BELOW IF YOU WANT IE8 SUPPORT AND ARE USING .block-grids
  // $('.block-grid.two-up>li:nth-child(2n+1)').css({clear: 'both'});
  // $('.block-grid.three-up>li:nth-child(3n+1)').css({clear: 'both'});
  // $('.block-grid.four-up>li:nth-child(4n+1)').css({clear: 'both'});
  // $('.block-grid.five-up>li:nth-child(5n+1)').css({clear: 'both'});

  // Hide address bar on mobile devices (except if #hash present, so we don't mess up deep linking).
  if (Modernizr.touch && !window.location.hash) {
    $(window).load(function () {
      setTimeout(function () {
        window.scrollTo(0, 1);
      }, 0);
    });
  }

})(jQuery, this);
