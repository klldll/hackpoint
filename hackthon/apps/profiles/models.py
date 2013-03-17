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

class UserProfile(models.Model):
    user = models.OneToOneField(User,
                        verbose_name=_('profile'),
                        unique=True,
                        related_name='profile',)
    username = models.CharField(_('Username'), max_length=100)
    email = models.EmailField(_('E-mail'))
    user_skills = models.TextField(_('User skills'))
    user_role = models.CharField(_('User role'), max_length=30,
                           choices=USER_ROLES)
    has_idea = models.BooleanField(_('Has idea'), default=False)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    @models.permalink
    def get_absolute_url(self):
        return ('profiles.views.profile_detail', [str(self.user.username)])


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=User)
