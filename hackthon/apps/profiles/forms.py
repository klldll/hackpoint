#-*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from models import UserProfile, SponsorProfile, UserProject
from utils import clear_email


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('user',) # User will be filled in by the view.


class UserProjectForm(forms.ModelForm):

    class Meta:
        model = UserProject
        exclude = ('owner',) # User will be filled in by the view.



# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = {'class': 'required'}


class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.

    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               max_length=75)),
                             label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password (again)"))

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("User with this username already exists."))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("Password does not match."))
        return self.cleaned_data


class RegistrationFormUniqueEmail(forms.Form):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.

    """
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                    maxlength=75)),
                                                    label=_("Email address"))
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=clear_email(email)).exists():
            raise forms.ValidationError(u"Такой email уже есть. Укажите, пожалуйста, другой адрес.")
        return email


class SponsorshipForm(forms.ModelForm):

    class Meta:
        model = SponsorProfile

    def clean_email(self):
        return email
