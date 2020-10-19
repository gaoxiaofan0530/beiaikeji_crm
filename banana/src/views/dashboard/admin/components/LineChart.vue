<template>
  <div id="main" :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from "echarts";
require("echarts/theme/macarons"); // echarts theme
import resize from "./mixins/resize";
import Utils from "../../../../assets/js/util.js";

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: "chart",
    },
    width: {
      type: String,
      default: "100%",
    },
    height: {
      type: String,
      default: "350px",
    },
    autoResize: {
      type: Boolean,
      default: true,
    },
    chartData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      chart: null,
      dataArrd: "",
    };
  },
  watch: {
    chartData: {
      deep: true,
      handler(val) {
        this.setOptions(val);
      },
    },
  },
  mounted() {
    Utils.$on("demo2", function (msg) {
      console.log("demo2", msg);
      this.dataArrd = msg;
      this.setOptions();
    });
    this.$nextTick(() => {
      this.initChart();
    });
  },
  beforeDestroy() {
    if (!this.chart) {
      return;
    }
    this.chart.dispose();
    this.chart = null;
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, "macarons");
      this.setOptions(this.chartData);
      console.log("chartData", this.chartData);
    },
    setOptions({ expectedData, actualData, dataArr, name } = {}) {
      if (name == "yeji") {
        console.log("this.dataArrd", dataArr);
        this.axios
          .get("http://127.0.0.1:8000/app/get_performance_this_year/", {
            params: {
              now_data_list: JSON.stringify(dataArr),
            },
          })
          .then((body) => {
            expectedData = body.data.data;
            this.chart.setOption({
              backgroundColor: "#ffffff",
              title: {
                text: null,
                left: "center",
                top: "49%",
                textStyle: {
                  fontSize: 12,
                  color: "#3C4353",
                  fontStyle: "normal",
                  fontWeight: "200",
                  fontFamily: "PingFangSC-Regular,PingFang SC;",
                },
              },
              tooltip: {
                trigger: "axis",
                axisPointer: {
                  // 坐标轴指示器，坐标轴触发有效
                  type: "shadow", // 默认为直线，可选为：'line' | 'shadow'
                },
              },
              grid: {
                top: "80",
                left: "3%",
                right: "4%",
                bottom: "3%",
                containLabel: true,
              },
              xAxis: [
                {
                  type: "category",
                  axisTick: {
                    show: false,
                  },
                  data: dataArr,
                },
              ],
              yAxis: [
                {
                  type: "value",
                  axisLine: {
                    show: false,
                  },
                  axisTick: {
                    show: false,
                  },
                  axisLabel: {
                    show: false,
                    formatter: "{value}",
                  },
                  splitLine: {
                    show: false,
                  },
                },
              ],
              series: [
                {
                  name: "业绩",
                  type: "bar",
                  barWidth: 20,
                  label: {
                    show: true,
                    position: "top",
                    textStyle: {
                      color: "#000000",
                    },
                  },
                  itemStyle: {
                    normal: {
                      color: function (params) {
                        //展示正值的柱子，负数设为透明
                        let colorArr =
                          params.value > 0
                            ? ["#FF9A22", "#FFD56E"]
                            : ["rgba(0,0,0,0)", "rgba(0,0,0,0)"];
                        return new echarts.graphic.LinearGradient(
                          0,
                          0,
                          0,
                          1,
                          [
                            {
                              offset: 0,
                              color: colorArr[0], // 0% 处的颜色
                            },
                            {
                              offset: 1,
                              color: colorArr[1], // 100% 处的颜色
                            },
                          ],
                          false
                        );
                      },
                      barBorderRadius: [30, 30, 0, 0],
                    },
                  },
                  data: expectedData,
                },
              ],
            });
          });
      } else if (name == "qiandan") {
        if (this.dataArr == "") {
          this.dataArr == this.dataArr;
        }
        this.axios
          .get("http://127.0.0.1:8000/app/get_qiandan_this_year/", {
            params: {
              now_data_list: JSON.stringify(dataArr),
            },
          })
          .then((body) => {
            expectedData = body.data.data;
            this.chart.setOption({
              title: {
                text: "",
                left: "center",
                top: "49%",
              },
              xAxis: {
                data: dataArr,
                boundaryGap: false,
                axisTick: {
                  show: false,
                },
              },
              grid: {
                left: 10,
                right: 10,
                bottom: 20,
                top: 30,
                containLabel: true,
              },
              tooltip: {
                trigger: "axis",
                axisPointer: {
                  type: "cross",
                },
                padding: [5, 10],
              },
              yAxis: {
                axisTick: {
                  show: false,
                },
              },
              legend: {
                data: ["expected"],
              },
              series: [
                {
                  name: "签单量",
                  itemStyle: {
                    normal: {
                      color: "#FF005A",
                      lineStyle: {
                        color: "#FF005A",
                        width: 2,
                      },
                    },
                  },
                  smooth: true,
                  type: "line",
                  data: expectedData,
                  animationDuration: 2800,
                  animationEasing: "cubicInOut",
                },
              ],
            });
          });
      } else if (name == "xiaoshou") {
        if (this.dataArr == "") {
          this.dataArr == dataArr;
        }
        this.axios
          .get("http://127.0.0.1:8000/app/get_xiaoshou_this_year/", {
            params: {
              now_data_list: JSON.stringify(dataArr),
            },
          })
          .then((body) => {
            expectedData = body.data.name;
            var money = body.data.money;
            var myChart = echarts.init(document.getElementById("main"));
            this.chart.setOption({
              title: {
                text: null,
                left: "center",
                top: "49%",
                textStyle: {
                  fontSize: 16,
                  color: "#3C4353",
                  fontStyle: "normal",
                  fontWeight: "400",
                  fontFamily: "PingFangSC-Regular,PingFang SC;",
                },
              },
              xAxis: {
                data: expectedData,
                boundaryGap: false,
                axisTick: {
                  show: false,
                },
              },
              grid: {
                trigger: "axis",
                axisPointer: {
                  type: "cross",
                },
                padding: [5, 10],
              },
              yAxis: {
                axisTick: {
                  show: false,
                },
              },
              legend: {
                data: ["expected"],
              },
              tooltip: {
                trigger: "item",
                formatter: "{a} <br/>{b} : {c} ({d}%)",
              },
              /* legend: {
					left: 'center',
					top: 'bottom',
					data: ['rose1', 'rose2', 'rose3', 'rose4', 'rose5', 'rose6', 'rose7', 'rose8']
				}, */ backgroundColor:
                "#fff",
              color: [
                "#2ec7c9",
                "#b6a2de",
                "#5ab1ef",
                "#ffb980",
                "#d87a80",
                "#8d98b3",
                "#FFEA01",
                "#B8D07C",
                "#fca4bb",
                "#dc69aa",
                "#07a2a4",
                "#9a7fd1",
                "#588dd5",
                "#f5994e",
                "#c05050",
                "#59678c",
                "#c9ab00",
                "#7eb00a",
                "#6f5553",
                "#c14089",
              ],
              tooltip: [
                {
                  trigger: "item",
                  formatter: "{a} <br/>{b}: {c} ({d}%)",
                },
              ],
              series: [
                {
                  name: "详情",
                  type: "pie",
                  radius: ["45%", "55%"],
                  data: body.data.money,
                  labelLine: {
                    normal: {
                      length: 20,
                      length2: 140,
                      lineStyle: {
                        color: "#e6e6e6",
                      },
                    },
                  },
                  label: {
                    normal: {
                      formatter: (params) => {
                        return (
                          "{icon|●}{name|" +
                          params.name +
                          "}{percent|" +
                          params.percent.toFixed(1) +
                          "%}{value|" +
                          params.value +
                          "}"
                        );
                      },
                      padding: [0, -130, 25, -130],
                      rich: {
                        color: "#333",
                        icon: {
                          fontSize: 16,
                        },
                        name: {
                          fontSize: 14,
                          padding: [0, 5, 0, 5],
                          color: "#666666",
                        },
                        percent: {
                          color: "#333",
                          padding: [0, 5, 0, 0],
                        },
                        value: {
                          fontSize: 16,
                          fontWeight: "bold",
                          color: "#333333",
                        },
                      },
                    },
                  },
                },
              ],
            });
          });
      } else if (name == "xiaoshouzu") {
        if (this.dataArr == "") {
          this.dataArr == dataArr;
        }
        this.axios
          .get("http://127.0.0.1:8000/app/get_xiaoshou_group_this_year/", {
            params: {
              now_data_list: JSON.stringify(dataArr),
            },
          })
          .then((body) => {
            expectedData = body.data.name;
            var money = body.data.money;
            var myChart = echarts.init(document.getElementById("main"));
            this.chart.setOption({
              title: {
                text: "总业绩" + body.data.count,
                left: "center",
                top: "49%",
                textStyle: {
                  fontSize: 16,
                  color: "#3C4353",
                  fontStyle: "normal",
                  fontWeight: "400",
                  fontFamily: "PingFangSC-Regular,PingFang SC;",
                },
              },
              xAxis: {
                data: expectedData,
                boundaryGap: false,
                axisTick: {
                  show: false,
                },
              },
              grid: {
                trigger: "axis",
                axisPointer: {
                  type: "cross",
                },
                padding: [5, 10],
              },
              yAxis: {
                axisTick: {
                  show: false,
                },
              },
              legend: {
                data: ["expected"],
              },
              tooltip: {
                trigger: "item",
                formatter: "{a} <br/>{b} : {c} ({d}%)",
              },
              /* legend: {
					left: 'center',
					top: 'bottom',
					data: ['rose1', 'rose2', 'rose3', 'rose4', 'rose5', 'rose6', 'rose7', 'rose8']
				}, */ backgroundColor:
                "#fff",
              color: [
                "#2ec7c9",
                "#b6a2de",
                "#5ab1ef",
                "#ffb980",
                "#d87a80",
                "#8d98b3",
                "#FFEA01",
                "#B8D07C",
                "#fca4bb",
                "#dc69aa",
                "#07a2a4",
                "#9a7fd1",
                "#588dd5",
                "#f5994e",
                "#c05050",
                "#59678c",
                "#c9ab00",
                "#7eb00a",
                "#6f5553",
                "#c14089",
              ],
              tooltip: [
                {
                  trigger: "item",
                  formatter: "{a} <br/>{b}: {c} ({d}%)",
                },
              ],
              series: [
                {
                  name: "详情",
                  type: "pie",
                  radius: ["45%", "55%"],
                  data: body.data.money,
                  labelLine: {
                    normal: {
                      length: 20,
                      length2: 140,
                      lineStyle: {
                        color: "#e6e6e6",
                      },
                    },
                  },
                  label: {
                    normal: {
                      formatter: (params) => {
                        return (
                          "{icon|●}{name|" +
                          params.name +
                          "}{percent|" +
                          params.percent.toFixed(1) +
                          "%}{value|" +
                          params.value +
                          "}"
                        );
                      },
                      padding: [0, -130, 25, -130],
                      rich: {
                        color: "#333",
                        icon: {
                          fontSize: 16,
                        },
                        name: {
                          fontSize: 14,
                          padding: [0, 5, 0, 5],
                          color: "#666666",
                        },
                        percent: {
                          color: "#333",
                          padding: [0, 5, 0, 0],
                        },
                        value: {
                          fontSize: 16,
                          fontWeight: "bold",
                          color: "#333333",
                        },
                      },
                    },
                  },
                },
              ],
            });
          });
      }
    },
  },
};
</script>
