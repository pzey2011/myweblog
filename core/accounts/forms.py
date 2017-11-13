from django import forms
from django.contrib.auth import authenticate
from .models import Profile
from core.posts.models import Post,Comment,Tag
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

        profile = Profile.objects.create(**cleaned_data)
        profile.set_password(self.password)
        profile.save()
        return profile

class PostCreateForm(forms.Form):
    PRIVACY_CHOICES = (('Private','lock'), ('Public','globe'))

    title=forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=forms.TextInput)
    text = forms.CharField(widget=forms.Textarea(attrs={'row':"2" , 'class':'materialize-textarea'}))
    image= forms.FileField(label='Post Image')
    privacy = forms.ChoiceField(
        widget=forms.Select(attrs={'class':'form-control'}),
        choices=PRIVACY_CHOICES,
    )
    def clean(self):
        return self.cleaned_data