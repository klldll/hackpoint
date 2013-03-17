#-*- coding: utf-8 -*-
"""
Views for creating, editing and viewing site-specific user profiles.

"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings

if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail, send_html_mail
else:
    from django.core.mail import send_mail

from profiles.models import UserProfile
from profiles.forms import UserProfileForm


@login_required
def profile_list(request, **kwargs):
    pass


@login_required
def profile_detail(request, username, **kwargs):
    pass


@login_required
def edit_profile(request, **kwargs):
    pass


def register(request):
    form = UserProfileForm(request.POST or None)
    if form.is_valid():
        profile = form.save(commit=False)
        user, created = User.objects.get_or_create(username=profile.username, email=profile.email)
        user.profile.username = profile.username
        user.profile.email = profile.email
        user.profile.has_idea = profile.has_idea
        user.profile.user_skills = profile.user_skills
        user.profile.user_role = profile.user_role
        user.save()
        user.profile.save()
        msg = u'<p>Благодарим вас за регистрацию на нашем ивенте. Мы будем оповещать вас о важных событиях.</p><p>С Уважением огранизаторы.</p>'
        send_html_mail(u'Спасибо за регистрацию на hackpoint.ru', '', msg, settings.DEFAULT_FROM_EMAIL, [user.email])
        return redirect('/accounts/register/thank/')
    else:
        pass
    return render(request, 'profiles/register.html', {'form': form})


def register_thank(request):
    return render(request, 'profiles/register_confirm.html', {'message': u'Поздавляем, вы успешно зарегистрировались на хакатон! Скоро мы напишем вам email.'})
