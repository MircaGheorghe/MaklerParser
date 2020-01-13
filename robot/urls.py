from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('change_text', views.change_text, name='change_text'),
    path('start_parser', views.start_parser, name='start_parser'),
    path('set_category', views.set_category, name='set_category'),
    path('set_account', views.set_account, name='set_account'),
    path('set_link', views.set_link, name='set_link'),
    path('delete_link', views.delete_link, name='delete_link'),
]
