from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
import os
import subprocess

def API_action(request,action):
  result = {}
  if action == "get_data":
    pass #;TODO 实现获取数据的功能
  if action == "get_abnormal_routers":
    result['abnormal_routers']= [1,34,456]

  return JsonResponse(result, safe= False)
  # raise SuspiciousOperation("Operation not allowed.")
