<template>
  <div>
    <el-row :gutter="20" v-for="(item,index) in routers" :key="index">
      <el-col :span="6">
        <el-card shadow="hover" class="mgb20" style="height:450px;">
          <div class="router-info">
            <div class="router-info-cont">
              <div class="router-info-name">{{item.name}}</div>
            </div>
          </div>
          <div class="router-info-list" v-for="(ip,i) in item.ips" :key="i">
            路由器端口{{i}}的IP：
            <span>{{ip}}</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="mgb20" style="height:450px;">
          <div class="prob_rose">
            <div :class="rose" :id="item.charts_name[0]" style="height: 450px;,width: 460px" ref="myEchart"></div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card shadow="hover" class="mgb20" style="height:450px;">
          <div class="time_line">
            <div :class="line" :id="item.charts_name[1]" style="height: 440px;,width: 460px"></div>
          </div>
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
  name: 'simu_each',
  data() {
    return {
      routers: [
        {
          name: 'Router-1',
          charts_name: ['Router-1-1-rose','Router-1-1-line'],
          type: '思科 abcd',
          ips: ['192.168.1.1','192.168.1.2','192.168.1.3'],
          'chart_rose': null,
          'chart_line': null,
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
        {
          name: 'Router-7',
          charts_name: ['Router-7-rose','Router-7-line'],
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

.router-info {
  display: flex;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 2px solid #ccc;
  margin-bottom: 20px;
}

.router-avator {
  width: 120px;
  height: 120px;
  border-radius: 50%;
}

.router-info-cont {
  padding-left: 50px;
  flex: 1;
  font-size: 14px;
  color: #999;
}

.router-info-cont div:first-child {
  font-size: 30px;
  color: #222;
}

.router-info-list {
  font-size: 16px;
  color: #000000;
  line-height: 25px;
}

.router-info-list span {
  margin-left: 70px;
}

.mgb20 {
  margin-bottom: 20px;
}

.todo-item {
  font-size: 14px;
}

.todo-item-del {
  text-decoration: line-through;
  color: #999;
}

.schart {
  width: 350px;
  height: 210px;
}
.test {
  position:absolute;
  right:1200px;
  bottom:2100px;
}
</style>
