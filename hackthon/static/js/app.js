;(function ($, window, undefined) {
  'use strict';

  var $doc = $(document),
      Modernizr = window.Modernizr;

  $(document).ready(function() {

    if (document.location.hash == '#mapModal') {
      $('#mapModal').foundation('reveal', 'open');
    };

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
        data: {
          email: $(this).find('input[id=id_email]').val(),
          password: $(this).find('input[id=id_password]').val()
        },
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
        contact: $(this).find('[id=id_contact]').val(),
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
          if (data.url) {
            document.location.href = data.url;
          }
        }
      });
      $(this).find('small.error').remove();
      $(this).find('input').removeClass('error');
      $(this).remove();
      return false;
    });

    $('.project_detail').delegate('a.team_left', 'click', function (event) {
      event.preventDefault();
      var id = $(this).data('projectId'),
          target = event.target,
          profile_id = $(this).data('profileId'),
          data = {
            project_id: id,
            profile_id: profile_id
          };

      $.post('/accounts/projects/left/', data, function (response) {
        $('.messages').html(response.messages).show();
        if (response.success === true) {
          $(target).hide()
            .parent()
            .find('.team_joined')
            .text('Хочу в команду')
            .removeClass('team_joined disabled')
            .addClass('team_join');
            $('.team_join').html('<i class="foundicon-checkmark"></i>&nbsp;Хочу в команду').show();
          $(target).hide();
        }
      }, 'json');
    });

    $('.project_detail').delegate('a.team_join', 'click', function (event) {
      event.preventDefault();
      var id = $(this).data('projectId'),
          target = event.target,
          profile_id = $(this).data('profileId'),
          data = {
            project_id: id,
            profile_id: profile_id
          };

      $.post('/accounts/projects/join/', data, function (response) {
        $('.messages').html(response.messages).show();
        if (response.success === true) {
          $(target).html('<i class="foundicon-checkmark"></i>&nbsp;Вы в команде')
            .removeClass('team_join')
            .addClass('team_joined disabled')
            .parent()
            .find('.team_left')
            .show();
          $('.team_join').hide();
        }
      }, 'json');
    });

    $('.has_idea').click(function (event) {
      event.preventDefault();
      $(this).next().toggleClass('hide');
    });

    $('#total_confirm').click(function (event) {
      event.preventDefault();
      $(this).addClass('disabled');
      var profile_id = $(this).data('profileId'),
          data = {
            profile_id: profile_id
          };

      $.post('/accounts/projects/confirm/', data, function (response) {
        $('.messages').html(response.messages).show();
        if (response.success === true) {
          $('#total_confirm').hide();
        }
      }, 'json');

    });

    $(document).foundation();

  });

  if (Modernizr.touch && !window.location.hash) {
    $(window).load(function () {
      setTimeout(function () {
        window.scrollTo(0, 1);
      }, 0);
    });
  }

})(jQuery, this);
