from django.urls import path
from . import views

app_name = 'cls'
urlpatterns = [
    path('', views.index, name='index')
]