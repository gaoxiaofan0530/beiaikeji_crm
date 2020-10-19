<template>
  <el-table :data="tableData" style="width: 100%;padding-top: 15px;">
    <el-table-column prop="order_date" label="最新签单" width="180"></el-table-column>
    <el-table-column prop="order_contract_sales" label width="180"></el-table-column>
    <el-table-column prop="sign_contract_shop" label></el-table-column>
    <el-table-column prop="shop_cooperation_duration" label></el-table-column>
    <el-table-column prop="order_amount" label></el-table-column>
    <el-table-column prop="tags" label></el-table-column>
  </el-table>
</template>

<script>
import { transactionList } from "@/api/remote-search";
import Utils from '../../../../assets/js/util.js'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        success: "success",
        pending: "danger",
      };
      return statusMap[status];
    },
    orderNoFilter(str) {
      return str.substring(0, 30);
    },
  },
  data() {
    return {
      list: null,
      tableData: [],
    };
  },
  created() {
    this.get_data2();
    this.fetchData();
  },
  mounted() {
    var that = this;
    Utils.$on('demo', function (msg) {
        that.get_data(msg);
    })
    this.$nextTick(() => {
      this.get_data();
    });
  },
  methods: {
    fetchData() {
      transactionList().then((response) => {
        this.list = response.data.items.slice(0, 8);
      });
    },
    get_data2(){
        var now = new Date();
        var year = now.getFullYear(); // 得到年份
        var month = now.getMonth() + 1;
        month = month.toString();
        if (month.length == 1) {
          month = "0" + month;
        }
        var now_data = year.toString() + "-" + month.toString();
        console.log('get_data2',now_data)
        this.axios
        .get("http://127.0.0.1:8000/app/select_order/", {
          params: {
            now_data: now_data,
            text:'1'
          }
        })
        .then((body) => {
          this.tableData = body.data.data;
        });
    },
    get_data(date) {
      var now = new Date();
      var year = now.getFullYear(); // 得到年份
      var month = now.getMonth() + 1;
      month = month.toString();
      if (month.length == 1) {
        month = "0" + month;
      }
      var now_data = year.toString() + "-" + month.toString();
      this.axios
      .get("http://127.0.0.1:8000/app/select_order/", {
        params: {
          now_data: date,
          text:'2'
        }
      })
      .then((body) => {
        this.tableData = body.data.data;
      });
      
    },
  },
};
</script>
