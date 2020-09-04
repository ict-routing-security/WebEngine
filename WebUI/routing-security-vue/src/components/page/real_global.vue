<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card shadow="hover" class="mgb20" style="height:252px;">
          <div class="user-info">
            <img :src="get_status_pic" class="user-avator" alt />
            <div class="user-info-cont">
              <div class="user-info-name">{{get_status_disc}}</div>
            </div>
          </div>
          <div class="user-info-list">
            可能的异常路由器：
            <span>{{abnormal_routers_test}}</span>
          </div>
          <div class="user-info-list">
            可能存在的异常行为：
            <span>序列号加一攻击</span>
          </div>
        </el-card>
        <el-card shadow="hover" style="height:332px;">
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
        <el-card shadow="hover" style="height:483px;">
          <div slot="header" class="clearfix">
            <span>路由拓扑</span>
            <el-button style="float: right; padding: 3px 0" type="text">刷新</el-button>
          </div>
          <img src="../../assets/img/tuopu.png" class="tuopu" alt />
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-card shadow="hover" :body-style="{padding: '0px'}">
        <div slot="header" class="clearfix">
          <span>历史异常记录</span>
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
export default {
  name: 'real_global',
  data() {
    return {
      abnormal_routers_test: [],
      abnormal_routers: [1,3,13],
      status: 'abnormal',
      name: localStorage.getItem('ms_username'),
      tableData: [{
        no: '1',
        date:'2020-8-21',
        time: '23:13',
        ID: '12',
        type: '序列号加一攻击',
        grade: '3'
      },
        {
          no: '2',
          date:'2020-8-21',
          time: '23:23',
          ID: '12',
          type: '伪装攻击',
          grade: '2'
        },
        {
          no: '3',
          date:'2020-8-21',
          time: '23:23',
          ID: '12',
          type: '伪装攻击',
          grade: '2'
        },
        {
          no: '4',
          date:'2020-8-21',
          time: '23:23',
          ID: '12',
          type: '伪装攻击',
          grade: '2'
        },
        {
          no: '5',
          date:'2020-8-21',
          time: '00:23',
          ID: '12',
          type: '伪装攻击',
          grade: '2'
        },
        {
          no: '6',
          date:'2020-8-22',
          time: '09:29',
          ID: '12',
          type: '伪装攻击',
          grade: '2'
        }],
      data: [
        {
          name: '2018/09/04',
          value: 1083
        },
        {
          name: '2018/09/05',
          value: 941
        },
        {
          name: '2018/09/06',
          value: 1139
        },
        {
          name: '2018/09/07',
          value: 816
        },
        {
          name: '2018/09/08',
          value: 327
        },
        {
          name: '2018/09/09',
          value: 228
        },
        {
          name: '2018/09/10',
          value: 1065
        }
      ],
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
  created() {
    this.get_abnormal_routers()
  },
  methods: {
    get_abnormal_routers() {
      axios.Get({
        url : 'get_abnormal_routers',
        params: {},
        callback: (res) =>{
          let data = res.data
          this.abnormal_routers_test = data['abnormal_routers']
        }
      })
    },
    changeDate() {
      const now = new Date().getTime();
      this.data.forEach((item, index) => {
        const date = new Date(now - (6 - index) * 86400000);
        item.name = `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`;
      });
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

.tuopu {
  width: 600px;
  height: 400px;
  border-radius: 0%;
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
