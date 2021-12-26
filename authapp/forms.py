from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
import random
import hashlib
from datetime import datetime
from authapp.models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'age', 'avatar', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.activation_key_expired = datetime.now()
        user.save()
        return user

    def clean_age(self):
        data_age = self.cleaned_data['age']
        if data_age < 18:
            raise forms.ValidationError('Ваш возраст слишком маленький.')
        return data_age


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'age', 'email', 'password', 'avatar',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data_age = self.cleaned_data['age']
        if data_age < 18:
            raise forms.ValidationError('Ваш возраст слишком маленький.')
        return data_age

    # username = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    # email = forms.CharField(widget=forms.EmailInput(attrs={
    #     'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'}))
    # first_name = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'form-control py-4', 'placeholder': 'Введите имя'}))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'form-control py-4', 'placeholder': 'Введите фамилию'}))
    # avatar = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control py-4', }),
    #                          required=False, label=u'Аватар')
    # password1 = forms.CharField(widget=forms.PasswordInput(attrs={
    #     'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))
    # password2 = forms.CharField(widget=forms.PasswordInput(attrs={
    #     'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'}))
    #
    # class Meta:
    #     model = ShopUser
    #     fields = ('username', 'email', 'first_name', 'last_name', 'avatar', 'password1', 'password2')
