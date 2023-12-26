import pprint

from django.shortcuts import render
from django.shortcuts import redirect
import requests
from rest_framework import views, generics
from rest_framework.response import Response


class GoogleLoginView(views.APIView):
    def get(self, request, *args, **kwargs):
        google_oauth_url = 'https://accounts.google.com/o/oauth2/auth'
        client_id = '404527887290-4qb6bantq9c9nucb8vd6nbe484re6g18.apps.googleusercontent.com'
        redirect_uri = 'http://localhost:8000/auth/google/callback'
        scope = 'openid profile email'

        google_auth_url = f'{google_oauth_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type=code'
        return redirect(google_auth_url)


# views.py


class GoogleCallbackView(views.APIView):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        redirect_uri = 'http://localhost:8000/auth/google/callback'
        token_url = 'https://accounts.google.com/o/oauth2/token'
        token_payload = {
            'code': code,
            'client_id': '404527887290-4qb6bantq9c9nucb8vd6nbe484re6g18.apps.googleusercontent.com',
            'client_secret': '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',
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
        response = requests.post(token_url, data=token_payload)
        access_token = response.json().get('access_token')
        user_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        user_response = requests.get(user_url, headers={'Authorization': f'Bearer {access_token}'})
        user_data = user_response.json()

        return Response({'msg': user_data})
        # return redirect(f'https://soff.uz?token={access_token}')


class Salom(views.APIView):

    def get(self, request):
        return Response({'msg': 'salom'})
