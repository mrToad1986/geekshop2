import requests
from django.conf import settings
from authapp.models import ShopUserProfile
from datetime import datetime
from social_core.exceptions import AuthForbidden


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return
    base_url = 'http://api.vk.com/method/users.get'

    fields_for_request = ['bdate', 'sex', 'about', 'langs', 'photo_max_orig']
    params = {
        'fields': ','.join(fields_for_request),
        'access_token': response['access_token'],
        'v': settings.API_VERSION
    }

    api_response = requests.get(base_url, params=params)

    if api_response.status_code != 200:
        return
    api_data = api_response.json()['response'][0]

    if 'sex' in api_data:
        if api_data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif api_data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        else:
            user.shopuserprofile.gender = ShopUserProfile.UNKNOWN

    if 'about' in api_data:
        user.shopuserprofile.about_me = api_data['about']

    if 'bdata' in api_data:
        bdata = datetime.strptime(api_data['bdate'], "%d.%m.%Y").date()
        age = datetime.now().year - bdata.year
        #if age < 100:
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    if 'langs' in api_data:
        print(api_data['langs'])

    if 'photo_max_orig' in api_data:
        #user.avatar = api_data['photo_max_orig']
        avatar_url = api_data['photo_max_orig']
        avatar_response = requests.get(avatar_url)
        avatar_path = f'{settings.MEDIA_ROOT}/users/{user.pk}.jpg'
        with open(avatar_path, 'wb') as avatar_file:
            avatar_file.write(avatar_response.content)
        user.avatar = f'users/{user.pk}.jpg'

    user.save()


