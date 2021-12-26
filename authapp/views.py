from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser


def login(request):
    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))

    context = {
        'title': 'Авторизация',
        'window_title': 'Вход в систему',
        'login_form': login_form
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    context = {
        'title': 'Редактирование',
        'window_title': 'Редактирование профиля',
        'edit_form': edit_form
    }

    return render(request, 'authapp/edit.html', context)


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(data=request.POST)
        if register_form.is_valid():
            user = register_form.save()
            send_verify_mail(user)
            return HttpResponseRedirect(reverse('authapp:login'))
    else:
        print('no')
        register_form = ShopUserRegisterForm()

    context = {
        'title': 'Регистрация',
        'window_title': 'Регистрация пользователя',
        'register_form': register_form
    }

    return render(request, 'authapp/register.html', context)

#вынести в authapp/services.py:
def verify(request, email, activation_key):
    user = ShopUser.objects.filter(email=email).first()
    if user:
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.activation_key = None
            user.activation_key_expired = None
            user.save()
            auth.login(request, user)
        return render(request, 'authapp/verify.html')

def send_verify_mail(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
    subject = 'Account verify'
    message = f'{settings.BASE_URL}{verify_link}'

    ##для отправки письма по html-шаблону
    #context = {...}
    #message = render_to_string('email')
    #return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], html_message=message, fail_silently=False)

    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
