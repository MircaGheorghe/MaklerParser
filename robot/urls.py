from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('start', views.start_parser, name='start_parser'),
]
