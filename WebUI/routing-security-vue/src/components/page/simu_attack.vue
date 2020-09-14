<template>
  <div>
    <el-row :gutter="20" v-for="(item,index) in anomalys" :key="index">
      <el-col :span="9">
        <el-card shadow="hover" class="mgb20" style="height:450px;">
          <div class="anomaly-info">
            <div class="anomaly-info-cont">
              <div class="anomaly-info-name">{{item.name}}</div>
            </div>
          </div>
          <div class="anomaly-disc">
            {{item.disc}}
          </div>
        </el-card>
      </el-col>
      <el-col :span="15">
        <el-card shadow="hover" class="mgb20" style="height:450px;">
          <div slot="header" class="clearfix">
            <span>历史异常记录</span>
          </div>
          <el-table
              :data="item.tableData"
              border
              class="table"
              ref="multipleTable"
              header-cell-class-name="table-header"
              @selection-change="handleSelectionChange"
          >
            <el-table-column prop="no" label="序号"  align="center"></el-table-column>
            <el-table-column prop="date" label="日期"  align="center"></el-table-column>
            <el-table-column prop="time" label="时间"  align="center"></el-table-column>
            <el-table-column prop="ID" label="路由器ID" align="center"></el-table-column>
            <el-table-column prop="grade" label="风险威胁等级" align="center"></el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Schart from 'vue-schart';
import echarts from "echarts";
import bus from '../common/bus';
export default {
  name: 'simu_attack',
  data() {
    return {
      anomalys: [
        {
          name: '序列号加一攻击',
          disc: '攻击路由器收到受害路由器的LSU(Link State Update，链路状态更新)报文后，将其序号加一或者更多，重新计算校验和发送出去。受害路由器收到此错误报文后不断发送具有更大链路序号的数据分组去纠正错误信息，导致网络带宽消耗。\n',
          tableData: [
            {
              no: '1',
              date:'2020-8-21',
              time: '23:13',
              ID: '12',
              grade: '3'
            },
            {
              no: '2',
              date:'2020-8-21',
              time: '23:23',
              ID: '12',
              grade: '2'
            },
            {
              no: '3',
              date:'2020-8-21',
              time: '23:23',
              ID: '12',
              grade: '2'
            },
            {
              no: '4',
              date:'2020-8-21',
              time: '23:23',
              ID: '12',
              grade: '2'
            },
            {
              no: '5',
              date:'2020-8-21',
              time: '00:23',
              ID: '12',
              grade: '2'
            },
            {
              no: '6',
              date:'2020-8-22',
              time: '09:29',
              ID: '12',
              grade: '2'
            }
          ]
        },
        {
          name: '配置异常',
          disc: 'OSPF协议邻居节点之间共有参数不匹配，造成邻居节点失联，相应链路断路。若断路的是冗余链路，则不容易被发现，因为整个网络仍然联通。然而冗余链路断路会使其他链路的负载加重，最终可能导致网络拥塞。\n',
          tableData: [
            {
              no: '1',
              date:'2020-8-21',
              time: '22:13',
              ID: '11',
              grade: '3'
            },
            {
              no: '2',
              date:'2020-8-21',
              time: '23:23',
              ID: '12',
              grade: '2'
            },
            {
              no: '3',
              date:'2020-8-21',
              time: '23:23',
              ID: '19',
              grade: '2'
            }
          ]
        },
        {
          name: 'LSR报文伪造攻击',
          disc: '攻击者向目标路由器（受害者路由器）高速发送LSR（Link State Request，链路状态请求）报文，使得目标路由器不断响应LSR报文，发送LSU报文，大量的CPU资源被占用，导致网络带宽消耗。\n',
          tableData: [
            {
              no: '1',
              date:'2020-8-21',
              time: '23:13',
              ID: '12',
              grade: '3'
            },
            {
              no: '2',
              date:'2020-8-21',
              time: '23:23',
              ID: '12',
              grade: '2'
            },
            {
              no: '3',
              date:'2020-8-21',
              time: '23:23',
              ID: '12',
              grade: '2'
            },
            {
              no: '4',
              date:'2020-8-21',
              time: '23:23',
              ID: '12',
              grade: '2'
            },
            {
              no: '5',
              date:'2020-8-21',
              time: '00:23',
              ID: '12',
              grade: '2'
            },
            {
              no: '6',
              date:'2020-8-22',
              time: '09:29',
              ID: '12',
              grade: '2'
            }
          ]
        },
      ],

      routers: [
        {
          name: 'Router-1',
          charts_name: ['Router-1-rose','Router-1-line'],
          type: '思科 abcd',
          ips: ['192.168.1.1','192.168.1.2','192.168.1.3'],
          chart_rose: null,
          chart_line: null,
          ano_prob: [700,400,60,405,190,300],
          hello_num :[60,60,60,60,60,60,60,60,60,60,60,60],
          lsr_num :[0,0,1,3,0,0,0,4,6,0,0,0],
          lsu_num:[30,0,0,32,0,0,29,0,0,67,3,0],
          lsa_num:[21,2,0,0,1,2,34,0,0,34,0,1]
        },
        {
          name: 'Router-13',
          charts_name: ['Router-13-rose','Router-13-line'],
          type: '思科 abcd',
          ips: ['192.168.13.1','192.168.1.2','192.168.13.3','192.168.13.2'],
          chart_rose: null,
          chart_line: null,
          ano_prob: [300,400,60,405,190,300],
          hello_num :[6,60,60,60,60,62,60,60,60,60,60,60],
          lsr_num :[20,0,1,3,0,0,0,4,6,0,0,0],
          lsu_num:[30,0,0,32,0,0,49,3,0,67,3,0],
          lsa_num:[21,23,0,0,1,2,24,0,0,34,0,1]
        },
      ],
    };
  },
  mounted() {
    this.initChart();
  },
  beforeDestroy() {
    if (!this.chart_rose) {
      return;
    }
    this.chart_rose.dispose();
    this.chart_rose = null;
  },
  components: {
    Schart
  },
  computed: {
  },
  methods: {
    initChart() {
      for(var rt of this.routers){
        //rose
        rt.chart_rose = echarts.init(document.getElementById(rt.charts_name[0]));
        rt.chart_rose.setOption({
              title: {
                text: "各异常可能性",
                left: "center",
                top: 20,
                textStyle: {
                  color: "#000000"
                }
              },
              tooltip: {
                trigger: "item",
                formatter: "{a} <br/>{b} : {c} ({d}%)"
              },

              visualMap: {
                show: false,
                min: 100,
                max: 800,
                inRange: {
                  colorLightness: [1, 0]
                }
              },
              series: [
                {
                  name: "异常类型",
                  type: "pie",
                  radius: "50%",
                  center: ["50%", "50%"],
                  data: [
                    { value: rt.ano_prob[0], name: "序列号加一攻击" },
                    { value: rt.ano_prob[1], name: "配置异常" },
                    { value: rt.ano_prob[2], name: "LSR报文伪造攻击" },
                    { value: rt.ano_prob[3], name: "最大年龄攻击" },
                    { value: rt.ano_prob[4], name: "伪装攻击" },
                    { value: rt.ano_prob[5], name: "最大序列号攻击" }
                  ].sort(function(a, b) {
                    return a.value - b.value;
                  }),
                  roseType: "radius",
                  label: {
                    normal: {
                      textStyle: {
                        color: "#000000"
                      }
                    }
                  },
                  labelLine: {
                    normal: {
                      lineStyle: {
                        color: "#000000"
                      },
                      smooth: 0.2,
                      length: 2,
                      length2: 20
                    }
                  },
                  itemStyle: {
                    normal: {
                      color: "#c23531",
                      shadowBlur: 200,
                      shadowColor: "rgba(0, 0, 0, 0.5)"
                    }
                  },

                  animationType: "scale",
                  animationEasing: "elasticOut",
                  animationDelay: function(idx) {
                    return Math.random() * 200;
                  }
                }
              ]

            }
        )
        //line
        rt.chart_line = echarts.init(document.getElementById(rt.charts_name[1]))
        rt.chart_line.setOption({
          title: {
            text: "该路由器过去2小时报文随时间变化",
            left: "center",
            top: 20,
            textStyle: {
              color: "#000000"
            }
          },
          legend: {
            data: ['Hello报文', 'LSR报文', 'LSU报文', 'LSA报文']
          },
          xAxis: {
            type: 'category',
            data: ['-12', '-11', '-10', '-9', '-8', '-7', '-6', '-5', '-4', '-3', '-2', '-1'],   // x轴数据
            name: '时间(min)',
            axisLabel: {
              interval: 0
            },
            // x轴名称样式
            nameTextStyle: {
              fontWeight: 500,
              fontSize: 15
            }
          },
          yAxis: {
            type: 'value',
            name: '报文数量',   // y轴名称
            // y轴名称样式
            nameTextStyle: {
              fontWeight: 500,
              fontSize: 15
            }
          },
          tooltip: {
            trigger: 'axis'   // axis   item   none三个值
          },
          series: [
            {
              name: 'Hello报文',
              data: rt.hello_num,
              type: 'line'
            },
            {
              name: 'LSR报文',
              data: rt.lsr_num,
              type: 'line'
            },
            {
              name: 'LSU报文',
              data: rt.lsu_num,
              type: 'line'
            },
            {
              name: 'LSA报文',
              data: rt.lsa_num,
              type: 'line'
            }
          ]
        })
      }
    }


  }
};
</script>


<style scoped>
.el-row {
  margin-bottom: 20px;
}

.grid-content {
  display: flex;
  align-items: center;
  height: 100px;
}

.grid-cont-right {
  flex: 1;
  text-align: center;
  font-size: 14px;
  color: #999;
}

.grid-num {
  font-size: 30px;
  font-weight: bold;
}

.grid-con-icon {
  font-size: 50px;
  width: 100px;
  height: 100px;
  text-align: center;
  line-height: 100px;
  color: #fff;
}

.grid-con-1 .grid-con-icon {
  background: rgb(45, 140, 240);
}

.grid-con-1 .grid-num {
  color: rgb(45, 140, 240);
}

.grid-con-2 .grid-con-icon {
  background: rgb(100, 213, 114);
}

.grid-con-2 .grid-num {
  color: rgb(45, 140, 240);
}

.grid-con-3 .grid-con-icon {
  background: rgb(242, 94, 67);
}

.grid-con-3 .grid-num {
  color: rgb(242, 94, 67);
}

.anomaly-info {
  display: flex;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 2px solid #ccc;
  margin-bottom: 20px;
}

.anomaly-avator {
  width: 120px;
  height: 120px;
  border-radius: 50%;
}

.anomaly-info-cont {
  padding-left: 50px;
  flex: 1;
  font-size: 14px;
  color: #999;
}

.anomaly-info-cont div:first-child {
  font-size: 30px;
  color: #222;
}

.anomaly-info-list {
  font-size: 16px;
  color: #000000;
  line-height: 25px;
}

.anomaly-info-list span {
  margin-left: 70px;
}

.mgb20 {
  margin-bottom: 20px;
}

.table {
  width: 100%;
  font-size: 14px;
}

.schart {
  width: 350px;
  height: 210px;
}

</style>
