#-*- coding: utf-8 -*-
"""
Views for creating, editing and viewing site-specific user profiles.

"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings

#from django.http import HttpResponse
from django.views.generic import ListView, DetailView

if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail, send_html_mail
else:
    from django.core.mail import send_mail

from annoying.decorators import ajax_request

from profiles.forms import UserProfileForm, RegistrationFormUniqueEmail, SponsorshipForm
from profiles.models import UserProfile


class ProifileList(ListView):
    #model = UserProfile
    queryset = UserProfile.objects.order_by('-user_role')
    context_object_name = 'profile_list'


class ProifileDetail(DetailView):
    context_object_name = 'profile'
    queryset = UserProfile.objects.all()


@login_required
def edit_profile(request, **kwargs):
    return render(request, 'default.html', {})


@ajax_request
@csrf_exempt
def register(request):
    result = False
    full_form = UserProfileForm(request.POST or None)
    simple_form = RegistrationFormUniqueEmail(request.POST or None)

    if simple_form.is_valid():
        email = simple_form.cleaned_data['email']
        user, __ = User.objects.get_or_create(username=email, email=email)
        msg = u'<p>Благодарим вас за регистрацию на нашем ивенте. Мы будем оповещать вас о важных событиях.</p><p>С уважением организаторы.</p>'
        send_html_mail(u'Спасибо за регистрацию на hackpoint.ru', '', msg, settings.DEFAULT_FROM_EMAIL, [user.email])
        result = True

    if full_form.is_valid():
        profile = full_form.save(commit=False)
        email = request.POST.get('email', None)
        username = request.POST.get('username', None)
        if email:
            user, created = User.objects.get_or_create(username=email, email=email)
            user.profile.username = username
            user.profile.user_skills = profile.user_skills
            user.profile.user_role = profile.user_role
            user.profile.has_idea = profile.has_idea
            user.save()
            user.profile.save()
        result = True

    if result:
        return {'created': result}
    return redirect('/')



@ajax_request
@csrf_exempt
def sponsorship_register(request):
    sponsor_form = SponsorshipForm(request.POST or None)

    if sponsor_form.is_valid():
        sponsor = sponsor_form.save()
        return {'created': True}
    return redirect('/')
