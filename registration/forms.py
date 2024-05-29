from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

class EmailChangeForm(forms.ModelForm):
    new_email = forms.EmailField(label=_('New Email'), max_length=254)

    class Meta:
        model = User
        fields = ['new_email']

    def clean_new_email(self):
        new_email = self.cleaned_data['new_email']
        if User.objects.filter(email=new_email).exists():
            raise ValidationError(_('This email address is already in use.'))
        return new_email
    

class FirstNameChangeForm(forms.Form):
    first_name = forms.CharField(label='New First Name', max_length=100)

class LastNameChangeForm(forms.Form):
    last_name = forms.CharField(label='New Last Name', max_length=100)  

    