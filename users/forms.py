from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User

class UserrLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Введите ваш логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder':'Введите пароль'}))
    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Введите ваше имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Введите вашу фамилию'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control', 'placeholder':'Введите ваш e-mail'}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Введите ваше логин'}))
    INN = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Введите ваш ИНН'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder':'Ваш пароль'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder':'Ваш пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder':'Ваш пароль'}))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'INN', 'password', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
            'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control', 'readonly': True}))
    INN = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'INN', 'password', 'password1', 'password2')
        