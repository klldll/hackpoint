#-*- coding: utf-8 -*-
"""
Views for creating, editing and viewing site-specific user profiles.

"""
import json

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.contrib import messages

from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView, UpdateView, CreateView

if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail, send_html_mail
else:
    from django.core.mail import send_mail

from annoying.decorators import ajax_request
from annoying.functions import get_object_or_None

from profiles.forms import UserProfileForm, RegistrationFormUniqueEmail, SponsorshipForm, UserProjectForm
from profiles.models import UserProfile, UserProject


class ProifileList(ListView):
    queryset = UserProfile.objects.order_by('-user_role')
    context_object_name = 'profile_list'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(ProifileList, self).get(request, *args, **kwargs)


class ProifileDetail(DetailView):
    context_object_name = 'profile'
    queryset = UserProfile.objects.all()

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(ProifileDetail, self).get(request, *args, **kwargs)


class ProfileEditView(UpdateView):
    form_class = UserProfileForm
    model = UserProfile
    template_name = 'profiles/edit_profile.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.userprofile = UserProfile.objects.get(user=request.user)
        return super(ProfileEditView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Возвращает словарь аргументов для экземпляра формы
        """
        kw = super(ProfileEditView, self).get_form_kwargs()
        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
                'instance': self.request.user.profile
            })
        if self.request.method == 'GET':
            kwargs.update({
                'instance': self.userprofile
            })
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, u'Ваш профиль успешно обновлен.')
        return super(ProfileEditView, self).form_valid(form)


class ProjectList(ListView):
    queryset = UserProject.objects.all()
    context_object_name = 'project_list'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(ProjectList, self).get(request, *args, **kwargs)


class ProjectDetail(DetailView):
    context_object_name = 'project'
    queryset = UserProject.objects.all()

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(ProjectDetail, self).get(request, *args, **kwargs)


class ProjectEditView(UpdateView):
    form_class = UserProjectForm
    model = UserProject
    template_name = 'profiles/edit_project.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.userproject = get_object_or_404(UserProject, owner=request.user)
        return super(ProjectEditView, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.userproject = UserProject.objects.get(owner=request.user)
        return super(ProjectEditView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Возвращает словарь аргументов для экземпляра формы
        """
        kw = super(ProjectEditView, self).get_form_kwargs()
        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
                'instance': self.userproject
            })
        if self.request.method == 'GET':
            kwargs.update({
                'instance': self.userproject
            })
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, u'Ваш проект успешно обновлен.')
        return super(ProjectEditView, self).form_valid(form)


class ProjectCreateView(CreateView):
    model = UserProject
    form_class = UserProjectForm
    template_name = 'profiles/create_project.html'
    success_url = '/accounts/projects/list/'

    def dispatch(self, *args, **kwargs):
        profile = self.request.user.profile
        if profile.empty():
            messages.success(self.request, u'Заполните пожалуйста свой профиль. Ваше имя и ваши навыки.', 'alert')
            return redirect('profile_detail', pk=profile.pk)
        as_member = UserProject.objects.filter(members=profile).exists()
        as_owner = UserProject.objects.filter(owner=profile).exists()
        if as_member:
            messages.success(self.request, u'Вы уже присоединились к проекту. Вы должны сначала покинуть проект, чтобы создать новый.', 'alert')
        if as_owner:
            messages.success(self.request, u'Вы можете создать только один проект. И он уже создан.', 'alert')
        if as_owner or as_member:
            return redirect('project_list')
        return super(ProjectCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user.profile
        self.object.save()

        messages.success(self.request, u'Ваш проект успешно создан.')
        return redirect(self.get_success_url())



class JoinProjectView(View):
    def __init__(self, *args, **kwargs):
        super(JoinProjectView, self).__init__(*args, **kwargs)

        self.errors = []
        self.messages = []
        self.data = {}
        self.success = False


    @property
    def response_data(self):
        """
        Format response data
        """
        return {
            'success': self.success,
            'errors': self.errors,
            'data': self.data,
            'messages': self.messages,
        }

    def post(self, request):
        msg = '<div data-alert class="alert-box %s">%s<a data-dismiss="alert" class="close">×</a></div>'
        #import ipdb;ipdb.set_trace()
        project_id = request.POST.get('project_id')
        profile_id = request.POST.get('profile_id')
        try:
            project_id = int(project_id)
        except:
            self.errors.append(u'Id проекта должно быть числом')
            project_id = None
        try:
            profile_id = int(profile_id)
        except:
            self.errors.append(u'Id профиля должно быть числом')
            profile_id = None
        if not project_id and not profile_id:
            return HttpResponse(json.dumps(self.response_data))

        project = get_object_or_None(UserProject, pk=project_id)
        profile = get_object_or_None(UserProfile, pk=profile_id)
        if profile and profile.in_team():
            self.messages = msg % ('alert', 'Вы уже записаны в команду.')
        elif project and profile:
            project.members.add(profile)
            self.success = True
            self.messages = msg % ('success', 'Вы успешно записаны в команду')
        else:
            self.messages = msg % ('alert', 'Команда не найдена')

        #some_signal.send(sender=MyAJAXView, instance=self)
        return HttpResponse(json.dumps(self.response_data))


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
