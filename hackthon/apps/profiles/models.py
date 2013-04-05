# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

from django.utils.translation import ugettext_lazy as _


USER_ROLES = (
    ('programmer', u'Программист'),
    ('designer', u'Дизайнер'),
    ('manager', u'Менеджер'),
    ('student', u'Студент'),
    ('other', u'Другое'),
)


class SponsorProfile(models.Model):

    sponsor_email = models.EmailField(_('email'), max_length=75)

    def __unicode__(self):
        return self.sponsor_email


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                        verbose_name=_('user'),
                        unique=True,
                        related_name='profile',)
    username = models.CharField(_('Username'), max_length=100)
    user_skills = models.TextField(_('User skills'))
    user_role = models.CharField(_('User role'), max_length=30,
                           choices=USER_ROLES)
    contact = models.CharField(_('Contact'), max_length=40, null=True)
    phone = models.CharField(_('Phone'), max_length=40, blank=True, null=True)
    has_idea = models.BooleanField(_('Has idea'), default=False)
    text_idea = models.TextField(_('Text idea'), blank=True, null=True)
    project = models.ForeignKey('UserProject', verbose_name=_('project'),
                               related_name=_('members'),
                               blank=True, null=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __unicode__(self):
        return self.user.username

    def in_team(self):
        try:
            team =  self.project or self.group
        except:
            return False
        if team:
            return True

    @property
    def team(self):
        if self.in_team():
            return self.project if self.project else self.group

    def empty(self):
        if self.username and self.user_skills:
            return False
        return True

    @models.permalink
    def get_absolute_url(self):
        return ('profile_detail', None, {'pk':str(self.pk)})


class UserProject(models.Model):
    owner = models.OneToOneField(UserProfile,
                        verbose_name=_('owner'),
                        unique=True,
                        related_name='group',
                        blank=True)
    title = models.CharField(_('Title'), max_length=100)
    text_idea = models.TextField(_('Text idea'), blank=True, null=True)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __unicode__(self):
        return '%s - %s' % (self.owner, self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('project_detail', None, {'pk':str(self.pk)})


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=User)
