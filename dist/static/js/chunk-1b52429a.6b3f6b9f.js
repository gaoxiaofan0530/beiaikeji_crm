(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-1b52429a"],{"90ca":function(e,t,a){},c433:function(e,t,a){"use strict";var o=a("90ca"),i=a.n(o);i.a},f328:function(e,t,a){"use strict";a.r(t);var o=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("el-drawer",{staticClass:"drawer",attrs:{title:"订单详情",visible:e.drawer,direction:e.direction,"before-close":e.handleClose,size:"100"},on:{"update:visible":function(t){e.drawer=t}}},[a("div",{staticClass:"demo-drawer__content"},[a("el-form",{attrs:{model:e.form}},[a("el-form-item",{attrs:{label:"订单ID","label-width":e.formLabelWidth}},[a("el-input",{staticStyle:{width:"80%"},attrs:{autocomplete:"off",disabled:!0},model:{value:e.order_edit.contract_id_edit,callback:function(t){e.$set(e.order_edit,"contract_id_edit",t)},expression:"order_edit.contract_id_edit"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"店名","label-width":e.formLabelWidth}},[a("el-input",{staticStyle:{width:"80%"},attrs:{placeholder:"请选择活动区域",disabled:!0},model:{value:e.order_edit.sign_contract_shop_edit,callback:function(t){e.$set(e.order_edit,"sign_contract_shop_edit",t)},expression:"order_edit.sign_contract_shop_edit"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"下单日期","label-width":e.formLabelWidth}},[a("el-date-picker",{attrs:{type:"date",placeholder:"选择日期",disabled:!0},model:{value:e.order_edit.order_date_edit,callback:function(t){e.$set(e.order_edit,"order_date_edit",t)},expression:"order_edit.order_date_edit"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"开始日期","label-width":e.formLabelWidth}},[a("el-date-picker",{attrs:{type:"date",placeholder:"选择日期",disabled:!0},model:{value:e.order_edit.order_start_date_edit,callback:function(t){e.$set(e.order_edit,"order_start_date_edit",t)},expression:"order_edit.order_start_date_edit"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"门店数","label-width":e.formLabelWidth}},[a("el-input-number",{attrs:{min:1,max:10,disabled:!0,label:"描述文字"},on:{change:e.handleChange},model:{value:e.order_edit.order_numbers_edit,callback:function(t){e.$set(e.order_edit,"order_numbers_edit",t)},expression:"order_edit.order_numbers_edit"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"合作时长","label-width":e.formLabelWidth}},[a("el-select",{staticClass:"filter-item",attrs:{filterable:"","value-key":"id",placeholder:"请选合作时长",disabled:!0},model:{value:e.order_edit.shop_cooperation_duration_edit,callback:function(t){e.$set(e.order_edit,"shop_cooperation_duration_edit",t)},expression:"order_edit.shop_cooperation_duration_edit"}},e._l(e.cooperation_duration,(function(e){return a("el-option",{key:e.id,attrs:{label:e.label,value:e}})})),1)],1),e._v(" "),a("el-form-item",{attrs:{label:"结束日期","label-width":e.formLabelWidth}},[a("el-date-picker",{attrs:{type:"date",placeholder:"选择日期",disabled:!0},model:{value:e.order_edit.order_end_date_edit,callback:function(t){e.$set(e.order_edit,"order_end_date_edit",t)},expression:"order_edit.order_end_date_edit"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"签约金额","label-width":e.formLabelWidth}},[a("el-input",{staticStyle:{width:"80%"},attrs:{placeholder:"请选择活动区域",disabled:!0},model:{value:e.order_edit.order_amount_edit,callback:function(t){e.$set(e.order_edit,"order_amount_edit",t)},expression:"order_edit.order_amount_edit"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"签约销售","label-width":e.formLabelWidth}},[a("el-input",{staticStyle:{width:"80%"},attrs:{placeholder:"签约销售",disabled:!0},model:{value:e.order_edit.order_contract_sales_edit,callback:function(t){e.$set(e.order_edit,"order_contract_sales_edit",t)},expression:"order_edit.order_contract_sales_edit"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"提成","label-width":e.formLabelWidth}},[a("el-input",{staticStyle:{width:"80%"},attrs:{autocomplete:"off",disabled:!0},model:{value:e.order_edit.order_commission,callback:function(t){e.$set(e.order_edit,"order_commission",t)},expression:"order_edit.order_commission"}})],1),e._v(" "),a("el-divider"),e._v(" "),e._l(e.shop_add_form,(function(t,o){return a("el-form-item",{key:t.key,staticStyle:{width:"80%"},attrs:{label:t.label,"label-width":e.formLabelWidth}},["文本类型"===t.type?a("span",[a("el-input",{attrs:{disabled:!0},on:{blur:function(a){return e.edit_shop_add_form(o,t.value)}},model:{value:t.value,callback:function(a){e.$set(t,"value",a)},expression:"domain.value"}})],1):e._e(),e._v(" "),"日期类型"===t.type?a("span",[a("el-date-picker",{attrs:{type:"date",placeholder:"选择日期",disabled:!0},on:{change:function(a){return e.edit_shop_add_form(o,t.value)}},model:{value:t.value,callback:function(a){e.$set(t,"value",a)},expression:"domain.value"}})],1):e._e(),e._v(" "),"选择下拉框"===t.type?a("span",[a("el-select",{attrs:{type:"date",disabled:!0,placeholder:"选择内容"},on:{change:function(a){return e.edit_shop_add_form(o,t.value)}},model:{value:t.value,callback:function(a){e.$set(t,"value",a)},expression:"domain.value"}},e._l(t.select,(function(e){return a("el-option",{key:e.label,attrs:{label:e.label,value:e.value}})})),1)],1):e._e(),e._v(" "),"大文本框"===t.type?a("span",[a("el-input",{attrs:{disabled:!0,type:"textarea"},on:{blur:function(a){return e.edit_shop_add_form(o,t.value)}},model:{value:t.value,callback:function(a){e.$set(t,"value",a)},expression:"domain.value"}})],1):e._e()])})),e._v(" "),a("el-divider",[e._v("备注")]),e._v(" "),a("el-form-item",{attrs:{label:"备注",disabled:!0,"label-width":e.formLabelWidth}},e._l(e.shop_edits,(function(t,o){return a("div",[a("el-input",{staticStyle:{width:"80%"},attrs:{placeholder:"备注信息",disabled:!0},model:{value:e.shop_edits[o]["label"],callback:function(t){e.$set(e.shop_edits[o],"label",t)},expression:"shop_edits[index]['label']"}})],1)})),0)],2)],1)]),e._v(" "),a("div",{staticClass:"filter-container",staticStyle:{"margin-left":"15px","margin-top":"25px"}},[a("el-input",{staticStyle:{width:"200px"},attrs:{placeholder:"查询"},on:{input:e.select_input},model:{value:e.title,callback:function(t){e.title=t},expression:"title"}},[a("i",{staticClass:"el-input__icon el-icon-search",attrs:{slot:"prefix"},slot:"prefix"})]),e._v(" "),a("el-date-picker",{attrs:{type:"month",placeholder:"选择月"},on:{change:e.select_month},model:{value:e.month,callback:function(t){e.month=t},expression:"month"}}),e._v(" "),"admin"===e.roles?a("span",[a("el-select",{attrs:{clearable:"",filterable:"",placeholder:"请选择"},on:{change:function(t){return e.xiaoshou_change(e.xiaoshou_value)}},model:{value:e.xiaoshou_value,callback:function(t){e.xiaoshou_value=t},expression:"xiaoshou_value"}},e._l(e.xiaoshou_options,(function(e){return a("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})})),1)],1):e._e()],1),e._v(" "),a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],ref:"multipleTable",staticStyle:{width:"100%","margin-left":"15px","margin-right":"30px"},attrs:{data:e.tableData,border:"",fit:"",stripe:"","highlight-current-row":""},on:{"sort-change":e.sortChange,"row-click":e.data_update}},[a("el-table-column",{attrs:{prop:"contract_id","show-overflow-tooltip":"",label:"ID"},on:{click:function(t){e.data_update(e.row),e.drawer=!0}}}),e._v(" "),a("el-table-column",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],attrs:{prop:"sign_contract_shop","show-overflow-tooltip":"",border:"",fit:"",stripe:"","highlight-current-row":"",label:"签约商户",width:"450"},on:{click:function(t){e.data_update(e.row),e.drawer=!0}},scopedSlots:e._u([{key:"default",fn:function(t){var o=t.row;return["断约"===o.tags?a("div",[a("el-popover",{attrs:{placement:"top-start",width:"400",trigger:"hover"},on:{show:function(t){return e.get_shop_edit(o.shop_id)}}},[e._l(e.shop_edits,(function(t,o){return a("div",[a("el-input",{staticStyle:{width:"100%"},attrs:{placeholder:"备注信息",disabled:!0},model:{value:e.shop_edits[o]["label"],callback:function(t){e.$set(e.shop_edits[o],"label",t)},expression:"shop_edits[index]['label']"}})],1)})),e._v(" "),a("span",{staticClass:"link-type",staticStyle:{color:"#606266"},attrs:{slot:"reference"},on:{click:function(t){e.data_update(o),e.drawer=!0}},slot:"reference"},[e._v(e._s(o.sign_contract_shop))])],2),e._v(" "),a("el-tag",{attrs:{type:"warning",effect:"dark"}},[e._v(e._s(o.tags))])],1):"续约"===o.tags?a("div",[a("el-popover",{attrs:{placement:"top-start",width:"400",trigger:"hover"},on:{show:function(t){return e.get_shop_edit(o.shop_id)}}},[e._l(e.shop_edits,(function(t,o){return a("div",[a("el-input",{staticStyle:{width:"100%"},attrs:{placeholder:"备注信息",disabled:!0},model:{value:e.shop_edits[o]["label"],callback:function(t){e.$set(e.shop_edits[o],"label",t)},expression:"shop_edits[index]['label']"}})],1)})),e._v(" "),a("span",{staticClass:"link-type",staticStyle:{color:"#606266"},attrs:{slot:"reference"},on:{click:function(t){e.data_update(o),e.drawer=!0}},slot:"reference"},[e._v(e._s(o.sign_contract_shop))])],2),e._v(" "),a("el-tag",{attrs:{effect:"dark"}},[e._v(e._s(o.tags))])],1):"新签"===o.tags?a("div",[a("el-popover",{attrs:{placement:"top-start",width:"400",trigger:"hover"},on:{show:function(t){return e.get_shop_edit(o.shop_id)}}},[e._l(e.shop_edits,(function(t,o){return a("div",[a("el-input",{staticStyle:{width:"100%"},attrs:{placeholder:"备注信息",disabled:!0},model:{value:e.shop_edits[o]["label"],callback:function(t){e.$set(e.shop_edits[o],"label",t)},expression:"shop_edits[index]['label']"}})],1)})),e._v(" "),a("span",{staticClass:"link-type",staticStyle:{color:"#606266"},attrs:{slot:"reference"},on:{click:function(t){e.data_update(o),e.drawer=!0}},slot:"reference"},[e._v(e._s(o.sign_contract_shop))])],2),e._v(" "),a("el-tag",{attrs:{type:"success",effect:"dark"}},[e._v(e._s(o.tags))])],1):e._e()]}}])}),e._v(" "),a("el-table-column",{attrs:{prop:"order_date","show-overflow-tooltip":"",label:"下单日期"},on:{click:function(t){e.data_update(e.row),e.drawer=!0}}}),e._v(" "),a("el-table-column",{attrs:{prop:"order_start_date",sortable:"custom","show-overflow-tooltip":"",label:"开始时间"},on:{click:function(t){e.data_update(e.row),e.drawer=!0}}}),e._v(" "),a("el-table-column",{attrs:{prop:"shop_cooperation_duration","show-overflow-tooltip":"",label:"合作时长"},on:{click:function(t){e.data_update(e.row),e.drawer=!0}}}),e._v(" "),a("el-table-column",{attrs:{prop:"order_end_date","show-overflow-tooltip":"",label:"结束日期"},on:{click:function(t){e.data_update(e.row),e.drawer=!0}}}),e._v(" "),a("el-table-column",{attrs:{prop:"order_amount","show-overflow-tooltip":"",label:"收款金额"},on:{click:function(t){e.data_update(e.row),e.drawer=!0}}}),e._v(" "),a("el-table-column",{attrs:{prop:"remaining_number_of_days","show-overflow-tooltip":"",label:"剩余天数"},on:{click:function(t){e.data_update(e.row),e.drawer=!0}},scopedSlots:e._u([{key:"default",fn:function(t){var o=t.row;return["已到期"===o.zhuangtai?a("div",[a("span",{staticClass:"link-type",staticStyle:{color:"#008000"},on:{click:function(t){e.data_update(o),e.drawer=!0}}},[e._v(e._s(o.remaining_number_of_days))])]):a("div",[a("span",{staticClass:"link-type",staticStyle:{color:"#FF0000"},on:{click:function(t){e.data_update(o),e.drawer=!0}}},[e._v(e._s(o.remaining_number_of_days))])])]}}])}),e._v(" "),a("el-table-column",{attrs:{label:"操作",width:"210","show-overflow-tooltip":!0},scopedSlots:e._u([{key:"default",fn:function(t){return["admin"===e.roles?a("div",[a("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"删除",placement:"top-start"}},[a("el-button",{attrs:{size:"mini",type:"danger",content:"删除",placement:"top"},on:{click:function(a){return a.stopPropagation(),e.delete_order(t.row)}}},[a("i",{staticClass:"el-icon-delete"})])],1)],1):e._e()]}}])})],1),e._v(" "),a("div",{staticStyle:{"text-align":"center","margin-top":"30px"}},[a("el-pagination",{staticStyle:{"margin-bottom":"15px"},attrs:{"current-page":e.currentPage,background:"",layout:"prev, pager,jumper, next, sizes, total","page-sizes":[10,20,50,100],total:e.total},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}})],1)],1)},i=[],r=a("ade3"),d=(a("b775"),a("0f9a")),l={data:function(){var e;return e={tableData:[],user_data:[],shop_add_form:[],title:"",month:"",xiaoshou_value:"",xiaoshou_options:"",cooperation_duration:[{id:1,label:"1个月"},{id:2,label:"2个月"},{id:3,label:"3个月"},{id:4,label:"4个月"},{id:5,label:"5个月"},{id:6,label:"6个月"},{id:7,label:"7个月"},{id:8,label:"8个月"},{id:9,label:"9个月"},{id:10,label:"10个月"},{id:11,label:"11个月"},{id:12,label:"12个月"}],total:0,pagesize:10,currentPage:1,drawer:!1,roles:"",formLabelWidth:"80px",categorys:[{id:"美发",label:"美发"},{id:"美容/SPA",label:"美容/SPA"},{id:"美甲美睫",label:"美甲美睫"},{id:"医学美容",label:"医学美容"},{id:"瑜伽",label:"瑜伽"},{id:"舞蹈",label:"舞蹈"},{id:"纹绣",label:"纹绣"},{id:"瘦身纤体",label:"瘦身纤体"},{id:"纹身",label:"纹身"},{id:"祛痘",label:"祛痘"},{id:"化妆品",label:"化妆品"},{id:"产后塑形",label:"产后塑形"},{id:"养发",label:"养发"},{id:"全部",label:"全部"}]},Object(r["a"])(e,"cooperation_duration",[{id:1,label:"1个月"},{id:2,label:"2个月"},{id:3,label:"3个月"},{id:4,label:"4个月"},{id:5,label:"5个月"},{id:6,label:"6个月"},{id:7,label:"7个月"},{id:8,label:"8个月"},{id:9,label:"9个月"},{id:10,label:"10个月"},{id:11,label:"11个月"},{id:12,label:"12个月"}]),Object(r["a"])(e,"order_by",0),Object(r["a"])(e,"admin",""),Object(r["a"])(e,"shop_edits",[]),Object(r["a"])(e,"order_edit",{contract_id_edit:void 0,order_date_edit:void 0,order_start_date_edit:void 0,sign_contract_shop_edit:void 0,customer_source_edit:void 0,contract_status_edit:void 0,shop_industry_edit:void 0,shop_kp_name_edit:void 0,shop_telephonenumber_edit:void 0,order_numbers_edit:void 0,shop_cooperation_duration_edit:void 0,shop_kp_wechat_id_edit:void 0,order_end_date_edit:void 0,order_amount_edit:void 0,payment_method_edit:void 0,order_contract_sales_edit:void 0,shop_remark_edit:void 0,order_form_edit:void 0,shop_id:void 0,order_commission:void 0}),e},created:function(){this.roles=d["default"].state["avatar"],"admin"===d["default"].state["avatar"]&&this.get_xiaoshou_data(),this.addUser(this.pagesize,this.currentPage),this.user_data_xiaoshou(),this.select_user()},mounted:function(){this.addUser()},methods:{handleClose:function(e){this.drawer=!1,this.edit_shop(this.order_edit.contract_id_edit,this.order_edit.customer_source_edit,this.order_edit.contract_status_edit,this.order_edit.contracted_projects_edit,this.order_edit.shop_industry_edit,this.order_edit.shop_kp_name_edit,this.order_edit.shop_telephonenumber_edit,this.order_edit.order_numbers_edit,this.order_edit.payment_method_edit,this.order_edit.shop_id,this.order_edit.shop_remark_edit)},select_user:function(){var e=this;this.axios.get("http://152.32.135.62/app/select_user/",{params:{username:d["default"].state["first_name"]}}).then((function(t){e.admin=t.data.data,console.log("admin",e.admin)})).catch((function(e){this.loading=!1,console.log(e)}))},get_shop_edit:function(e){var t=this;console.log(e),this.axios.get("http://152.32.135.62/app/table_simple_get_edit/",{params:{shop_id:e,leixing:"公海"}}).then((function(e){t.shop_edits=e.data.data})).catch((function(e){this.loading=!1,console.log(e)}))},get_xiaoshou_data:function(){var e=this;this.axios.get("http://152.32.135.62/app/get_xiaoshou_data/").then((function(t){e.xiaoshou_options=t.data.data}))},addUser:function(e,t){var a=this;this.axios.get("http://152.32.135.62/app/table_simple_order_data_all/",{params:{pagesize:e,currentPage:t,username:this.xiaoshou_value,order_by:this.order_by,title:this.title,month:this.month}}).then((function(e){a.tableData=e.data.data,a.total=e.data.total,a.loading=!1})).catch((function(e){this.loading=!1,console.log(e)}))},edit_shop:function(e,t,a,o,i,r,d,l,s,n,_){var c=this;this.axios.get("http://152.32.135.62/app/order_select/",{params:{contract_id:e,customer_source:t,contract_status:a,contracted_projects:o,shop_industry:i,shop_kp_name:r,shop_telephonenumber:d,order_numbers:l,payment_method:s,shop_remark:_}}).then((function(e){c.$notify({title:"操作成功",message:"",type:"success"}),c.addUser(c.pagesize,c.currentPage)})).catch((function(e){this.loading=!1,console.log(e)}))},select_input:function(){this.addUser(this.pagesize,this.currentPage)},select_month:function(){this.addUser(this.pagesize,this.currentPage)},xiaoshou_change:function(){this.addUser(this.pagesize,this.currentPage)},data_update:function(e){this.drawer=!0,this.order_edit.contract_id_edit=e.contract_id,this.order_edit.order_date_edit=e.order_date,this.order_edit.order_start_date_edit=e.order_start_date,this.order_edit.sign_contract_shop_edit=e.sign_contract_shop,this.order_edit.customer_source_edit=e.customer_source,this.order_edit.contract_status_edit=e.contract_status,this.order_edit.contracted_projects_edit=e.contracted_projects,this.order_edit.shop_industry_edit=e.shop_industry,this.order_edit.shop_kp_name_edit=e.shop_kp_name,this.order_edit.shop_telephonenumber_edit=e.shop_telephonenumber,this.order_edit.order_numbers_edit=e.order_numbers,this.order_edit.shop_cooperation_duration_edit=e.shop_cooperation_duration,this.order_edit.shop_kp_wechat_id_edit=e.shop_kp_wechat_id,this.get_shop_edit(e.shop_id),this.order_edit.order_end_date_edit=e.order_end_date,this.order_edit.order_amount_edit=e.order_amount,this.order_edit.payment_method_edit=e.payment_method,this.order_edit.order_contract_sales_edit=e.order_contract_sales,this.order_edit.shop_remark_edit=e.shop_remark,this.order_edit.order_form_edit=e.order_form,this.order_edit.order_commission=e.order_commission,this.order_edit.shop_id=e.shop_id,this.shop_add_form=e.order_form},edit_shop_add_form:function(e,t){this.axios.get("http://152.32.135.62/app/edit_order_form_data/",{params:{shop_id:this.order_edit.sign_contract_shop_edit,index:e,value:t}}).then((function(e){})).catch((function(e){this.loading=!1,console.log(e)}))},user_data_xiaoshou:function(){var e=this;this.axios.get("http://152.32.135.62/app/get_user_data/",{}).then((function(t){e.user_data=t.data.data})).catch((function(e){this.loading=!1,console.log(e)}))},delete_order:function(e){var t=this;console.log(e),this.$confirm("确定要删除订单吗? 是否继续?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then((function(){t.axios.get("http://152.32.135.62/app/delete_order/",{params:{order_id:e.contract_id,shop_id:e.shop_id}}).then((function(e){1==e.data.state?(t.$notify({title:"删除成功",message:"",type:"success"}),t.addUser(t.pagesize,t.currentPage)):t.$notify({title:"删除失败",message:"",type:"error"})})).catch((function(e){this.loading=!1,console.log(e)}))}))},sortChange:function(e,t,a){this.order_by=e.order,this.addUser(this.pagesize,this.currentPage)},handleSizeChange:function(e){this.pagesize=e,this.addUser(e,this.currentPage),this.qryTableDate()},handleCurrentChange:function(e){console.log("第几页",e),this.currentPage=e,this.addUser(this.pagesize,e),this.qryTableDate()}}},s=l,n=(a("c433"),a("2877")),_=Object(n["a"])(s,o,i,!1,null,null,null);t["default"]=_.exports}}]);