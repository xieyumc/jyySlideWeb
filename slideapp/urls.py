# slideapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # 其他 URL 配置
    path('upload_image/', views.upload_image, name='upload_image'),
]