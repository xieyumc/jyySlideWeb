# slideapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_slide, name='create_slide'),
    path('edit/<int:slide_id>/', views.edit_slide, name='edit_slide'),
    path('upload_image/', views.upload_image, name='upload_image'),
]