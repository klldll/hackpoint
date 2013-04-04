;(function ($, window, undefined) {
  'use strict';

  var $doc = $(document),
      Modernizr = window.Modernizr;

  $(document).ready(function() {

    $.fn.placeholder ? $('input, textarea').placeholder() : null;

    $.ajaxSetup({
      beforeSend: function (xhr) {
        xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
      }
    });

    var callback = function(data, form) {
      $(form).find('small.error').remove();
      $.each(data.errors, function(key, val)  {
        $(form).find('#' + key).removeClass('error');
        $(form).find('#' + key).after('');

        if (!data.valid) {
          $(form).find('#' + key).addClass('error');
          $(form).find('#' + key).after('<small class="error">' + val + '</small>');
        }
      });
    }

    $('form#sponsorship_simple').validate(
    '/validate/sponsorshipform/', {
      callback: callback
    });

    $('form#register_full').validate(
    '/validate/userprofileform/', {
      callback: callback
    });

    $('form#register_simple').validate(
    '/validate/registrationformuniqueemail/', {
      callback: callback
    });

    $('form#register_simple2').validate(
    '/validate/registrationformuniqueemail/', {
      callback: callback
    });

    $('form#sponsorship_simple').on('form:validate', function (e) {
      $.ajax({
        url: '/accounts/register/sponsorship/',
        data: { sponsor_email: $(this).find('input[id=id_sponsor_email]').val()},
        type: 'POST',
        success : function(data, status) {
          $('#sponsorshipModal').html('<h4>Спасибо</h4><p>Мы обязательно напишем вам в ближайшее время</p><a class="close-reveal-modal">&#215;</a>');
          setTimeout(function() {$('#sponsorshipModal').fadeOut(500).foundation('reveal', 'close')}, 3000)
        }
      });
      $(this).find('small.error').remove();
      $(this).find('input').removeClass('error');
      return false;
    });

    $('form#register_simple, form#register_simple2').on('form:validate', function (e) {
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
          $('#registerModal').foundation('reveal', 'close');
        }
      });
      $(this).find('small.error').remove();
      $(this).find('input').removeClass('error');
      $(this).remove();
      return false;
    });

    $('.team_join').click(function (event) {
      $(this).addClass('disabled');
      event.preventDefault();
      var id = $(this).data('projectId'),
          target = event.target,
          profile_id = $(this).data('profileId'),
          data = {
            project_id: id,
            profile_id: profile_id
          };

      console.log(id, profile_id);
      $.post('/accounts/projects/join/', data, function (response) {
        $('.messages').html(response.messages).show();
        $(target).text('Вы в команде').removeClass('team_join');
        $('.team_join').hide();
      }, 'json');

    });

    $(document).foundation();

    // Customize twitter feed
    var hideTwitterAttempts = 0;
    function hideTwitterBoxElements() {
      setTimeout( function() {
        if ( $('[id*=twitter]').length ) {
          $('[id*=twitter]').each( function(){
            if ( $(this).width() == 220 ) {
              $(this).width( 198 ); //override min-width of 220px
            }
            var ibody = $(this).contents().find( 'body' );
            ibody.width( $(this).width() + 20 ); //remove scrollbar by adding width

            if ( ibody.find( '.timeline .stream .h-feed li.tweet' ).length ) {
              ibody.find( '.timeline .stream' ).css( 'overflow-x', 'hidden' );
              ibody.find( '.timeline .stream' ).css( 'overflow-y', 'scroll' );
            } else {
              $(this).hide();
            }
          });
        }
        hideTwitterAttempts++;
        if ( hideTwitterAttempts < 3 ) {
        hideTwitterBoxElements();
      }
      }, 1500);
    }

    // somewhere in your code after html page load
    hideTwitterBoxElements();
  });

  // Hide address bar on mobile devices (except if #hash present, so we don't mess up deep linking).
  if (Modernizr.touch && !window.location.hash) {
    $(window).load(function () {
      setTimeout(function () {
        window.scrollTo(0, 1);
      }, 0);
    });
  }

})(jQuery, this);
