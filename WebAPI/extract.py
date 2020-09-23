from WebAPI import models
import statistics
from WebAPI.scapy.all import *
load_contrib("ospf")
from WebAPI.views import *

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

def 提取单slot特征(单slot数据包列表,rnum, pnum,rid,time):
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
  特征向量.append(rid)
  特征向量.append(time)
  特征向量.append(rnum)
  特征向量.append(LSU统计.LSU计数 / rnum / pnum)
  特征向量.append(LSU统计.LSA序列号方差)
  特征向量.append(LSU统计.LSA满序列号计数)
  特征向量.append(LSU统计.LSA满年龄计数)
  特征向量.append(LSU统计.LSA计数 / rnum / pnum)
  特征向量.append(LSU统计.LSA不同序列号个数)
  特征向量.append(LSU统计.LSA序列号极差)
  特征向量.append(LSAcknowledge统计.LSA满序列号且满年龄计数)
  特征向量.append(LSAcknowledge统计.LSAcknowledge计数 / rnum / pnum)
  特征向量.append(LSAcknowledge统计.LSA计数 / rnum / pnum)
  特征向量.append(LSR统计.LSR计数 / pnum)
  特征向量.append(LSR统计.LSR不同发送者个数)
  特征向量.append(LSR统计.LSR重复请求个数)
  特征向量.append(Hello统计.Hello计数 / pnum)
  特征向量.append(Hello统计.Hello不同发送者个数)
  特征向量.append(Hello统计.共享字段不相等的报文对个数)
  特征向量.append(Hello统计.不等于众数的共享字段个数)
  write_packet(rid, time, Hello统计.Hello计数, LSR统计.LSR计数, LSU统计.LSA计数, LSAcknowledge统计.LSA计数)
  return 特征向量

def packets_process(rid, file_name):
  file_name = 'WebAPI/'+file_name
  素Pcap解析器 = RawPcapReader(file_name)
  num = 0
  rnum = get_num_routers()
  pnum = get_num_ports(rid)
  print('端口数量为 '+ str(pnum))
  print('路由器数量为 ' + str(rnum))
  单slot数据包列表 = list()
  特征矩阵 = list()
  上个slot时间戳 = None
  当前位于首个slot = True
  输出矩阵 = open('WebAPI/features'+str(rid)+'.csv', 'w')
  try:
    for 素数据包, 元数据 in 素Pcap解析器:
      报文时间戳 = 元数据.sec
      这个slot时间戳 = 报文时间戳 // 60
      if 上个slot时间戳 == None:
        上个slot时间戳 = 这个slot时间戳
      if 这个slot时间戳 > 上个slot时间戳:
        if not 当前位于首个slot:
          t = 上个slot时间戳 * 60
          t = time.localtime(t)
          t = time.strftime("%Y-%m-%d %H:%M:%S", t)
          特征向量 = 提取单slot特征(单slot数据包列表, rnum, pnum, rid, t)
          print(特征向量)
          单slot数据包列表.clear()
          特征矩阵 += 特征向量
          num += 1
          上个slot时间戳 = 这个slot时间戳
        当前位于首个slot = False
        if (num == 2):
          print(特征矩阵)
          输出矩阵.write(','.join(map(str,特征矩阵))+'\n')
          特征矩阵.clear()
          特征矩阵 += 特征向量
          num = 1
      if not 当前位于首个slot:
        数据包 = Ether(素数据包)
        if 数据包.haslayer(OSPF_Hdr):
          单slot数据包列表.append(数据包)
    输出矩阵.flush()
    os.fsync(输出矩阵)
    输出矩阵.close()
  except EOFError:
    pass
