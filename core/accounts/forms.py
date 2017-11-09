from django import forms
from django.contrib.auth import authenticate
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                               max_length=100)
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                               max_length=100)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, Enter the username and password correctly")
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

    def login(self, cleaned_data):
        user = cleaned_data.get('user')
        return user

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                               max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}), max_length=100)
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}), max_length=100)
    email = forms.EmailField(label='Email',widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}),max_length=255)

    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        email = self.cleaned_data.get('email')
        if password != password_confirm:
            self.add_error('password_confirm', "passwords do not match !")
        if Profile.objects.filter(email=email).count() > 0:
            self.add_error('email','Email is already in use!')

        return self.cleaned_data

    def save(self,cleaned_data):
        self.password = self.cleaned_data.pop('password')
        self.cleaned_data.pop('password_confirm')
        #todo erase print
        print('user_data: ',cleaned_data)

        profile = Profile.objects.create(**cleaned_data)
        profile.set_password(self.password)
        profile.save()
        return profile
