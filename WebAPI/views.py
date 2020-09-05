from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
import os
import subprocess

def API_action(request,action):
  result = {}
  #获取real_global页面的数据，数据源来自数据库处理后的结果
  if action == "get_real_global_data":
    # 以下根据数据库中最近一小时内的异常记录
    result['status'] = 'normal' #normal or abnormal
    result['abnormal_routers'] = [1, 34, 456, 789]
    result['abnormal_behaviors'] = ['序列号加一攻击','伪装攻击']

    #以下数据库所有的异常记录
    result['tableData'] = 



  if action == "get_data":
    pass #;TODO 实现获取数据的功能


  return JsonResponse(result, safe= False)
  # raise SuspiciousOperation("Operation not allowed.")
