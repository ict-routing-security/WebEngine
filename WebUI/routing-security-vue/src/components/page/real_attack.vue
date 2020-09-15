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
import axios from '@/api/axios';
export default {
  name: 'real_attack',
  data() {
    return {
      anomalys: [
        {
          name: '序列号加一攻击',
          disc: '攻击路由器收到受害路由器的LSU(Link State Update，链路状态更新)报文后，将其序号加一或者更多，重新计算校验和发送出去。受害路由器收到此错误报文后不断发送具有更大链路序号的数据分组去纠正错误信息，导致网络带宽消耗。\n',
          tableData: []
        },
        {
          name: '配置异常',
          disc: 'OSPF协议邻居节点之间共有参数不匹配，造成邻居节点失联，相应链路断路。若断路的是冗余链路，则不容易被发现，因为整个网络仍然联通。然而冗余链路断路会使其他链路的负载加重，最终可能导致网络拥塞。\n',
          tableData: []
        },
        {
          name: 'LSR报文伪造攻击',
          disc: '攻击者向目标路由器（受害者路由器）高速发送LSR（Link State Request，链路状态请求）报文，使得目标路由器不断响应LSR报文，发送LSU报文，大量的CPU资源被占用，导致网络带宽消耗。\n',
          tableData: []
        },
        {
          name: '最大年龄攻击',
          disc: '攻击路由器收到受害路由器的LSU报文后，将其年龄设为最大值，重新计算校验和发送出去。受害路由器收到错误信息后会不断发送具有更大序号的数据分组去纠正错误信息，占用CPU资源，消耗网络带宽。\n' +
              '同样利用受害路由器的反击机制。\n',
          tableData: []
        },
        {
          name: '伪装攻击',
          disc: '攻击路由器收到受害路由器的LSU后，修改将其包含的拓扑信息，重新计算校验和发送出去。由于攻击路由器成功伪装，使得其他路由器信任并接受错误拓扑信息，造成网络中产生路由环路、长路径路由等。\n'+
              '利用提前触发受害路由器反击机制实现伪装——攻击路由器预先发送一个内容随意的trigger LSU。受害路由器收到此trigger LSU后触发反击机制发送反击LSU，在此反击LSU到达其他路由器之前，攻击路由器会发送包含错误拓扑的disguised LSU，并控制时间确保它先于反击LSU到达其他路由器，使得其他路由器接受错误拓扑信息。\n',
          tableData: []
        },
        {
          name: '最大序列号攻击',
          disc: '攻击路由器收到受害路由器的LSU报文后，将其序号设为最大值0x7FFFFFFF，重新计算校验和发送出去。受害路由器收到此错误报文后会将其age字段设为MaxAge(3600)并泛洪出去。其他路由器收到最大年龄报文时删除路由表中相应表项，造成节点之间的临时失联。\n',
          tableData: []
        },
      ],
    };
  },
  created() {
    this.get_real_attack_data()
  },
  components: {
    Schart
  },
  computed: {
  },
  methods: {
    get_real_attack_data() {
      axios.Get({
        url : 'get_real_attack_data',
        params: {},
        callback: (res) =>{
          let data = res.data
          this.anomalys[0].tableData = data['attack0']
          this.anomalys[1].tableData = data['attack1']
          this.anomalys[2].tableData = data['attack2']
          this.anomalys[3].tableData = data['attack3']
          this.anomalys[4].tableData = data['attack4']
          this.anomalys[5].tableData = data['attack5']
        }
      })
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
