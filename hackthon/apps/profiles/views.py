#-*- coding: utf-8 -*-
"""
Views for creating, editing and viewing site-specific user profiles.

"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404, render

from profiles.models import UserProfile
from profiles.forms import UserProfileForm


@login_required
def profile_list(request, public_profile_field=None,
                 template_name='profiles/profile_list.html', **kwargs):
    pass


@login_required
def profile_detail(request, username, public_profile_field=None,
                   template_name='profiles/profile_detail.html',
                   **kwargs):
    pass


@login_required
def edit_profile(request, **kwargs):
    pass


def register(request):
    import ipdb;ipdb.set_trace()
    form = UserProfileForm(request.POST or None)
    if form.is_valid():
        profile = form.save(commit=False)
        user = User.objects.create(username=profile.username, email=profile.email)
        user.profile = profile
        user.save()
        profile.save()
        return render(request, 'profiles/confirm.html', {'form': form})

    else:
        pass
    return render(request, 'profiles/register.html', {'form': form})
