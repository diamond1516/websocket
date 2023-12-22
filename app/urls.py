
from django.urls import path

from app.views import GoogleLoginView, GoogleCallbackView, Salom

urlpatterns = [
    path('auth/google', GoogleLoginView.as_view(), name='google-login'),
    path('auth/google/callback', GoogleCallbackView.as_view(), name='google-callback'),
    path('auth/test', Salom.as_view())
]



