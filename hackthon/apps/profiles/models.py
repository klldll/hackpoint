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
    has_idea = models.BooleanField(_('Has idea'), default=False)
    text_idea = models.TextField(_('Text idea'), blank=True, null=True)
    project = models.ForeignKey('UserProject', verbose_name=_('project'),
                               related_name=_('members'),
                               blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    @models.permalink
    def get_absolute_url(self):
        return ('profile_detail', None, {'pk':str(self.pk)})


class UserProject(models.Model):
    owner = models.OneToOneField(UserProfile,
                        verbose_name=_('owner'),
                        unique=True,)
                        #related_name='project',)
    title = models.CharField(_('Title'), max_length=100)
    text_idea = models.TextField(_('Text idea'), blank=True, null=True)

    def __unicode__(self):
        return '%s - %s' % (self.owner, self.title)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    @models.permalink
    def get_absolute_url(self):
        return ('project_detail', None, {'pk':str(self.pk)})


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=User)
