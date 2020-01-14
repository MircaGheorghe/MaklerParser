from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('change_text', views.change_text, name='change_text'),
    path('set_category_table', views.set_category_table, name='set_category_table'),
    path('set_account', views.set_account, name='set_account'),
    path('set_link', views.set_link, name='set_link'),
    path('delete_link', views.delete_link, name='delete_link'),
    path('get_modal', views.get_modal, name='get_modal'),
    path('get_table', views.get_table, name='get_table'),
]
