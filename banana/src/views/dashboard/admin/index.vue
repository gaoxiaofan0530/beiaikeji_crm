<template>
  <div class="dashboard-editor-container">
    <github-corner class="github-corner" />

    <panel-group @handleSetLineChartData="handleSetLineChartData" />

    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <line-chart :chart-data="lineChartData" />
    </el-row>

    <!-- <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <raddar-chart />
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <pie-chart />
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <bar-chart />
        </div>
      </el-col>
    </el-row> -->

    <el-row :gutter="8">
      <el-col
        :xs="{span: 24}"
        :sm="{span: 24}"
        :md="{span: 24}"
        :lg="{span: 12}"
        :xl="{span: 12}"
        style="padding-right:8px;margin-bottom:30px;width:100%"
      >
        <transaction-table />
      </el-col>
      <!-- <el-col
        :xs="{span: 24}"
        :sm="{span: 12}"
        :md="{span: 12}"
        :lg="{span: 6}"
        :xl="{span: 6}"
        style="margin-bottom:30px;"
      >
        <todo-list />
      </el-col>
      <el-col
        :xs="{span: 24}"
        :sm="{span: 12}"
        :md="{span: 12}"
        :lg="{span: 6}"
        :xl="{span: 6}"
        style="margin-bottom:30px;"
      >
        <box-card />
      </el-col> -->
    </el-row>
  </div>
</template>

<script>
import GithubCorner from "@/components/GithubCorner";
import PanelGroup from "./components/PanelGroup";
import LineChart from "./components/LineChart";
import RaddarChart from "./components/RaddarChart";
import PieChart from "./components/PieChart";
import BarChart from "./components/BarChart";
import TransactionTable from "./components/TransactionTable";
import TodoList from "./components/TodoList";
import BoxCard from "./components/BoxCard";
import Utils from '../../../assets/js/util.js'


var dataArr = [];
var data = new Date();
var year = data.getFullYear();
data.setMonth(data.getMonth() + 1, 1); //获取到当前月份,设置月份
for (var i = 0; i < 12; i++) {
  data.setMonth(data.getMonth() - 1); //每次循环一次 月份值减1
  var m = data.getMonth() + 1;
  m = m < 10 ? "0" + m : m;
  dataArr.push(data.getFullYear() + "-" + m);
}
dataArr = dataArr.reverse();
var newVisitis_year = [];
var messages_year = [];
var purchases_year = [];
var shoppings_year = [];
// this.axios
//   .get("http://127.0.0.1:8000/app/get_performance_this_year/", {
//     params: {
//       now_data_list:dataArr
//     },
//   })
//   .then((body) => {
//     console.log(body.data.data);
// });
// var d = new Date();
// var year2 = d.getFullYear()
// var month2 = d.getMonth() + 1
// month2 = month2 < 10 ? "0" + month2 : month2;
// var str = d.getFullYear()+"-"+(d.getMonth()+1)
const lineChartData = {
  purchases: {
    expectedData: newVisitis_year,
    dataArr,
    name:'yeji'
  },
  messages: {
    expectedData: [200, 192, 120, 144, 160, 130, 140],
    actualData: [180, 160, 151, 106, 145, 150, 130],
    dataArr,
    name:'qiandan'
  },
  newVisitis: {
    expectedData: [80, 100, 121, 104, 105, 90, 100],
    actualData: [120, 90, 100, 138, 142, 130, 130],
    dataArr,
    name:'xiaoshou'
  },
  shoppings: {
    expectedData: [130, 140, 141, 142, 145, 150, 160],
    actualData: [120, 82, 91, 154, 162, 140, 130],
    dataArr,
    name:'xiaoshouzu'
  },
};

export default {
  name: "DashboardAdmin",
  components: {
    GithubCorner,
    PanelGroup,
    LineChart,
    RaddarChart,
    PieChart,
    BarChart,
    TransactionTable,
    TodoList,
    BoxCard,
  },
  mounted() {
    Utils.$on('demo3', function (msg) {
      this.axios
          .get("http://127.0.0.1:8000/app/select_new_date/", {
            params: {
              now_data: msg,
            },
          })
          .then((body) => {
              lineChartData.purchases.dataArr = body.data.data
              lineChartData.messages.dataArr = body.data.data
              lineChartData.newVisitis.dataArr = body.data.data
              lineChartData.shoppings.dataArr = body.data.data
          });
    })
  },
  data() {
    return {
      lineChartData: lineChartData.purchases,
    };
  },
  methods: {
    handleSetLineChartData(type) {
      this.lineChartData = lineChartData[type];
    },
  },
};
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

  .github-corner {
    position: absolute;
    top: 0px;
    border: 0;
    right: 0;
  }

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

@media (max-width: 1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
