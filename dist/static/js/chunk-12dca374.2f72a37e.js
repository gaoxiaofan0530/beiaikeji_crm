(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-12dca374"],{"2de5":function(t,e,a){"use strict";var s=a("53a2"),i=a.n(s);i.a},"53a2":function(t,e,a){},"99ac":function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"dashboard-editor-container"},[a("el-date-picker",{attrs:{type:"month",placeholder:"选择月","value-format":"yyyy-MM"},on:{change:t.formatTime},model:{value:t.month_data,callback:function(e){t.month_data=e},expression:"month_data"}}),t._v(" "),"admin"===t.roles?a("span",[a("el-select",{attrs:{clearable:"",filterable:"",placeholder:"请选择"},on:{change:function(e){return t.xiaoshou_change(t.xiaoshou_value)}},model:{value:t.xiaoshou_value,callback:function(e){t.xiaoshou_value=e},expression:"xiaoshou_value"}},t._l(t.xiaoshou_options,(function(t){return a("el-option",{key:t.value,attrs:{label:t.label,value:t.value}})})),1)],1):t._e(),t._v(" "),a("el-row",{staticClass:"panel-group",attrs:{gutter:40}},[a("el-col",{staticClass:"card-panel-col",attrs:{xs:12,sm:12,lg:6}},[a("div",{staticClass:"card-panel",on:{click:function(e){return t.handleSetLineChartData("newVisitis")}}},[a("div",{staticClass:"card-panel-icon-wrapper icon-people"},[a("svg-icon",{attrs:{"icon-class":"money","class-name":"card-panel-icon"}})],1),t._v(" "),a("div",{staticClass:"card-panel-description"},[a("div",{staticClass:"card-panel-text"},[t._v("本月业绩")]),t._v(" "),a("div",{staticClass:"card-panel-num"},[t._v(t._s(t.table_simple_data))])]),t._v(" "),a("div",{staticClass:"card-panel-description"},[a("div",{staticClass:"card-panel-text"},[t._v("提成点")]),t._v(" "),a("span",{staticClass:"card-panel-num2"},[t._v("%")]),t._v(" "),a("div",{staticClass:"card-panel-num"},[t._v(t._s(t.commission_point))])]),t._v(" "),a("div",{staticClass:"card-panel-description"},[a("div",{staticClass:"card-panel-text"},[t._v("本月提成")]),t._v(" "),a("div",{staticClass:"card-panel-num"},[t._v(t._s(t.table_simple_data_signing))])])])]),t._v(" "),a("el-col",{staticClass:"card-panel-col",attrs:{xs:12,sm:12,lg:6}},[a("div",{staticClass:"card-panel",on:{click:function(e){return t.handleSetLineChartData("messages")}}},[a("div",{staticClass:"card-panel-icon-wrapper icon-message"},[a("svg-icon",{attrs:{"icon-class":"money","class-name":"card-panel-icon"}})],1),t._v(" "),a("div",{staticClass:"card-panel-description3"},[a("div",{staticClass:"card-panel-text"},[t._v("本月奖金")]),t._v(" "),a("div",{staticClass:"card-panel-num"},[t._v(t._s(t.last_month_service_bonus))]),t._v(" "),a("span",{staticClass:"card-panel-num"},[t._v("/")]),t._v(" "),a("div",{staticClass:"card-panel-num"},[t._v(t._s(t.month_service_bonus))])]),t._v(" "),a("div",{staticClass:"card-panel-description3"},[a("div",{staticClass:"card-panel-text"},[t._v("下月奖金")]),t._v(" "),a("div",{staticClass:"card-panel-num"},[t._v(t._s(t.next_month_service_bonus))]),t._v(" "),a("span",{staticClass:"card-panel-num"},[t._v("/")]),t._v(" "),a("div",{staticClass:"card-panel-num"},[t._v(t._s(t.next_get_month_service_bonus))])])])]),t._v(" "),a("el-col",{staticClass:"card-panel-col",attrs:{xs:12,sm:12,lg:6}},[a("div",{staticClass:"card-panel",on:{click:function(e){return t.handleSetLineChartData("purchases")}}},[a("div",{staticClass:"card-panel-icon-wrapper icon-money"},[a("svg-icon",{attrs:{"icon-class":"form","class-name":"card-panel-icon"}})],1),t._v(" "),a("div",{staticClass:"card-panel-description4"},[a("div",{staticClass:"card-panel-text"},[t._v("本月签单")]),t._v(" "),a("div",{staticClass:"card-panel-num"},[t._v(t._s(t.user))])])])]),t._v(" "),a("el-col",{staticClass:"card-panel-col",attrs:{xs:12,sm:12,lg:6}},[a("div",{staticClass:"card-panel",on:{click:function(e){return t.handleSetLineChartData("shoppings")}}},[a("div",{staticClass:"card-panel-icon-wrapper icon-shopping"},[a("svg-icon",{attrs:{"icon-class":"peoples","class-name":"card-panel-icon"}})],1),t._v(" "),a("div",{staticClass:"card-panel-description4"},[a("div",{staticClass:"card-panel-text"},[t._v("意向客户")]),t._v(" "),a("div",{staticClass:"card-panel-num"},[t._v(t._s(t.table_simple_new_all_data))])])])])],1),t._v(" "),a("el-row",{attrs:{gutter:12}},[a("el-col",{attrs:{span:8}},[a("el-card",[a("div",{staticClass:"card-fixed-header-db"},[t._v("\n          待办事项\n          "),a("el-select",{attrs:{filterable:"",placeholder:"请选择"},on:{change:function(e){return t.get_shop_name_todo()}},model:{value:t.todo_value,callback:function(e){t.todo_value=e},expression:"todo_value"}},t._l(t.todo_dict,(function(t){return a("el-option",{key:t.value,attrs:{label:t.label,value:t.value}})})),1)],1),t._v(" "),a("div",{staticClass:"box-card card-panel-col card-setting"},[void 0!==t.to_do&&t.to_do.length>0?a("div",t._l(t.to_do,(function(e,s){return a("div",{key:s,staticClass:"text item"},[a("el-card",{staticClass:"card-bottom",attrs:{shadow:"never"}},[a("div",{staticClass:"card-bottom-db"}),t._v("\n                "+t._s(e.shop_name)+"【"+t._s(e.project)+"】\n                "),a("el-button",{staticStyle:{padding:"1px"},attrs:{type:"danger",icon:"el-icon-check",circle:""},on:{click:function(e){return t.select(s)}}}),t._v(" "),a("div",{staticClass:"bottom clearfix"},[a("i",{staticClass:"el-icon-alarm-clock time"}),t._v(" "),a("time",{staticClass:"time"},[t._v("截止时间："+t._s(e.time))]),t._v(" "),a("class",{staticClass:"money"},[t._v("   ￥"+t._s(e.money))]),t._v(" "),"审核未通过"===e.status?a("class",[a("el-popover",{attrs:{placement:"top-start",width:"400",trigger:"hover"}},[a("el-input",{staticStyle:{width:"100%"},attrs:{label:"驳回原因",disabled:!0},model:{value:e.edit,callback:function(a){t.$set(e,"edit",a)},expression:"to_do.edit"}}),t._v(" "),a("class",{staticClass:"money",staticStyle:{color:"#f4516c"},attrs:{slot:"reference"},slot:"reference"},[t._v("   "+t._s(e.status))])],1)],1):a("class",[a("class",{staticClass:"money",staticStyle:{color:"#f4516c"}},[t._v("   "+t._s(e.status))])],1),t._v(" "),a("el-progress",{staticStyle:{width:"30%",float:"right",position:"relative",bottom:"-5px"},attrs:{percentage:e.schedule,"show-text":!1}})],1)],1)],1)})),0):a("div",[a("div",{staticClass:"div2"},[t._v("暂无")])])])])],1),t._v(" "),a("el-col",{attrs:{span:8}},[a("el-card",[a("div",{staticClass:"card-fixed-header-dsh"},[t._v("\n          待审核事项\n          "),a("el-select",{attrs:{filterable:"",placeholder:"请选择"},on:{change:function(e){return t.get_shop_name_pending_review()}},model:{value:t.pending_review_value,callback:function(e){t.pending_review_value=e},expression:"pending_review_value"}},t._l(t.pending_review_dict,(function(t){return a("el-option",{key:t.value,attrs:{label:t.label,value:t.value}})})),1)],1),t._v(" "),a("div",{staticClass:"box-card card-panel-col card-setting"},[void 0!==t.pending_review&&t.pending_review.length>0?a("div",t._l(t.pending_review,(function(e,s){return a("div",{key:s,staticClass:"text item"},[a("el-card",{staticClass:"card-bottom",attrs:{shadow:"never"}},[a("div",{staticClass:"card-bottom-sh"}),t._v("\n                "+t._s(e.shop_name)+"【"+t._s(e.project)+"】\n                "),a("div",{staticClass:"bottom clearfix"},[a("span",{staticClass:"time"},[t._v("提交时间")]),t._v(" "),a("time",{staticClass:"time"},[t._v(t._s(e.submit_time))]),t._v(" "),a("class",{staticClass:"money"},[t._v("   ￥"+t._s(e.money))]),t._v(" "),a("class",{staticClass:"money",staticStyle:{color:"#f0e68c"}},[t._v("   "+t._s(e.status))]),t._v(" "),a("el-progress",{staticStyle:{width:"30%",float:"right",position:"relative",bottom:"-5px"},attrs:{percentage:e.schedule,"show-text":!1}})],1)])],1)})),0):a("div",[a("div",{staticClass:"div2"},[t._v("暂无")])])])])],1),t._v(" "),a("el-col",{attrs:{span:8}},[a("el-card",[a("div",{staticClass:"card-fixed-header-ywc"},[t._v("\n          已完成事项\n          "),a("el-select",{attrs:{filterable:"",placeholder:"请选择"},on:{change:function(e){return t.get_shop_name_completed()}},model:{value:t.completed_value,callback:function(e){t.completed_value=e},expression:"completed_value"}},t._l(t.completed_dict,(function(t){return a("el-option",{key:t.value,attrs:{label:t.label,value:t.value}})})),1)],1),t._v(" "),a("div",{staticClass:"box-card card-panel-col card-setting"},[void 0!==t.completed&&t.completed.length>0?a("div",t._l(t.completed,(function(e,s){return a("div",{key:s,staticClass:"text item"},[a("el-card",{staticClass:"card-bottom",attrs:{shadow:"never"}},[a("div",{staticClass:"card-bottom-wc"}),t._v("\n                "+t._s(e.shop_name)+"【"+t._s(e.project)+"】\n                "),a("div",{staticClass:"bottom clearfix"},[a("span",{staticClass:"time"},[t._v("通过时间")]),t._v(" "),a("time",{staticClass:"time"},[t._v(t._s(e.success_time))]),t._v(" "),a("class",{staticClass:"money"},[t._v("   ￥"+t._s(e.money))]),t._v(" "),a("class",{staticClass:"money",staticStyle:{color:"#34bfa3"}},[t._v("   "+t._s(e.status))]),t._v(" "),a("el-progress",{staticStyle:{width:"30%",float:"right",position:"relative",bottom:"-5px"},attrs:{percentage:e.schedule,"show-text":!1}})],1)])],1)})),0):a("div",[a("div",{staticClass:"div2"},[t._v("暂无")])])])])],1)],1),t._v(" "),a("el-dialog",{staticClass:"dialog",attrs:{title:"待办事项提交审核",visible:t.dialogFormVisible,center:"true"},on:{"update:visible":function(e){t.dialogFormVisible=e}}},[a("el-form",{attrs:{model:t.form}},[a("el-form-item",{attrs:{label:"代办事项名称","label-width":t.formLabelWidth}},[a("el-input",{attrs:{autocomplete:"off",disabled:!0},model:{value:t.form.name,callback:function(e){t.$set(t.form,"name",e)},expression:"form.name"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"备注信息","label-width":t.formLabelWidth}},[a("el-input",{attrs:{type:"textarea",autocomplete:"off"},model:{value:t.edit,callback:function(e){t.edit=e},expression:"edit"}})],1)],1),t._v(" "),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(e){t.dialogFormVisible=!1}}},[t._v("取 消")]),t._v(" "),a("el-button",{attrs:{type:"primary"},on:{click:function(e){t.dialogFormVisible=!1,t.handleclose(t.form)}}},[t._v("确 定")])],1)],1),t._v(" "),a("el-dialog",{staticClass:"dialog",attrs:{title:"奖金明细",visible:t.dialogFormVisible_jiangjinmingxi,center:"true"},on:{"update:visible":function(e){t.dialogFormVisible_jiangjinmingxi=e}}},[a("el-tabs",{attrs:{type:"card"},on:{"tab-click":t.handleClick},model:{value:t.activeName,callback:function(e){t.activeName=e},expression:"activeName"}},[a("el-tab-pane",{attrs:{label:"本月",name:"first"}},[a("el-table",{staticStyle:{width:"100%"},attrs:{data:t.jiangjin,label:t.本月服务奖金}},[a("el-table-column",{attrs:{property:"shop_name",label:"店名",width:"200"}}),t._v(" "),a("el-table-column",{attrs:{property:"project",label:"项目名称",width:"200"}}),t._v(" "),a("el-table-column",{attrs:{property:"money",label:"奖金"}}),t._v(" "),a("el-table-column",{attrs:{property:"time",label:"截止时间"}}),t._v(" "),a("el-table-column",{attrs:{property:"status",label:"状态"},scopedSlots:t._u([{key:"default",fn:function(e){var s=e.row;return["未完成"===s.status?a("div",[a("span",{staticClass:"link-type",staticStyle:{color:"#FF0000"}},[t._v(t._s(s.status))])]):"已完成"===s.status?a("div",[a("span",{staticClass:"link-type",staticStyle:{color:"#7CFC00"}},[t._v(t._s(s.status))])]):"待审核"===s.status?a("div",[a("span",{staticClass:"link-type",staticStyle:{color:"#FFD700"}},[t._v(t._s(s.status))])]):t._e()]}}])})],1),t._v(" "),a("div",{staticStyle:{"text-align":"center","margin-top":"30px"}},[a("el-pagination",{staticStyle:{"margin-bottom":"15px"},attrs:{"current-page":t.currentPage,background:"",layout:"prev, pager,jumper, next, sizes, total","page-sizes":[10,20,50,100],total:t.total},on:{"size-change":t.handleSizeChange,"current-change":t.handleCurrentChange}})],1)],1),t._v(" "),a("el-tab-pane",{attrs:{label:"下月",name:"second"}},[a("el-table",{staticStyle:{width:"100%"},attrs:{data:t.jiangjin_xiayue,label:t.下月服务奖金}},[a("el-table-column",{attrs:{property:"shop_name",label:"店名",width:"200"}}),t._v(" "),a("el-table-column",{attrs:{property:"project",label:"项目名称",width:"200"}}),t._v(" "),a("el-table-column",{attrs:{property:"money",label:"奖金"}}),t._v(" "),a("el-table-column",{attrs:{property:"time",label:"截止时间"}}),t._v(" "),a("el-table-column",{attrs:{property:"status",label:"状态"},scopedSlots:t._u([{key:"default",fn:function(e){var s=e.row;return["未完成"===s.status?a("div",[a("span",{staticClass:"link-type",staticStyle:{color:"#FF0000"}},[t._v(t._s(s.status))])]):"已完成"===s.status?a("div",[a("span",{staticClass:"link-type",staticStyle:{color:"#7CFC00"}},[t._v(t._s(s.status))])]):"待审核"===s.status?a("div",[a("span",{staticClass:"link-type",staticStyle:{color:"#FFD700"}},[t._v(t._s(s.status))])]):t._e()]}}])})],1),t._v(" "),a("div",{staticStyle:{"text-align":"center","margin-top":"30px"}},[a("el-pagination",{staticStyle:{"margin-bottom":"15px"},attrs:{"current-page":t.currentPage,background:"",layout:"prev, pager,jumper, next, sizes, total","page-sizes":[10,20,50,100],total:t.total_xiayue},on:{"size-change":t.handleSizeChange_xiayue,"current-change":t.handleCurrentChange_xiayue}})],1)],1)],1),t._v(" "),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(e){t.dialogFormVisible_jiangjinmingxi=!1}}},[t._v("取 消")]),t._v(" "),a("el-button",{attrs:{type:"primary"},on:{click:function(e){t.dialogFormVisible_jiangjinmingxi=!1}}},[t._v("确 定")])],1)],1),t._v(" "),a("el-dialog",{attrs:{title:"本月业绩概览",visible:t.dialogTableVisible_benyueyeji},on:{"update:visible":function(e){t.dialogTableVisible_benyueyeji=e}}},[a("el-table",{attrs:{data:t.benyueyeji_data}},[a("el-table-column",{attrs:{property:"sign_contract_shop",label:"签约店名",width:"200"}}),t._v(" "),a("el-table-column",{attrs:{property:"order_date",label:"签约日期",width:"150"}}),t._v(" "),a("el-table-column",{attrs:{property:"order_amount",label:"签约金额"}}),t._v(" "),a("el-table-column",{attrs:{property:"tags",label:"签约状态"},scopedSlots:t._u([{key:"default",fn:function(e){var s=e.row;return["新签"===s.tags?a("div",[a("span",{staticClass:"link-type",staticStyle:{color:"#00FF00"},attrs:{slot:"reference"},slot:"reference"},[t._v(t._s(s.tags))])]):"断约"===s.tags?a("div",[a("span",{staticClass:"link-type",staticStyle:{color:"#FFFF00"},attrs:{slot:"reference"},slot:"reference"},[t._v(t._s(s.tags))])]):"续约"===s.tags?a("div",[a("span",{staticClass:"link-type",staticStyle:{color:"#1E90FF"},attrs:{slot:"reference"},slot:"reference"},[t._v(t._s(s.tags))])]):t._e()]}}])})],1),t._v(" "),a("div",{staticStyle:{"text-align":"center","margin-top":"30px"}},[a("el-pagination",{staticStyle:{"margin-bottom":"15px"},attrs:{"current-page":t.currentPage_benyueyeji,background:"",layout:"prev, pager,jumper, next, sizes, total","page-sizes":[10,20,50,100],total:t.total_benyueyeji},on:{"size-change":t.handleSizeChange_benyueyeji,"current-change":t.handleCurrentChange_benyueyeji}})],1)],1)],1)},i=[],n=(a("6b54"),a("ec1b")),o=a.n(n),l=(a("b775"),a("0f9a")),r={components:{CountTo:o.a},data:function(){return{lat:"",lng:"",activeName:"first",dialogFormVisible_jiangjinmingxi:!1,edit:"",dialogTableVisible_benyueyeji:!1,startVal:0,table_simple_data:0,table_simple_data_signing:0,dialogFormVisible:!1,last_month_service_bonus:0,next_get_month_service_bonus:0,next_month_service_bonus:0,month_service_bonus:0,user:0,month_data:0,jiangjin_xiayue:0,currentPage_xiayue:1,pagesize_xiayue:10,total_xiayue:0,benyueyeji_data:[],currentPage_benyueyeji:1,pagesize_benyueyeji:10,total_benyueyeji:0,jiangjin:[],date_year:0,date_month:0,commission_point:0,table_simple_new_all_data:0,currentPage:1,pagesize:10,to_do:[],completed:[],pending_review:[],total:0,index:"",roles:"",formLabelWidth:"120px",form:{lat2:"",lng2:"",name:"",region:"",date1:"",date2:"",delivery:!1,type:[],resource:"",desc:""},todo_dict:[],todo_value:"待办事项",todo_shop_name:"",get_username:"",pending_review_dict:[],pending_review_value:"待审核事项",completed_dict:[],xiaoshou_value:"",completed_value:"已完成事项",xiaoshou_options:[]}},created:function(){this.roles=l["default"].state["avatar"],console.log("this.roles",this.roles),"admin"===l["default"].state["avatar"]&&this.get_xiaoshou_data();var t=new Date,e=t.getFullYear(),a=t.getMonth()+1;a=a.toString(),1==a.length&&(a="0"+a),this.month_data=e.toString()+"-"+a.toString(),this.date_year=e.toString(),this.date_month=a.toString(),console.log(e.toString()+"-"+a.toString()),this.fetchData(l["default"].state["first_name"]),this.get_to_do(l["default"].state["first_name"]),this.get_shop_name(l["default"].state["first_name"]),this.get_pending_review(l["default"].state["first_name"]),this.get_completed(l["default"].state["first_name"])},methods:{handleclose:function(t){var e=this;this.axios.get("http://152.32.135.62/app/submit_review/",{params:{project:this.to_do[this.index].project,shop_name:this.to_do[this.index].shop_name,time:this.to_do[this.index].time,money:this.to_do[this.index].money,schedule:this.to_do[this.index].schedule,username:this.to_do[this.index].username,order_id:this.to_do[this.index].order_id,edit:this.edit,lat:this.lat,lng:this.lng}}).then((function(t){e.$notify({title:"提交成功",message:"",type:"success"}),e.get_to_do(e.xiaoshou_value),e.get_pending_review(e.xiaoshou_value)}))},get_benyuejiangjing:function(){var t=this;""===this.xiaoshou_value?this.axios.get("http://152.32.135.62/app/get_benyuejiangjing/",{params:{pagesize:this.pagesize,currentPage:this.currentPage,month:this.month_data,username:l["default"].state["first_name"]}}).then((function(e){console.log("body",e),t.jiangjin=e.data.data,t.total=e.data.total})):this.axios.get("http://152.32.135.62/app/get_benyuejiangjing/",{params:{pagesize:this.pagesize,currentPage:this.currentPage,month:this.month_data,username:this.xiaoshou_value}}).then((function(e){t.jiangjin=e.data.data,t.total=e.data.total}))},get_benyueyeji:function(){var t=this;""===this.xiaoshou_value?this.axios.get("http://152.32.135.62/app/get_benyueyeji/",{params:{pagesize:this.pagesize_benyueyeji,currentPage:this.currentPage_benyueyeji,month:this.month_data,username:l["default"].state["first_name"]}}).then((function(e){t.benyueyeji_data=e.data.data,t.total_benyueyeji=e.data.total})):this.axios.get("http://152.32.135.62/app/get_benyueyeji/",{params:{pagesize:this.pagesize_benyueyeji,currentPage:this.currentPage_benyueyeji,month:this.month_data,username:this.xiaoshou_value}}).then((function(e){t.benyueyeji_data=e.data.data,t.total_benyueyeji=e.data.total}))},get_benyuejiangjing_xiayue:function(){var t=this;""===this.xiaoshou_value?this.axios.get("http://152.32.135.62/app/get_benyuejiangjing_xiayue/",{params:{pagesize:this.pagesize_xiayue,currentPage:this.currentPage_xiayue,month:this.month_data,username:l["default"].state["first_name"]}}).then((function(e){console.log("body",e),t.jiangjin_xiayue=e.data.data,t.total_xiayue=e.data.total})):this.axios.get("http://152.32.135.62/app/get_benyuejiangjing_xiayue/",{params:{pagesize:this.pagesize_xiayue,currentPage:this.currentPage_xiayue,month:this.month_data,username:this.xiaoshou_value}}).then((function(e){t.jiangjin_xiayue=e.data.data,t.total_xiayue=e.data.total}))},get_xiaoshou_data:function(){var t=this;this.axios.get("http://152.32.135.62/app/get_xiaoshou_data/").then((function(e){t.xiaoshou_options=e.data.data}))},get_shop_name_todo:function(t){var e=this;console.log("shop_name",this.todo_value),""!=this.xiaoshou_value?this.axios.get("http://152.32.135.62/app/get_to_do/",{params:{username:this.xiaoshou_value,shop_name:this.todo_value}}).then((function(t){e.to_do=t.data.data})):this.axios.get("http://152.32.135.62/app/get_to_do/",{params:{username:l["default"].state["first_name"],shop_name:this.todo_value}}).then((function(t){e.to_do=t.data.data}))},get_shop_name_pending_review:function(t){var e=this;""!=this.xiaoshou_value?this.axios.get("http://152.32.135.62/app/get_pending_review/",{params:{username:this.xiaoshou_value,shop_name:this.pending_review_value}}).then((function(t){console.log(t.data.data),e.pending_review=t.data.data})):this.axios.get("http://152.32.135.62/app/get_pending_review/",{params:{username:l["default"].state["first_name"],shop_name:this.pending_review_value}}).then((function(t){console.log(t.data.data),e.pending_review=t.data.data}))},get_shop_name_completed:function(t){var e=this;""!=this.xiaoshou_value?this.axios.get("http://152.32.135.62/app/get_completed/",{params:{username:this.xiaoshou_value,shop_name:this.completed_value}}).then((function(t){e.completed=t.data.data})):this.axios.get("http://152.32.135.62/app/get_completed/",{params:{username:l["default"].state["first_name"],shop_name:this.pending_review_value}}).then((function(t){console.log(t.data.data),e.pending_review=t.data.data}))},get_shop_name:function(t){var e=this;this.axios.get("http://152.32.135.62/app/get_shop_name/",{params:{username:t}}).then((function(t){e.todo_dict=t.data.todo_dict,e.pending_review_dict=t.data.pending_review_dict,e.completed_dict=t.data.completed_dict})).catch((function(t){this.loading=!1,console.log(t)}))},formatTime:function(t){var e=this;console.log("this.xiaoshou_value",this.xiaoshou_value),""===this.xiaoshou_value&&(this.xiaoshou_value=l["default"].state["first_name"]),this.axios.get("http://152.32.135.62/app/order_count/",{params:{username:this.xiaoshou_value,month_data:this.month_data}}).then((function(t){e.table_simple_data=t.data.table_simple_data,e.table_simple_data_signing=t.data.table_simple_data_signing,e.user=t.data.user,e.commission_point=t.data.commission_point,e.table_simple_new_all_data=t.data.table_simple_new_all_data,e.last_month_service_bonus=t.data.last_month_service_bonus,e.month_service_bonus=t.data.month_service_bonus,e.next_get_month_service_bonus=t.data.next_get_month_service_bonus,e.next_month_service_bonus=t.data.next_month_service_bonus,console.log(t.data)}))},handleSetLineChartData:function(t){"newVisitis"===t?(this.dialogTableVisible_benyueyeji=!0,this.get_benyueyeji()):"shoppings"===t?window.location.href="http://www.beiai.tech/#/table/dynamic-table":"messages"===t?(this.dialogFormVisible_jiangjinmingxi=!0,this.get_benyuejiangjing(),this.get_benyuejiangjing_xiayue()):"purchases"===t?window.location.href="http://www.beiai.tech/#/charts/%E6%88%91%E7%9A%84%E8%AE%A2%E5%8D%95":this.$notify({title:"找不到地址",message:"",type:"error"})},fetchData:function(t){var e=this;this.axios.get("http://152.32.135.62/app/order_count/",{params:{username:t,month_data:this.month_data}}).then((function(t){e.table_simple_data=t.data.table_simple_data,e.table_simple_data_signing=t.data.table_simple_data_signing,e.user=t.data.user,e.commission_point=t.data.commission_point,e.table_simple_new_all_data=t.data.table_simple_new_all_data,e.last_month_service_bonus=t.data.last_month_service_bonus,e.month_service_bonus=t.data.month_service_bonus,e.next_get_month_service_bonus=t.data.next_get_month_service_bonus,e.next_month_service_bonus=t.data.next_month_service_bonus,console.log(t.data)}))},select:function(t){var e=new Date,a=e.getFullYear(),s=e.getMonth()+1,i=e.getDate();s=s.toString(),1===s.length&&(s="0"+s);var n=new Date(a+"-"+s+"-"+i),o=new Date(this.to_do[t].time),l=o.getTime()-n.getTime(),r=l/864e5;console.log("差值",r),n.getTime()>o.getTime()?this.$notify({title:"提交失败",message:"已超时",type:"error"}):r>15?this.$notify({title:"提交失败",message:"截止日期之前15天内提交",type:"error"}):(this.form.name=this.to_do[t].shop_name+"【"+this.to_do[t].project+"】",this.dialogFormVisible=!0,this.index=t)},get_to_do:function(t){var e=this;""!=this.xiaoshou_value?this.axios.get("http://152.32.135.62/app/get_to_do/",{params:{username:this.xiaoshou_value,shop_name:this.todo_value}}).then((function(t){e.to_do=t.data.data})):this.axios.get("http://152.32.135.62/app/get_to_do/",{params:{username:l["default"].state["first_name"],shop_name:this.todo_value}}).then((function(t){e.to_do=t.data.data}))},xiaoshou_change:function(t){""===t?(this.fetchData(l["default"].state["first_name"]),this.get_to_do(l["default"].state["first_name"]),this.get_shop_name(l["default"].state["first_name"]),this.get_pending_review(l["default"].state["first_name"]),this.get_completed(l["default"].state["first_name"])):(this.fetchData(t),this.get_to_do(t),this.get_shop_name(t),this.get_pending_review(t),this.get_completed(t))},get_pending_review:function(t){var e=this;""!=this.xiaoshou_value?this.axios.get("http://152.32.135.62/app/get_pending_review/",{params:{username:this.xiaoshou_value,shop_name:this.pending_review_value}}).then((function(t){console.log(t.data.data),e.pending_review=t.data.data})):this.axios.get("http://152.32.135.62/app/get_pending_review/",{params:{username:l["default"].state["first_name"],shop_name:this.pending_review_value}}).then((function(t){console.log(t.data.data),e.pending_review=t.data.data}))},get_completed:function(t){var e=this;""!=this.xiaoshou_value?this.axios.get("http://152.32.135.62/app/get_completed/",{params:{username:this.xiaoshou_value,shop_name:this.completed_value}}).then((function(t){e.completed=t.data.data})):this.axios.get("http://152.32.135.62/app/get_completed/",{params:{username:l["default"].state["first_name"],shop_name:this.completed_value}}).then((function(t){e.completed=t.data.data}))},handleSizeChange:function(t){this.pagesize=t,this.get_benyuejiangjing()},handleCurrentChange:function(t){this.currentPage=t,this.get_benyuejiangjing()},handleSizeChange_xiayue:function(t){this.pagesize_xiayue=t,this.get_benyuejiangjing_xiayue()},handleCurrentChange_xiayue:function(t){this.currentPage_xiayue=t,this.get_benyuejiangjing_xiayue()},handleSizeChange_benyueyeji:function(t){this.pagesize_benyueyeji=t,this.get_benyueyeji()},handleCurrentChange_benyueyeji:function(t){this.currentPage_benyueyeji=t,this.get_benyueyeji()}}},_=r,c=(a("2de5"),a("2877")),d=Object(c["a"])(_,s,i,!1,null,"7bd36a93",null);e["default"]=d.exports}}]);