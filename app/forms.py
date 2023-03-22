from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation



# forgot password form
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=255, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'} ))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete' :'new-password', 'class' : 'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete' :'new-password', 'class': 'form-control'})) 
