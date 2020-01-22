from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('logout', views.page_logout, name='logout'),
    path('change_status', views.change_status, name='change_status'),
    path('set_category', views.set_category, name='set_category'),
    path('set_account', views.set_account, name='set_account'),
    path('set_link', views.set_link, name='set_link'),
    path('delete_link_cat', views.delete_link_cat, name='delete_link_cat'),
    path('delete_acc', views.delete_acc, name='delete_acc'),
    path('get_modal', views.get_modal, name='get_modal'),
    path('get_table', views.get_table, name='get_table'),
    path('get_acc_modal', views.get_acc_modal, name='get_acc_modal'),
    path('get_chat_id', views.get_chat_id, name='get_chat_id'),
]
