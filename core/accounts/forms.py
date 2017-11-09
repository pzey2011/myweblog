from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' :'Username'}), max_length=100)
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class' : 'form-control' , 'placeholder' :'Password'}),max_length=100)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, Enter the username and password correctly")
        else:
            self.cleaned_data['user']=user
        return self.cleaned_data

    def login(self, cleaned_data):
        user=cleaned_data.get('user')
        return user