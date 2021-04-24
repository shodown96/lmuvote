from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

class VoteForm(forms.ModelForm):
    class Meta:
        model=Vote
        fields = ["category", "candidate"]

class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'lastname.firstname'}))
    email = forms.CharField(label='Webmail')
    reg_no = forms.CharField()
    # password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    # confirm_password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder': 'Enter password again'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        # exclude = ['username']
    def check_user(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            return messages.error(request, "Deadline, bruhh", "danger")
            # return self.add_error(None, "User already exists")
            # raise forms.ValidationError("User already exists")
        return username
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            return self.add_error(None,"Password Doesn't match")
            # raise forms.ValidationError("Password Doesn't match")
        return confirm_password

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea())