# from django import forms

# class UserRegForm(forms.Form):
#     username = forms.CharField(max_length = 21)
#     password = forms.CharField(widget = forms.PasswordInput())
#     email = forms.CharField(widget=forms.EmailInput())


# import form class from django
from django import forms
  
# import GeeksModel from models.py
from django.contrib.auth.models import User
  
# create a ModelForm
class UserRegistrationForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        