import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from choices import CATEGORY_CHOICES, PRIORITY_CHOICES, STATUS_CHOICES


class RegistrationForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'required': True}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'required': True}))
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs={'placeholder': 'Username', 'required': True}), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'required': True}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required': True}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'required': True}))

    def clean_email(self):
        try:
            user = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_("The Email ID already exists. Please try another one."))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean_password(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'required': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required':True}))


class CreateTicketForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'required':True, 'class': 'form-control'}), label=_("Title"))
    description = forms.CharField(widget=forms.Textarea(attrs={'required':True, 'class': 'form-control'}), label=_("Description"))
    category = forms.ChoiceField(choices = CATEGORY_CHOICES, widget=forms.Select(attrs={'required':True, 'class': 'form-control'}), required=True, label=_("Category"))
    priority = forms.ChoiceField(choices = PRIORITY_CHOICES, widget=forms.Select(attrs={'required':True, 'class': 'form-control'}), required=True, label=_("Priority"))
    status = forms.ChoiceField(choices = STATUS_CHOICES, widget=forms.Select(attrs={'required':True, 'class': 'form-control'}), required=True, label=_("Status"))
    assignee = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'required': False, 'class': 'form-control'}))


class CreateCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'required':False, 'class': 'form-control', 'rows':4}), label=_("Comment"))
