from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('reg/', views.Registration.as_view(), name='reg'),
    path('auth/', views.Authorization.as_view()),
    path('test/', views.TestSession.as_view())
]