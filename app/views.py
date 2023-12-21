import pprint

from django.shortcuts import render

# Create your views here.


# views.py
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views import View
import requests



class GoogleLoginView(View):
    def get(self, request, *args, **kwargs):
        # Google OAuth yozuvini olish
        google_oauth_url = 'https://accounts.google.com/o/oauth2/auth'
        client_id = '404527887290-4qb6bantq9c9nucb8vd6nbe484re6g18.apps.googleusercontent.com'  # Google yonida olingan client_id
        redirect_uri = 'http://localhost:8000/auth/google/callback'  # Google yonida olingan redirect_uri
        scope = 'openid profile email'  # Siz kerakli huquqlarni sozlab chiquvchi ruhnoma

        google_auth_url = f'{google_oauth_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type=code'
        return redirect(google_auth_url)


# views.py


class GoogleCallbackView(View):
    def get(self, request, *args, **kwargs):
        # Google dan kelgan ma'lumotlarni tekshirish
        code = request.GET.get('code')
        redirect_uri = 'http://localhost:8000/auth/google/callback'  # Google yonida olingan redirect_uri

        # Token so'rovi
        token_url = 'https://accounts.google.com/o/oauth2/token'
        token_payload = {
            'code': code,
            'client_id': '404527887290-4qb6bantq9c9nucb8vd6nbe484re6g18.apps.googleusercontent.com',
            'client_secret': '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',
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
        # pprint.pprint(token_payload)
        response = requests.post(token_url, data=token_payload)
        access_token = response.json().get('access_token')
        # print(access_token)

        # Foydalanuvchi ma'lumotlarini olish
        user_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        user_response = requests.get(user_url, headers={'Authorization': f'Bearer {access_token}'})
        user_data = user_response.json()

        # Foydalanuvchini serverda yaratish yoki kirish
        # ...
        # pprint.pprint(user_data)
        return JsonResponse({'status': user_data})
