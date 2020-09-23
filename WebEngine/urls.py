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
import numpy as np
from WebEngine.settings import BASE_DIR
from WebAPI.views import API_action
from WebAPI.extract import packets_process
from WebAPI.classify_model import predict
from apscheduler.schedulers.background import BackgroundScheduler

urlpatterns = [
  path('admin/',admin.site.urls,{},'admin'),
  #;TODO 添加规则，将“ui/”重定向至“ui/index.html”
  re_path(r'^ui/(?P<path>.+)$',serve,{
    'document_root':os.path.join(BASE_DIR,'WebUI/routing-security-vue/dist'),
  },'ui'),
  re_path(r'^api/(?P<action>.*)$',API_action,{},'api'),
]

scheduler = BackgroundScheduler()
def extract():
  #要求镜像的数据包具有特定命名; 后续：定期清除数据库的历史数据
  print('后台开始更新......')
  id_list = [8]
  for id in id_list:
    pkg_file_name = 'packets'+str(id)+'.pcap'
    packets_process(id, pkg_file_name)
    fea_flie = np.loadtxt('WebAPI/features'+str(id)+'.csv',delimiter=',', dtype=np.str)
    # print(fea_flie[0:3])
    predict(fea_flie)

#后续：修改成时间格式
scheduler.add_job(extract, "interval",  minutes=60)
scheduler.start()
print("Scheduler started!")

