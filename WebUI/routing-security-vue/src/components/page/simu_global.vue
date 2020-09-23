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
          <el-button @click="to_simueach" style="padding: 5px 0">点击查看异常详情</el-button>
        </el-card>
        <el-card shadow="hover" style="height:342px;">
          <div slot="header" class="clearfix">
            <span>历史异常分类</span>
          </div>序列号加一攻击
          <el-progress :percentage="71.3" color="#42b983"></el-progress>配置异常
          <el-progress :percentage="24.1" color="#f1e05a"></el-progress>LSR报文伪造攻击
          <el-progress :percentage="13.7"></el-progress>最大年龄攻击
          <el-progress :percentage="5.0" color="#f56c6c"></el-progress>伪装攻击
          <el-progress :percentage="500" color="#f96c7a"></el-progress>最大序列号攻击
          <el-progress :percentage="0.4" color="#0200a0"></el-progress>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-row :gutter="20" class="mgb20">
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{padding: '0px'}">
              <div class="grid-content grid-con-1">
                <i class="el-icon-tickets grid-con-icon"></i>
                <div class="grid-cont-right">
                  <div class="grid-num">1234</div>
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
                  <div class="grid-num">321</div>
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
                  <div class="grid-num">5000</div>
                  <div>危险路由器数</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        <el-card shadow="hover" style="height:553px;">
          <div slot="header" class="clearfix">
            <span>路由拓扑</span>
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
          <span>历史异常记录</span>
          <el-button @click="to_simuattack" style="float: right; padding: 5px 0">点击查看各异常事件</el-button>
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
  name: 'simu_global',
  data() {
    return {
      abnormal_routers: [12],
      abnormal_behaviors: ['序列号加一攻击','最大年龄攻击'],
      status: 'normal',
      tuopugraph :null,
      tableData: [{
        no: 1,
        date: '2020-9-10',
        time: '23:12:01',
        ID: 12,
        type: '序列号加一攻击',
        grade: 2
      },{
        no: 2,
        date: '2020-9-10',
        time: '23:13:01',
        ID: 12,
        type: '序列号加一攻击',
        grade: 2
      },{
        no: 3,
        date: '2020-9-10',
        time: '23:17:01',
        ID: 12,
        type: '最大年龄攻击',
        grade: 2
      }
      ],
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
      links: [
        {
          source: 4,
          target: 9,
          value: '连接'
        },
        {
          source: 3,
          target: 7,
          value: '连接'
        },{
          source: 4,
          target: 8,
          value: '连接'
        },{
        source: 0,
        target: 2,
        value: '连接'
      },{
        source: 0,
        target: 5,
        value: '连接'
      },{
        source: 0,
        target: 1,
        value: '连接'
      },{
        source: 5,
        target: 6,
        value: '连接'
      },{
        source: 6,
        target: 7,
        value: '连接'
      },{
        source: 7,
        target: 8,
        value: '连接'
      },{
        source: 8,
        target: 9,
        value: '连接'
      }]
    };
  },
  mounted() {
    this.initChart();
  },
  beforeDestroy() {
    if (!this.tuopugraph) {
      return;
    }
    this.tuopugraph.dispose();
    this.tuopugraph = null;
  },
  components: {
    Schart
  },
  computed: {
    get_status_pic(){
      return this.status === 'normal' ? require("../../assets/img/normal.png") : require('../../assets/img/abnormal.png');
    },
    get_status_disc(){
      return this.status === 'normal' ? '路由系统正常' :'注意，系统存在异常风险！';
    }
  },

  // created() {
  //     this.handleListener();
  //     this.changeDate();
  // },
  // activated() {
  //     this.handleListener();
  // },
  // deactivated() {
  //     window.removeEventListener('resize', this.renderChart);
  //     bus.$off('collapse', this.handleBus);
  // },
  methods: {
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
    to_simueach(){
      this.$router.push('/simueach')
    },
    to_simuattack(){
      this.$router.push('/simuattack')
    },
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
