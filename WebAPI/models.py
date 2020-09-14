from django.db import models

#; Create your models here.
class Router(models.Model):
    #需要满足对称性
    rid = models.PositiveSmallIntegerField() #路由器ID from 0
    port = models.PositiveSmallIntegerField() #端口
    portip = models.GenericIPAddressField() #端口IP
    neibrid = models.PositiveSmallIntegerField() #端口邻居路由器ID

class Anomaly(models.Model):
    rid = models.PositiveSmallIntegerField()
    time = models.DateTimeField(auto_now= False)
    event = models.PositiveSmallIntegerField() #序列号加一攻击，配置异常，LSR报文伪造攻击，最大年龄攻击，伪装攻击，最大序列号攻击分别为0-5 必须从0开始
    prob_1 = models.FloatField()  #实际应为prob_0
    prob_2 = models.FloatField()
    prob_3 = models.FloatField()
    prob_4 = models.FloatField()
    prob_5 = models.FloatField()
    prob_6 = models.FloatField()

class Packet(models.Model):
    #暂时定为一个小时更新一次
    rid = models.PositiveSmallIntegerField()
    stime = models.DateTimeField(auto_now= False) #每分钟起始时间
    hello_num = models.PositiveSmallIntegerField()
    lsr_num = models.PositiveSmallIntegerField()
    lsu_num = models.PositiveSmallIntegerField()
    lsa_num = models.PositiveSmallIntegerField()