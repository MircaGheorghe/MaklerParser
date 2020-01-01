from django.contrib import admin
from django.urls import path, include
from robot import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('robot.urls')),
]
