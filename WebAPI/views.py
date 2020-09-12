from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
from WebAPI import models
from django.db.models import Max
import os
import subprocess
import datetime

monitor_minutes = 60
anomaly_dict = {0:'序列号加一攻击', 1:'配置异常', 2:'LSR报文伪造攻击',3:'最大年龄攻击', 4:'伪装攻击', 5:'最大序列号攻击'}

def list_delete_duplicate(orinl):
  newl = []
  for i in orinl:
    if i not in newl:
      newl.append(i)
  return newl

def get_abn_bhvs(l):
  newl = []
  for i in l:
    newl.append(anomaly_dict[i])
  return newl

def get_graph(adj_dict, anm_router_list):
  #理论上存在节点没有邻居所以在adj_dict中没有表项的情况，所以节点的最大ID通过提前遍历得到
  max_id  = -1
  for (k,v) in adj_dict.items():
    max_id = max(max_id, k)
  ???

def API_action(request,action):
  result = {}
  #获取real_global页面的数据，数据源来自数据库处理后的结果
  if action == "get_real_global_data":
    # 从packet里的最大（最新）时间; 后面可以按需改成当前时间
    latest_time = models.Packet.objects.all().aggregate(Max('stime'))
    # print(latest_time['stime__max'])
    monitor_from_time = latest_time['stime__max'] - datetime.timedelta(minutes=monitor_minutes)
    # print(monitor_from_time)
    monitor_anomalys = models.Anomaly.objects.filter(time__gte=monitor_from_time)
    abnormal_routers = monitor_anomalys.values_list('rid',flat = True)
    # print(list(abnormal_routers))
    abnormal_routers = list_delete_duplicate(list(abnormal_routers))
    status = 'normal'
    danger_router_num =len(abnormal_routers)
    if(danger_router_num > 0):
      status = 'abnormal'
    abnormal_behaviors = monitor_anomalys.values_list('event',flat = True)
    abnormal_behaviors = list_delete_duplicate(list(abnormal_behaviors))
    abnormal_behaviors = get_abn_bhvs(abnormal_behaviors)
    # print(abnormal_behaviors)

    routers = models.Router.objects.all()
    router_nb_dict = {}
    for router in routers:
      if router.rid not in router_nb_dict:
        router_nb_dict[router.rid] = []
      router_nb_dict[router.rid].append(router.neibrid)
    online_router_num = len(router_nb_dict) #当某个节点没有邻居的时候，将不会被统计
    all_router_num = online_router_num  #路由器总数，应该为手动获取，这里直接等于在线路由器总数
    # print(router_nb_dict)

    # 以下根据数据库中最近一小时内的异常记录
    result['status'] = status #normal or abnormal
    result['abnormal_routers'] = list(abnormal_routers)
    result['abnormal_behaviors'] = abnormal_behaviors
    #以下数据库所有的异常记录
    result['tableData'] = [{
        'no': '1',
        'date':'2020-8-21',
        'time': '23:13',
        'ID': '12',
        'type': '序列号加一攻击',
        'grade': '3'
      },
      {
        'no': '2',
        'date': '2020-8-21',
        'time': '23:21',
        'ID': '12',
        'type': '伪装攻击',
        'grade': '2'
      },
      {
        'no': '3',
        'date': '2020-8-21',
        'time': '00:21',
        'ID': '12',
        'type': '最大序列号攻击',
        'grade': '2'
      },
    ]
  if action == "get_data":
    pass #;TODO 实现获取数据的功能


  return JsonResponse(result, safe= False)
  # raise SuspiciousOperation("Operation not allowed.")
