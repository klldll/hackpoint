#-*- coding: utf-8 -*-
"""
Views for creating, editing and viewing site-specific user profiles.

"""
import json
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404, render, redirect, resolve_url
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
from profiles.models import UserProfile, UserProject, Message


class ProifileList(ListView):
    queryset = UserProfile.objects.filter(
        user__last_login__gte=datetime.now()-timedelta(days=60)
    ).order_by('-user_role', '-user__date_joined')
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
        self.userprofile = get_object_or_None(UserProfile, user=request.user)
        return super(ProfileEditView, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            avatar = request.POST.get('avatar', None)
            userprofile = get_object_or_None(
                UserProfile, user=request.user
            )
            userprofile.avatar = avatar if avatar else '/static/i/default.ing'
            userprofile.save()
        self.userprofile = UserProfile.objects.get(user=request.user)
        return super(ProfileEditView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Возвращает словарь аргументов для экземпляра формы
        """
        kwargs = super(ProfileEditView, self).get_form_kwargs()
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
    queryset = UserProject.objects.filter(pirvate=False, archived=False)
    context_object_name = 'project_list'

    #@method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(ProjectList, self).get(request, *args, **kwargs)


class ProjectDetail(DetailView):
    context_object_name = 'project'
    queryset = UserProject.objects.filter(archived=False)

    #@method_decorator(login_required)
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
        self.userproject = get_object_or_None(
            UserProject, owner=request.user.profile
        )
        if request.is_ajax() and self.userproject:
            avatar = request.POST.get('avatar', None)
            self.userproject.avatar = avatar if avatar else '/static/i/default_project.ing'
            self.userproject.save()
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
    # TODO change absolute url to url view
    success_url = '/accounts/projects/list/'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        profile = self.request.user.profile
        if profile.empty:
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


class BaseAjaxVew(View):
    def __init__(self, *args, **kwargs):
        super(BaseAjaxVew, self).__init__(*args, **kwargs)

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


class JoinProjectView(BaseAjaxVew):

    def post(self, request):
        msg = '<div data-alert class="alert-box %s">%s<a href="#" data-dismiss="alert" class="close">&times;</a></div>'
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
        if profile and profile.in_team:
            self.messages = msg % ('alert', 'Вы уже записаны в команду.')
        elif project and profile:
            project.members.add(profile)
            self.success = True
            self.messages = msg % ('success', 'Вы успешно записаны в команду')
        else:
            self.messages = msg % ('alert', 'Команда не найдена')

        #some_signal.send(sender=MyAJAXView, instance=self)
        return HttpResponse(json.dumps(self.response_data))


class LeftProjectView(BaseAjaxVew):

    def post(self, request):
        msg = '<div data-alert class="alert-box %s">%s<a href="#" data-dismiss="alert" class="close">&times;</a></div>'
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
        if profile and not profile.in_team:
            self.messages = msg % ('alert', 'Вы не состоите ни в одной команде.')
        elif project and profile:
            try:
                project.members.remove(profile)
                self.success = True
                self.messages = msg % ('success', 'Вы покинули команду. Время искать новую!')
            except:
                self.success = False
                self.messages = msg % ('alert', 'Наверное, это не ваша команда.')
        else:
            self.messages = msg % ('alert', 'Команда не найдена')

        #some_signal.send(sender=MyAJAXView, instance=self)
        return HttpResponse(json.dumps(self.response_data))


class ConfirmRegisterView(BaseAjaxVew):

    def post(self, request):
        msg = '<div data-alert class="alert-box %s">%s<a href="#" data-dismiss="alert" class="close">&times;</a></div>'
        profile_id = request.user.profile.pk
        try:
            profile_id = int(profile_id)
        except:
            self.errors.append(u'Id профиля должно быть числом')
            profile_id = None
        if not profile_id:
            return HttpResponse(json.dumps(self.response_data))

        profile = get_object_or_None(UserProfile, pk=profile_id)
        if profile:
            try:
                profile.confirmed = True
                profile.save()
                self.success = True
                self.messages = msg % ('success', 'Вы успешно подтвердили ваше участие. Спасибо!')
            except:
                self.success = False
                self.messages = msg % ('alert', 'Уппс.. Что-то пошло не так..')
        else:
            self.messages = msg % ('alert', 'Все плохо.')

        return HttpResponse(json.dumps(self.response_data))


@ajax_request
@csrf_exempt
def register(request):
    result = False
    full_form = UserProfileForm(request.POST or None)
    simple_form = RegistrationFormUniqueEmail(request.POST or None)

    if simple_form.is_valid():
        email = simple_form.cleaned_data['email']
        password = simple_form.cleaned_data['password']
        user, __ = User.objects.get_or_create(username=email, email=email)
        user.set_password(password)
        user.save()
        msg = u'<p>Благодарим вас за регистрацию на нашем ивенте. Мы будем оповещать вас о важных событиях.</p><p>Вы уже можете <a href="http://hackpoint.ru/login/">войти на сайт</a> и найти себе команду.</p><p>С уважением организаторы.</p>'
        send_html_mail(u'Спасибо за регистрацию на hackpoint.ru', '', msg, settings.DEFAULT_FROM_EMAIL, [user.email])
        result = True
        new_user = authenticate(username=email,
                                password=password)
        login(request, new_user)
        #return HttpResponseRedirect("/dashboard/")

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
            user.profile.contact = profile.contact
            user.save()
            user.profile.save()
        result = True

    if result:
        return {
            'created': result,
            'url': resolve_url('profile_detail', pk=user.id)
        }
    return redirect('/')


@ajax_request
@csrf_exempt
def sponsorship_register(request):
    sponsor_form = SponsorshipForm(request.POST or None)

    if sponsor_form.is_valid():
        sponsor = sponsor_form.save()
        return {'created': True}
    return redirect('/')


@ajax_request
@csrf_exempt
def messages_new(request):
    text = request.POST.get('text', '')
    title = request.POST.get('title', '')
    Message.objects.create(text=text, title=title)
    return {'created': True}


@login_required
def messages_zaebee(request, id):
    msg = get_object_or_None(Message, id=id)
    text = json.loads(msg.text)
    text = text.replace('\n', '<br>')
    data = {
        'text': text,
        'title': msg.title
    }
    return render(request, 'message_zaebee.html', data)
