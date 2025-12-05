from django.urls import re_path
from . import views

urlpatterns = [
    re_path('login', views.Login.as_view()),
    re_path('logout', views.Logout.as_view()),
    re_path('test-token', views.test_token.as_view()),
]