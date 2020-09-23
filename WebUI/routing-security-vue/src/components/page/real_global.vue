<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card shadow="hover" class="mgb20" style="height:312px;">
          <div class="user-info">
            <img :src="get_status_pic" class="user-avator" alt />
            <div class="user-info-cont">
              <div class="user-info-name">{{get_status_disc}}</div>
            </div>
          </div>
          <div class="user-info-list">
            可能的异常路由器：
            <span>{{abnormal_routers}}</span>
          </div>
          <div class="user-info-list">
            可能存在的异常行为：
            <span>{{abnormal_behaviors}}</span>
          </div>
          <el-button @click="to_realeach" style="padding: 5px 0">点击查看异常详情</el-button>
        </el-card>
        <el-card shadow="hover" style="height:342px;">
          <div slot="header" class="clearfix">
            <span>历史全部异常分类</span>
          </div>序列号加一攻击
          <el-progress :percentage="a_radio[0]" color="#42b983"></el-progress>配置异常
          <el-progress :percentage="a_radio[1]" color="#f1e05a"></el-progress>LSR报文伪造攻击
          <el-progress :percentage="a_radio[2]" color="#4169E1"></el-progress>最大年龄攻击
          <el-progress :percentage="a_radio[3]" color="#f56c6c"></el-progress>伪装攻击
          <el-progress :percentage="a_radio[4]" color="#FF1493"></el-progress>最大序列号攻击
          <el-progress :percentage="a_radio[5]" color="#0200a0"></el-progress>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-row :gutter="20" class="mgb20">
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{padding: '0px'}">
              <div class="grid-content grid-con-1">
                <i class="el-icon-tickets grid-con-icon"></i>
                <div class="grid-cont-right">
                  <div class="grid-num">{{all_router_num}}</div>
                  <div>路由器总数</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{padding: '0px'}">
              <div class="grid-content grid-con-2">
                <i class="el-icon-tickets grid-con-icon"></i>
                <div class="grid-cont-right">
                  <div class="grid-num">{{online_router_num}}</div>
                  <div>路由器在线数</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{padding: '0px'}">
              <div class="grid-content grid-con-3">
                <i class="el-icon-tickets grid-con-icon"></i>
                <div class="grid-cont-right">
                  <div class="grid-num">{{danger_router_num}}</div>
                  <div>危险路由器数</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        <el-card shadow="hover" style="height:553px;">
          <div slot="header" class="clearfix">
            <span>最近一小时路由拓扑</span>
          </div>
          <div class="tuopudiv">
            <div class="tuopu" id="tp" style="height: 435px;,width: 900px" ref="myEchart"></div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-card shadow="hover" :body-style="{padding: '0px'}">
        <div slot="header" class="clearfix">
          <span>历史全部异常记录</span>
          <el-button @click="to_realattack" style="float: right; padding: 5px 0">点击查看各异常事件</el-button>
        </div>
        <el-table
            :data="tableData"
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
          <el-table-column prop="type" label="关键风险异常" align="center"></el-table-column>
          <el-table-column prop="grade" label="风险威胁等级" align="center"></el-table-column>
        </el-table>
      </el-card>
    </el-row>
  </div>
</template>

<script>
import Schart from 'vue-schart';
import axios from '../../api/axios'
import bus from '../common/bus';
import echarts from 'echarts';
export default {
  name: 'real_global',
  data() {
    return {
      abnormal_routers: [],
      abnormal_behaviors: [],
      status: '',
      tableData: [],
      a_radio : [],
      all_router_num: 0,
      online_router_num: 0,
      danger_router_num: 0,
      nodes: [{
        'name': 'Router-1',
        category: 0,
        draggable: true,
        symbolSize: 40
      },{
        name: 'Router-2',
        category: 0,
        draggable: true,
      },{
        name: 'Router-3',
        category: 0,
      },{
        name: 'Router-4',
        category: 1,
      },{
        name: 'Router-5',
        category: 0,
      },{
        name: 'Router-6',
        category: 0,
      },{
        name: 'Router-7',
        category: 0,
      },{
        name: 'Router-8',
        category: 0,
      },{
        name: 'Router-9',
        category: 0,
      },{
        name: 'Router-10',
        category: 0,
      }],
      links: []
    };
  },
  components: {
    Schart
  },
  computed: {
    role() {
      return this.name === 'admin' ? '超级管理员' : '普通用户';
    },
    get_status_pic(){
      return this.status === 'normal' ? require("../../assets/img/normal.png") : require('../../assets/img/abnormal.png');
    },
    get_status_disc(){
      return this.status === 'normal' ? '路由系统正常' :'注意，最近一小时内系统存在异常风险！';
    }
  },
  created() {
    this.get_real_global_data()
  },
  // mounted() {
  //   this.initChart();
  // },
  methods: {
    get_real_global_data() {
      axios.Get({
        url : 'get_real_global_data',
        params: {},
        callback: (res) =>{
          let data = res.data
          this.abnormal_routers = data['abnormal_routers']
          this.status = data['status']
          this.abnormal_behaviors = data['abnormal_behaviors']
          this.tableData = data['tableData']
          this.danger_router_num =data['danger_router_num']
          this.all_router_num = data['all_router_num']
          this.online_router_num = data['online_router_num']
          this.a_radio = data['a_radio']
          this.nodes = data['nodes']
          this.links = data['links']
          this.initChart()
        }
      })
    },
    initChart(){
      this.tuopugraph = echarts.init(document.getElementById("tp"));
      this.tuopugraph.setOption({
        title: {
        },
        tooltip: {},
        animationDurationUpdate: 500,
        animationEasingUpdate: 'quinticInOut',
        label: {
          normal: {
            show: true,
            textStyle: {
              fontSize: 12
            },
          }
        },
        legend: {
          x: "right",
          show: true,
          data: ["正常路由器","异常路由器"]
        },
        series:[
          {
            type: 'graph',
            layout: 'circular',
            symbolSize: 45,
            focusNodeAdjacency: true,
            roam: 'move',
            categories:[{
              name: '正常路由器',
              itemStyle: {
                normal: {
                  color: "#009860",
                }
              }
            },{
              name: '异常路由器',
              itemStyle: {
                normal: {
                  color: "#FF6347",
                }
              }
            },{
              name: '主机',
              itemStyle: {
                normal: {
                  color: "#3592F",
                }
              }
            }],
            label: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 12
                },
              }
            },
            force: {
              repulsion: 1000
            },
            edgeSymbolSize: [4, 50],
            edgeLabel: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 10
                },
                formatter: "{c}"
              }
            },
            data: this.nodes,
            links: this.links,
            lineStyle: {
              normal: {
                opacity: 0.9,
                width: 1,
                curveness: 0
              }
            }
          }
        ],
        grid:{
          containLabel: true
        }
      })
    },
    to_realeach(){
      this.$router.push('/realeach')
    },
    to_realattack(){
      this.$router.push('/realattack')
    }
    // handleListener() {
    //     bus.$on('collapse', this.handleBus);
    //     // 调用renderChart方法对图表进行重新渲染
    //     window.addEventListener('resize', this.renderChart);
    // },
    // handleBus(msg) {
    //     setTimeout(() => {
    //         this.renderChart();
    //     }, 200);
    // },
    // renderChart() {
    //     this.$refs.bar.renderChart();
    //     this.$refs.line.renderChart();
    // }
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

.user-info {
  display: flex;
  align-items: center;
  padding-bottom: 40px;
  border-bottom: 2px solid #ccc;
  margin-bottom: 20px;
}

.user-avator {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

.user-info-cont {
  padding-left: 50px;
  flex: 1;
  font-size: 14px;
  color: #999;
}

.user-info-cont div:first-child {
  font-size: 30px;
  color: #222;
}

.user-info-list {
  font-size: 14px;
  color: #999;
  line-height: 25px;
}

.user-info-list span {
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
  width: 100%;
  height: 300px;
}
.table {
  width: 100%;
  font-size: 14px;
}
</style>
