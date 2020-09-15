from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
from django.db.models import Q
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
  #这里默认路由器序号从0开始，当从1开始，max_id及links需要调整
  max_id  = -1
  links = []
  for (k,v) in adj_dict.items():
    max_id = max(max_id, k)
    for j in v:
      if (j > k):
        links.append({'source': k,'target': j, 'value': ""})
  nodes = []

  for i in range(max_id+1):
    name = 'Router-' + str(i)
    category = 0
    if i in anm_router_list:
      category = 1
    symbolSize = 40
    nodes.append({'name':name, 'category': category, 'symbolSize': symbolSize})
  return max_id+1 , nodes , links

def get_anomaly_all(anomalys):
  anomalys = anomalys.order_by('-time')
  tableData = []
  num = -1
  a_nums = [0,0,0,0,0,0]
  for a in anomalys:
    num += 1
    no = num
    date = str(a.time).strip().split(' ')[0]
    time = str(a.time).strip().split(' ')[1]
    id  = a.rid
    type = anomaly_dict[a.event]
    max_prob = max(a.prob_1, a.prob_2, a.prob_3, a.prob_4, a.prob_5, a.prob_6)
    grade = 1
    if(max_prob > 0.5):
      grade = 3
    elif(max_prob > 0.3):
      grade =2
    a_nums[a.event] += 1
    tableData.append({'no': no, 'date': date, 'time': time, 'ID': id, 'type': type, 'grade': grade})
  sum = 0
  for a in a_nums:
    sum += a
  for i in range(len(a_nums)):
    a_nums[i] = (a_nums[i] / sum )*100
  return tableData,a_nums

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
    # print(router_nb_dict)
    #路由器总数
    all_router_num, nodes , links = get_graph(router_nb_dict, abnormal_routers)

    anomalys = models.Anomaly.objects.all()
    tableData, a_radio = get_anomaly_all(anomalys)

    # 以下根据数据库中最近一小时内的异常记录
    result['status'] = status #normal or abnormal
    result['abnormal_routers'] = abnormal_routers
    result['abnormal_behaviors'] = abnormal_behaviors
    result['a_radio'] = a_radio
    result['all_router_num'] = all_router_num
    result['online_router_num'] = online_router_num
    result['danger_router_num'] = danger_router_num
    result['nodes'] = nodes
    result['links'] = links
    result['tableData'] = tableData
    return JsonResponse(result, safe=False)

  if action == "get_real_each_data":
    # 从packet里的最大（最新）时间; 后面可以按需改成当前时间
    latest_time = models.Packet.objects.all().aggregate(Max('stime'))
    # print(latest_time['stime__max'])
    monitor_from_time = latest_time['stime__max'] - datetime.timedelta(minutes=monitor_minutes)
    # print(monitor_from_time)
    monitor_anomalys = models.Anomaly.objects.filter(time__gte=monitor_from_time)
    ma_dict = {}
    for ma in monitor_anomalys:
      if ma.rid not in ma_dict:
        ma_dict[ma.rid] = []
      if ma.event not in ma_dict[ma.rid]:
        ma_dict[ma.rid].append(ma.event)
    routers_return = []
    routers = models.Router.objects.all()
    for (k,v) in ma_dict.items():
      name = 'Router-' + str(k)
      ips = routers.filter(rid = k).order_by('port').values_list('portip',flat= True)
      ips = list(ips)
      #测试情况下可能会出现packet没有相应表项的情况
      k_latest_time = models.Packet.objects.filter(rid = k).aggregate(Max('stime'))
      k_monitor_from_time = k_latest_time['stime__max'] - datetime.timedelta(minutes=monitor_minutes)
      k_monitor_packets = models.Packet.objects.filter(rid = k).filter(stime__gt = k_monitor_from_time)
      k_monitor_packets = k_monitor_packets.order_by('stime')
      k_lsr_num = k_monitor_packets.values_list('lsr_num',flat= True)
      k_hello_num = k_monitor_packets.values_list('hello_num',flat= True)
      k_lsu_num = k_monitor_packets.values_list('lsu_num',flat= True)
      k_lsa_num = k_monitor_packets.values_list('lsa_num',flat= True)
      hello_num = list(k_hello_num)
      lsr_num = list(k_lsr_num)
      lsu_num = list(k_lsu_num)
      lsa_num = list(k_lsa_num)

      for vv in v:
        #检测期内此路由器可能出现多种异常，所以用一个列表v的形式
        charts_name = ['Router-' + str(k) + '-' + str(vv) + '-rose', 'Router-' + str(k) + '-' + str(vv)+ '-line']
        show = monitor_anomalys.filter(Q(rid=k) & Q(event=vv)).order_by('time')[0]
        ano_prob = []
        ano_prob.append(show.prob_1 )
        ano_prob.append(show.prob_2 )
        ano_prob.append(show.prob_3 )
        ano_prob.append(show.prob_4 )
        ano_prob.append(show.prob_5 )
        ano_prob.append(show.prob_6 )
        time = show.time
        name = 'test2'
        routers_return.append({'name': name, 'charts_name': charts_name, 'ips':ips, 'chart_rose': "c", 'chart_line': "c",'ano_prob': ano_prob, 'hello_num': hello_num,'lsr_num':lsr_num,'lsu_num':lsu_num, 'lsa_num': lsa_num})
    result['routers'] = routers_return
    return JsonResponse(result, safe=False)

  if action == 'get_real_attack_data':
    anomalys_return =[[],[],[],[],[],[]]
    anomalys = models.Anomaly.objects.all()
    for i in range(6):
      num = -1
      anomalys_each = anomalys.filter(event = i)
      for a in anomalys_each:
        num += 1
        date = str(a.time).strip().split(' ')[0]
        time = str(a.time).strip().split(' ')[1]
        id = a.rid
        max_prob = max(a.prob_1, a.prob_2, a.prob_3, a.prob_4, a.prob_5, a.prob_6)
        grade = 1
        if (max_prob > 0.5):
          grade = 3
        elif (max_prob > 0.3):
          grade = 2
        anomalys_return[i].append({'no': num, 'date': date, 'time': time, 'ID': id, 'grade': grade})
    result['attack0'] = anomalys_return[0]
    result['attack1'] = anomalys_return[1]
    result['attack2'] = anomalys_return[2]
    result['attack3'] = anomalys_return[3]
    result['attack4'] = anomalys_return[4]
    result['attack5'] = anomalys_return[5]
    return JsonResponse(result, safe=False)

  # raise SuspiciousOperation("Operation not allowed.")
