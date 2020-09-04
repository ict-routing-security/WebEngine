"""WebEngine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
  https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
  1. Add an import:  from my_app import views
  2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
  1. Add an import:  from other_app.views import Home
  2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
  1. Import the include() function: from django.urls import include, path
  2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.views.static import serve
import os

from WebEngine.settings import BASE_DIR
from WebAPI.views import API_action

urlpatterns = [
  path('admin/',admin.site.urls,{},'admin'),
  #;TODO 添加规则，将“ui/”重定向至“ui/index.html” test
  re_path(r'^ui/(?P<path>.+)$',serve,{
    'document_root':os.path.join(BASE_DIR,'WebUI'),
  },'ui'),
  re_path(r'^api/(?P<action>.*)$',API_action,{},'api'),
]
