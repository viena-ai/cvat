from django.urls import path

from .views import *

urlpatterns=[
    path('does_user_exists', does_user_exists)
]
