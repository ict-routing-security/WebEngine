import os
import subprocess
from django.http import HttpResponse

def API_action(request,action):
  #;TODO complete data-fetch operation
  return HttpResponse(f'{action}')
