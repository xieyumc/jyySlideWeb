# slideapp/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_slide, name='create_slide'),
    path('edit/<int:slide_id>/', views.edit_slide, name='edit_slide'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('delete/<int:slide_id>/', views.delete_slide, name='delete_slide'),
# 登录和注销
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

]