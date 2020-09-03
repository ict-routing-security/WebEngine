from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
import os
import subprocess

def API_action(request,action):
  if action == "get_data":
    pass #;TODO 实现获取数据的功能
  raise SuspiciousOperation("Operation not allowed.")
