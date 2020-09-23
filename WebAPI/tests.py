from django.test import TestCase

#; Create your tests here.
import statistics
import time
from WebAPI.scapy.all import *
load_contrib("ospf")

default_r_num = 13

#; 等效于将0添加至序列中然后调用max函数
def 求最大值(序列):
  最大值 = 0
  for 数值 in 序列:
    if 数值 > 最大值:
      最大值 = 数值
  return 最大值

求方差 = statistics.pvariance
求均值 = statistics.mean

def 求不同值个数(序列):
  return len(set(序列))

def 求极差(序列):
  最大值 = 最小值 = None
  for 数值 in 序列:
    最大值 = max(数值,最大值) if 最大值 != None else 数值
    最小值 = min(数值,最小值) if 最小值 != None else 数值
  return 最大值 - 最小值 if 最大值 != None and 最小值 != None else 0

class 网络规模检测器类:
  def __init__(self):
    self.路由器总数 = 1
    self.接口个数 = 1
    self.路由器记录 = dict() #;键：路由器ID，值：发现时的时间戳
    self.地址记录 = dict() #;键：路由器ID，值：映射表（键：地址，值：时间戳）
  def 发现路由器(self,时间戳,路由器ID):
    print("路由器记录添加")
    print(self.路由器记录)
    self.路由器记录[路由器ID] = 时间戳
    #;此时先不更新路由器总数，等时间槽更新时再更新
  def 发现信号源(self,时间戳,路由器ID,地址):
    if 路由器ID not in self.地址记录:
      self.地址记录[路由器ID] = dict()
    self.地址记录[路由器ID][地址] = 时间戳
  def 时间槽更新(self,当前时间戳):
    #;清理路由器记录条目
    print("路由器记录删除前")
    print(self.路由器记录)
    临界时间戳 = 当前时间戳 - 2100
    垃圾桶 = list()
    for 路由器ID,时间戳 in self.路由器记录.items():
      if 时间戳 < 临界时间戳:
        垃圾桶.append(路由器ID)
    for 路由器ID in 垃圾桶:
      self.路由器记录.pop(路由器ID)
    #;清理地址记录条目
    临界时间戳 = 当前时间戳 - 90
    垃圾桶 = list()
    for 路由器ID,地址记录内表 in self.地址记录.items():
      内表垃圾桶 = list()
      for 地址,时间戳 in 地址记录内表.items():
        if 时间戳 < 临界时间戳:
          内表垃圾桶.append(地址)
      for 地址 in 内表垃圾桶:
        地址记录内表.pop(地址)
      if len(地址记录内表) == 0:
        垃圾桶.append(路由器ID)
    for 路由器ID in 垃圾桶:
      self.地址记录.pop(路由器ID)
    #;更新数据
    print("路由器记录删除后")
    print(self.路由器记录)
    路由器总数t = len(self.路由器记录)
    if (路由器总数t == 0):
      路由器总数t = default_r_num
    self.路由器总数 = 路由器总数t
    self.接口个数 = 求最大值(map(len,self.地址记录.values()))

class 洪泛LSU报文统计信息类:
  def __init__(self):
    self.LSU计数 = 0
    self.LSA序列号方差 = 0.0
    self.LSA满序列号计数 = 0
    self.LSA满年龄计数 = 0
    self.LSA计数 = 0
    self.LSA不同序列号个数 = 0
    self.LSA序列号极差 = 0
    #;以下是内部数据
    self.序列号记录 = dict()
  def 新增LSU报文(self,LSU报文):
    self.LSU计数 += 1
    for LSA in LSU报文.lsalist:
      self.LSA计数 += 1
      if LSA.seq == 0x7fffffff:
        self.LSA满序列号计数 += 1
      if LSA.age == 3600:
        self.LSA满年龄计数 += 1
      广播主体 = LSA.adrouter
      if 广播主体 not in self.序列号记录:
        self.序列号记录[广播主体] = list()
      self.序列号记录[广播主体].append(LSA.seq^0x80000000)
  def 计算特征向量(self):
    self.LSA序列号方差 = 求最大值(map(求方差,self.序列号记录.values()))
    self.LSA不同序列号个数 = 求最大值(map(求不同值个数,self.序列号记录.values()))
    self.LSA序列号极差 = 求最大值(map(求极差,self.序列号记录.values()))

class LSAcknowledge报文统计信息类:
  def __init__(self):
    self.LSA满序列号且满年龄计数 = 0
    self.LSAcknowledge计数 = 0
    self.LSA计数 = 0
  def 新增LSAcknowledge报文(self,LSAcknowledge报文):
    self.LSAcknowledge计数 += 1
    for LSA in LSAcknowledge报文.lsaheaders:
      self.LSA计数 += 1
      if LSA.seq == 0x7fffffff and LSA.age == 3600:
        self.LSA满序列号且满年龄计数 += 1
  def 计算特征向量(self):
    pass #;这里不需要操作

class LSR报文统计信息类:
  def __init__(self):
    self.LSR计数 = 0
    self.LSR不同发送者个数 = 0
    self.LSR重复请求个数 = 0
    #;以下是内部数据
    self.发送者集合 = set()
    self.请求项记录 = dict({None:1}) #;确保最大值不小于1
  def 新增LSR报文(self,LSR报文):
    self.LSR计数 += 1
    self.发送者集合.add(LSR报文.src)
    for 请求项 in LSR报文.requests:
      键 = raw(请求项) #;转成二进制字符串以后才能用作键
      self.请求项记录[键] = 1 + self.请求项记录.get(键,0)
  def 计算特征向量(self):
    self.LSR不同发送者个数 = len(self.发送者集合)
    self.LSR重复请求个数 = 求最大值(self.请求项记录.values()) - 1

class Hello报文统计信息类:
  def __init__(self):
    self.Hello计数 = 0
    self.Hello不同发送者个数 = 0
    self.共享字段不相等的报文对个数 = 0
    self.不等于众数的共享字段个数 = 0
    #;以下是内部数据
    self.发送者集合 = set()
    self.AreaID记录 = dict()
    self.AuthenticationType记录 = dict()
    self.HelloInterval记录 = dict()
    self.DeadInterval记录 = dict()
    self.StubAreaFlag记录 = dict()
    self.不相等的AreaID对个数 = 0
    self.不相等的AuthenticationType对个数 = 0
    self.不相等的HelloInterval对个数 = 0
    self.不相等的DeadInterval对个数 = 0
    self.不相等的StubAreaFlag对个数 = 0
  def 新增Hello报文(self,Hello报文):
    self.Hello计数 += 1
    self.发送者集合.add(Hello报文.src)
    def 增量操作(映射表,键):
      映射表[键] = 1 + 映射表.get(键,0)
      return sum(键值对[1] for 键值对 in filter(lambda 键值对:键值对[0]!=键,映射表.items()))
      #; 取映射表中其它键对应值之和，作为增量。
    self.不相等的AreaID对个数 += 增量操作(self.AreaID记录,Hello报文.area)
    self.不相等的AuthenticationType对个数 += 增量操作(self.AuthenticationType记录,Hello报文.authtype)
    self.不相等的HelloInterval对个数 += 增量操作(self.HelloInterval记录,Hello报文.hellointerval)
    self.不相等的DeadInterval对个数 += 增量操作(self.DeadInterval记录,Hello报文.deadinterval)
    self.不相等的StubAreaFlag对个数 += 增量操作(self.StubAreaFlag记录,Hello报文.options.E)
  def 计算特征向量(self):
    self.Hello不同发送者个数 = len(self.发送者集合)
    def 取映射表中非最大值之和(映射表):
      最大值 = 求最大值(映射表.values())
      return sum(filter(lambda 值:值!=最大值,映射表.values()))
    不等于众数的AreaID个数 = 取映射表中非最大值之和(self.AreaID记录)
    不等于众数的AuthenticationType个数 = 取映射表中非最大值之和(self.AuthenticationType记录)
    不等于众数的HelloInterval个数 = 取映射表中非最大值之和(self.HelloInterval记录)
    不等于众数的DeadInterval个数 = 取映射表中非最大值之和(self.DeadInterval记录)
    不等于众数的StubAreaFlag个数 = 取映射表中非最大值之和(self.StubAreaFlag记录)
    self.共享字段不相等的报文对个数 = max(self.不相等的AreaID对个数,self.不相等的AuthenticationType对个数,self.不相等的HelloInterval对个数,self.不相等的DeadInterval对个数,self.不相等的StubAreaFlag对个数)
    self.不等于众数的共享字段个数 = max(不等于众数的AreaID个数,不等于众数的AuthenticationType个数,不等于众数的HelloInterval个数,不等于众数的DeadInterval个数,不等于众数的StubAreaFlag个数)

规模检测器 = 网络规模检测器类()

def 提取单slot特征(单slot数据包列表):
  LSU统计 = 洪泛LSU报文统计信息类()
  LSAcknowledge统计 = LSAcknowledge报文统计信息类()
  LSR统计 = LSR报文统计信息类()
  Hello统计 = Hello报文统计信息类()
  for 数据包 in 单slot数据包列表:
    assert 数据包.haslayer(OSPF_Hdr)
    OSPF报文 = 数据包[OSPF_Hdr]
    if OSPF报文.haslayer(OSPF_Hello):
      Hello统计.新增Hello报文(OSPF报文)
    elif OSPF报文.haslayer(OSPF_LSUpd) and 数据包[IP].dst == "224.0.0.5":
      LSU统计.新增LSU报文(OSPF报文)
    elif OSPF报文.haslayer(OSPF_LSReq):
      LSR统计.新增LSR报文(OSPF报文)
    elif OSPF报文.haslayer(OSPF_LSAck):
      LSAcknowledge统计.新增LSAcknowledge报文(OSPF报文)
  LSU统计.计算特征向量()
  LSAcknowledge统计.计算特征向量()
  LSR统计.计算特征向量()
  Hello统计.计算特征向量()
  特征向量 = list()
  特征向量.append(规模检测器.路由器总数)
  特征向量.append(LSU统计.LSU计数 / 规模检测器.路由器总数 / 规模检测器.接口个数)
  特征向量.append(LSU统计.LSA序列号方差)
  特征向量.append(LSU统计.LSA满序列号计数)
  特征向量.append(LSU统计.LSA满年龄计数)
  特征向量.append(LSU统计.LSA计数 / 规模检测器.路由器总数 / 规模检测器.接口个数)
  特征向量.append(LSU统计.LSA不同序列号个数)
  特征向量.append(LSU统计.LSA序列号极差)
  特征向量.append(LSAcknowledge统计.LSA满序列号且满年龄计数)
  特征向量.append(LSAcknowledge统计.LSAcknowledge计数 / 规模检测器.路由器总数 / 规模检测器.接口个数)
  特征向量.append(LSAcknowledge统计.LSA计数 / 规模检测器.路由器总数 / 规模检测器.接口个数)
  特征向量.append(LSR统计.LSR计数 / 规模检测器.接口个数)
  特征向量.append(LSR统计.LSR不同发送者个数)
  特征向量.append(LSR统计.LSR重复请求个数)
  特征向量.append(Hello统计.Hello计数 / 规模检测器.接口个数)
  特征向量.append(Hello统计.Hello不同发送者个数)
  特征向量.append(Hello统计.共享字段不相等的报文对个数)
  特征向量.append(Hello统计.不等于众数的共享字段个数)
  return 特征向量

# 命令行参数解析器 = argparse.ArgumentParser()
# 命令行参数解析器.add_argument("input_file")
# 命令行参数 = 命令行参数解析器.parse_args()
# 输入文件名 = 命令行参数.input_file
输入文件名 = 'seq_1_8.pcap'

with open("feature_matrix.csv","w") as 输出文件:
  素Pcap解析器 = RawPcapReader(输入文件名)
  num =0
  单slot数据包列表 = list()
  特征矩阵 = list()
  上个slot时间戳 = None
  当前位于首个slot = True
  try:
    for 素数据包,元数据 in 素Pcap解析器:
      报文时间戳 = 元数据.sec
      这个slot时间戳 = 报文时间戳 // 60
      if 上个slot时间戳 == None:
        上个slot时间戳 = 这个slot时间戳
      if 这个slot时间戳 > 上个slot时间戳:
        规模检测器.时间槽更新(这个slot时间戳)
        print("******interface num:******")
        上个slot时间戳 = 这个slot时间戳

        t = 上个slot时间戳*60
        print(t)
        t = time.localtime(t)
        t = time.strftime("%Y-%m-%d %H:%M:%S", t)
        print(t)

        if not 当前位于首个slot:
          特征向量 = 提取单slot特征(单slot数据包列表)
          单slot数据包列表.clear()
          特征矩阵 += 特征向量
          num += 1
          if (num ==2):
            输出文件.write(','.join(map(str,特征矩阵))+'\n')
            特征矩阵.clear()
            特征矩阵 += 特征向量
            num =1
        当前位于首个slot = False
      if not 当前位于首个slot:
        数据包 = Ether(素数据包)
        if 数据包.haslayer(OSPF_Hdr):
          单slot数据包列表.append(数据包)
          OSPF报文 = 数据包[OSPF_Hdr]
          if OSPF报文.haslayer(OSPF_Hello) and 数据包[IP].dst == "224.0.0.5":
            规模检测器.发现信号源(报文时间戳,OSPF报文.src,数据包[IP].src)
          if OSPF报文.haslayer(OSPF_LSUpd):
            for LSA in OSPF报文.lsalist:
              规模检测器.发现路由器(报文时间戳,LSA.adrouter)
  except EOFError:
    pass
#; 注：因为首尾两个slot不完整，所以掐头去尾。
