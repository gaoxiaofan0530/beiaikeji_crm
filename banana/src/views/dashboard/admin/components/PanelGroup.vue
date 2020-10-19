<template>
  <div @click="noclick">
    <el-date-picker
        v-model="now_data"
        ref="chooseKpi19"
        type="monthrange"
        align="right"
        unlink-panels
        range-separator="-"
        start-placeholder="开始月份"
        end-placeholder="结束月份"
        @change="formatTime"
        :picker-options="pickerOptions"
        @blur="chooseKpi19"
        @focus="datePicker_click"
    ></el-date-picker>
    <el-row :gutter="40" class="panel-group">
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel" @click="handleSetLineChartData('purchases')">
          <div class="card-panel-icon-wrapper icon-money">
            <svg-icon icon-class="money" class-name="card-panel-icon" />
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">业绩</div>
            <div class="card-panel-num">{{ money }}</div>
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">同比</div>
            <div v-if="float.includes('-') === true">
              <div class="card-panel-num" style="color:#FF0000">{{ float }}</div>
            </div>
            <div v-else>
              <div class="card-panel-num" style="color:#008000">+{{ float }}</div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel" @click="handleSetLineChartData('messages')">
          <div class="card-panel-icon-wrapper icon-message">
            <svg-icon icon-class="skill" class-name="card-panel-icon" />
          </div>
          <div class="card-panel-description2">
            <div class="card-panel-text2">新签</div>
            <div class="card-panel-num2">{{ xinqian_number_orders }}</div>
          </div>
          <div class="card-panel-description2">
            <div class="card-panel-text2">续约</div>
            <div class="card-panel-num2">{{ xuyue_number_orders }}</div>
          </div>
          <div class="card-panel-description2">
            <div class="card-panel-text2">断约</div>
            <div class="card-panel-num2">{{ number_orders }}</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel" @click="handleSetLineChartData('newVisitis')">
          <div class="card-panel-icon-wrapper icon-people">
            <svg-icon icon-class="people" class-name="card-panel-icon" />
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">👍</div>
            <div class="card-panel-num">{{ top_name }}</div>
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">￥</div>
            <div class="card-panel-num">{{ top_money }}</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel" @click="handleSetLineChartData('shoppings')">
          <div class="card-panel-icon-wrapper icon-shopping">
            <svg-icon icon-class="peoples" class-name="card-panel-icon" />
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">👍</div>
            <div class="card-panel-num">{{ top_group_name }}</div>
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">￥</div>
            <div class="card-panel-num">{{ top_group_money }}</div>
          </div>
        </div>
      </el-col>
    </el-row>
    <!-- <el-table :data="tableData" style="width: 100%;padding-top: 15px;">
    <el-table-column prop="order_date" label="最新签单" width="180"></el-table-column>
    <el-table-column prop="order_contract_sales" label width="180"></el-table-column>
    <el-table-column prop="sign_contract_shop" label></el-table-column>
    <el-table-column prop="shop_cooperation_duration" label></el-table-column>
    <el-table-column prop="order_amount" label></el-table-column>
    <el-table-column prop="tags" label></el-table-column>
    </el-table> -->
  </div>
</template>

<script>
import CountTo from "vue-count-to";
import Utils from "../../../../assets/js/util.js";
import request from '@/utils/request'
import global from '@/store/modules/user'

export default {
  name: "DataList",
  data() {
    return {
      now_data: "",
      old_data: "",
      money: 0,
      float: "",
      top_name: "",
      month_data: "",
      top_money: "",
      top_group_name: "销售一组",
      top_group_money: "",
      number_orders: 1,
      xinqian_number_orders: 1,
      xuyue_number_orders: 1,
      now_date_data: "",
      roles: '',
      count:1,
      date: "",
      pickerOptions: {
        shortcuts: [
          {
            text: "最近一个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 10);
              picker.$emit("pick", [start, end]);
            },
          },
          {
            text: "最近三个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 70);
              picker.$emit("pick", [start, end]);
            },
          },{
            text: "最近半年",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 160);
              picker.$emit("pick", [start, end]);
            },
          },{
            text: "最近一年",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 345);
              picker.$emit("pick", [start, end]);
            },
          }
        ],
        // disabledDate(time) {
        //     let curDate = (new Date()).getTime();
        //     let three = 90 * 24 * 3600 * 1000;
        //     let threeMonths = curDate - three;
        //     return time.getTime() > Date.now() || time.getTime() < threeMonths;;
        // }
      },
    };
  },
  created: function () {
    // const end = new Date();
    // const start = new Date();
    // start.setTime(start.getTime() - 3600 * 1000 * 24 * 345);
    // picker.$emit("pick", [start, end]);
    this.roles = global.state['avatar']
    // 当前年月
    var now = new Date();
    var year = now.getFullYear()-1; // 得到年份
    var month = now.getMonth() + 2;
    month = month.toString();
    if (month.length == 1) {
      month = "0" + month;
    }
    this.now_data = year.toString() + "-" + month.toString();
    // this.month_data=this.now_data
    // 上一个月年月
    now.setMonth(now.getMonth() - 1);
    var old_year = now.getFullYear() -1; // 得到年份
    var old_month = now.getMonth() + 2;
    old_month = old_month.toString();
    if (old_month.length == 1) {
      old_month = "0" + old_month;
    }
    this.old_data = old_year.toString() + "-" + old_month.toString();
    var now = new Date();
    var year_now = now.getFullYear(); // 得到年份
    var month_now = now.getMonth();
    month_now = month_now.toString();
    if (month_now.length == 1) {
      month_now = "0" + month_now;
    }
    var now_data2 = year_now.toString() + "-" + month_now.toString();
    var a = this.getNextMonth2(now_data2 + "-01");
    this.now_data = [this.now_data, a];
    var now = new Date();
    var year_old = now.getFullYear(); // 得到年份
    var month_old = now.getMonth();
    month_old = month_old.toString();
    if (month_old.length == 1) {
      month_old = "0" + month_old;
    }
    var now_data2 = year_old.toString() + "-" + month_old.toString();
    var b = this.getNextMonth2(now_data2 + "-01");
    this.old_data = [this.old_data, b];
    this.get_performance_this_month();
    this.get_top_one();
    this.get_number_orders();
    this.get_top_group();
    this.send_data();
    // this.formatTime()
  },
  methods: {
    noclick(){
      console.log(this.count)
      if (this.count == 1){
        this.count = 3
      }else if (this.count == 3){
        this.$refs.chooseKpi19.hidePicker();
        this.count = 1
      }
    },
    datePicker_click(){
      this.count = 1
    },
    chooseKpi19() {
      this.$refs.chooseKpi19.blur();
    },
    getNextMonth(date) {
      var arr = date.split("-");
      var year = arr[0]; //获取当前日期的年份
      var month = arr[1]; //获取当前日期的月份
      var day = arr[2]; //获取当前日期的日
      var days = new Date(year, month, 0);
      days = days.getDate(); //获取当前日期中月的天数
      var year2 = year;
      var month2 = parseInt(month) - 1;
      if (month2 == 0) {
        year2 = parseInt(year2) - 1;
        month2 = 12;
      }
      var day2 = day;
      var days2 = new Date(year2, month2, 0);
      days2 = days2.getDate();
      if (day2 > days2) {
        day2 = days2;
      }
      if (month2 < 10) {
        month2 = "0" + month2;
      }
      var t2 = year2 + "-" + month2 + "-" + day2;
      return t2;
    },
    getNextMonth2(date) {
      var arr = date.split("-");
      var year = arr[0]; //获取当前日期的年份
      var month = arr[1]; //获取当前日期的月份
      var day = arr[2]; //获取当前日期的日
      var days = new Date(year, month, 0);
      days = days.getDate(); //获取当前日期中月的天数
      var year2 = year;
      var month2 = parseInt(month) + 1;
      if (month2 == 0) {
        year2 = parseInt(year2) + 1;
        month2 = 12;
      }
      var day2 = day;
      var days2 = new Date(year2, month2, 0);
      days2 = days2.getDate();
      if (day2 > days2) {
        day2 = days2;
      }
      if (month2 < 10) {
        month2 = "0" + month2;
      }
      var t2 = year2 + "-" + month2;
      return t2;
    },
    functionA() {
      var a = JSON.stringify(this.now_data);
      Utils.$emit("demo", a);
    },
    functionB() {
      var a = JSON.stringify(this.now_data);
      Utils.$emit("demo2", a);
    },
    functionC() {
      var a = JSON.stringify(this.now_data);
      Utils.$emit("demo3", a);
    },
    formatTime() {
      var year1 = this.now_data[0].getFullYear(); // 得到年份
      var month1 = this.now_data[0].getMonth() + 1;
      if (month1.toString().length == 1) {
        month1 = "0" + month1;
      }
      var year2 = this.now_data[1].getFullYear();
      var month2 = this.now_data[1].getMonth() + 1;
      if (month2.toString().length == 1) {
        month2 = "0" + month2;
      }
      this.now_data = [year1 + "-" + month1, year2 + "-" + month2];
      var a = this.getNextMonth(this.now_data[0].toString() + "-01").slice(
        0,
        7
      );
      var b = this.getNextMonth(this.now_data[1].toString() + "-01").slice(
        0,
        7
      );
      this.old_data = [a, b];
      console.log('123',this.now_data)
      console.log('456',this.old_data)
      this.get_performance_this_month();
      this.get_top_one();
      this.get_number_orders();
      this.get_top_group();
      this.functionA();
      this.functionC();
      this.functionB();
    },
    handleSetLineChartData(type) {
      this.$emit("handleSetLineChartData", type);
    },
    send_data() {
      this.axios
        .get("http://127.0.0.1:8000/app/send_data/")
        .then((res) => {})
        .catch(function (error) {
          this.loading = false;
        });
    },
    get_performance_this_month() {
      this.axios
        .get("http://127.0.0.1:8000/app/get_performance_this_month/", {
          params: {
            // 每页显示的条数
            now_data: JSON.stringify(this.now_data),
            // 显示第几页
            old_data: JSON.stringify(this.old_data),
          },
        })
        .then((res) => {
          this.money = res.data.now_money;
          this.float = res.data.float;
        })
        .catch(function (error) {
          this.loading = false;
        });
    },
    get_top_one() {
      this.axios
        .get("http://127.0.0.1:8000/app/get_top_one/", {
          params: {
            // 每页显示的条数
            now_data: JSON.stringify(this.now_data),
          },
        })
        .then((res) => {
          this.top_name = res.data.top_name;
          this.top_money = res.data.top_money;
        })
        .catch(function (error) {
          this.loading = false;
        });
    },
    get_number_orders() {
      this.axios
        .get("http://127.0.0.1:8000/app/get_number_orders/", {
          params: {
            // 每页显示的条数
            now_data: JSON.stringify(this.now_data),
          },
        })
        .then((res) => {
          this.number_orders = res.data.number_orders;
          this.xinqian_number_orders = res.data.xinqian_number_orders;
          this.xuyue_number_orders = res.data.xuyue_number_orders;
        })
        .catch(function (error) {
          this.loading = false;
        });
    },
    get_top_group() {
      this.axios
        .get("http://127.0.0.1:8000/app/get_top_group/", {
          params: {
            // 每页显示的条数
            now_data: JSON.stringify(this.now_data),
          },
        })
        .then((res) => {
          this.top_group_name = res.data.group_name;
          this.top_group_money = res.data.group_money;
        })
        .catch(function (error) {
          this.loading = false;
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.panel-group {
  margin-top: 18px;

  .card-panel-col {
    margin-bottom: 32px;
  }

  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);
    border-color: rgba(0, 0, 0, 0.05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-people {
        background: #40c9c6;
      }

      .icon-message {
        background: #36a3f7;
      }

      .icon-money {
        background: #f4516c;
      }

      .icon-shopping {
        background: #34bfa3;
      }
    }

    .icon-people {
      color: #40c9c6;
    }

    .icon-message {
      color: #36a3f7;
    }

    .icon-money {
      color: #f4516c;
    }

    .icon-shopping {
      color: #34bfa3;
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-icon {
      float: left;
      font-size: 48px;
    }

    .card-panel-description {
      // float: inherit;
      // float: right;
      font-weight: bold;
      // margin: 10px;
      margin: 20px;
      margin-right: 0px;
      margin-top: 30px;
      .card-panel-text {
        // float: right;
        line-height: 10px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-left: -15px;
      }

      .card-panel-num {
        margin-top: -16px;
        margin-right: 10px;
        float: right;
        font-size: 18px;
      }
    }
    .card-panel-description2 {
      // float: inherit;
      // float: right;
      font-weight: bold;
      // margin: 10px;
      margin: 20px;
      margin-right: 0px;
      .card-panel-text2 {
        // float: right;
        line-height: 10px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-left: -15px;
      }

      .card-panel-num2 {
        margin-top: -17px;
        margin-right: 10px;
        float: right;
        font-size: 18px;
      }
    }
  }
}

@media (max-width: 550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>
