<template>
  <div>
    <el-drawer
      class="drawer"
      title="订单详情"
      :visible.sync="drawer"
      :before-close="handleClose"
      size="100"
    >
      <div class="demo-drawer__content">
        <el-form :model="form">
          <el-form-item label="订单ID" :label-width="formLabelWidth">
            <el-input
              v-model="order_edit.contract_id_edit"
              autocomplete="off"
              style="width:80%"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="店名" :label-width="formLabelWidth">
            <el-input
              v-model="order_edit.sign_contract_shop_edit"
              style="width:80%"
              placeholder="请选择活动区域"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="下单日期" :label-width="formLabelWidth">
            <el-date-picker
              v-model="order_edit.order_date_edit"
              type="date"
              placeholder="选择日期"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="开始日期" :label-width="formLabelWidth">
            <el-date-picker
              v-model="order_edit.order_start_date_edit"
              type="date"
              placeholder="选择日期"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="门店数" :label-width="formLabelWidth">
            <el-input-number
              v-model="order_edit.order_numbers_edit"
              :min="1"
              :max="10"
              :disabled="true"
              label="描述文字"
            />
          </el-form-item>
          <el-form-item label="合作时长" :label-width="formLabelWidth">
            <el-select
              v-model="order_edit.shop_cooperation_duration_edit"
              filterable
              class="filter-item"
              value-key="id"
              placeholder="请选合作时长"
              :disabled="true"
            >
              <el-option
                v-for="item in cooperation_duration"
                :key="item.id"
                :label="item.label"
                :value="item"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="结束日期" :label-width="formLabelWidth">
            <el-date-picker
              v-model="order_edit.order_end_date_edit"
              type="date"
              placeholder="选择日期"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="签约金额" :label-width="formLabelWidth">
            <el-input
              v-model="order_edit.order_amount_edit"
              style="width:80%"
              placeholder="请选择活动区域"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="成本费" :label-width="formLabelWidth">
            <el-input
              v-model="order_edit.cost_fees"
              style="width:80%"
              placeholder="请选择活动区域"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="签约销售" :label-width="formLabelWidth">
            <el-input
              v-model="order_edit.order_contract_sales_edit"
              style="width:80%"
              placeholder="签约销售"
              :disabled="true"
            />
          </el-form-item>
          <el-divider />
          <el-form-item
            v-for="(domain, index) in shop_add_form"
            :key="domain.key"
            :label="domain.label"
            style="width:80%"
            :label-width="formLabelWidth"
          >
            <span v-if="domain.type === '文本类型'">
              <el-input
                v-model="domain.value"
                :disabled="true"
                @blur="edit_shop_add_form(index,domain.value)"
              />
            </span>
            <span v-if="domain.type === '日期类型'">
              <el-date-picker
                v-model="domain.value"
                type="date"
                placeholder="选择日期"
                :disabled="true"
                @change="edit_shop_add_form(index,domain.value)"
              />
            </span>
            <span v-if="domain.type === '选择下拉框'">
              <el-select
                v-model="domain.value"
                type="date"
                :disabled="true"
                placeholder="选择内容"
                @change="edit_shop_add_form(index,domain.value)"
              >
                <el-option
                  v-for="item in domain.select"
                  :key="item.label"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </span>
            <span v-if="domain.type === '大文本框'">
              <el-input
                v-model="domain.value"
                :disabled="true"
                type="textarea"
                @blur="edit_shop_add_form(index,domain.value)"
              />
            </span>
          </el-form-item>
          <el-divider>任务截图</el-divider>
            <img width="50%" height="50%" :src="order_edit.dialogImageUrl" alt="">
          <el-divider>备注</el-divider>
          <el-form-item label="备注" :disabled="true" :label-width="formLabelWidth">
            <div v-for="(item,index) in shop_edits">
              <el-input
                v-model="shop_edits[index]['label']"
                style="width:80%"
                placeholder="备注信息"
                :disabled="true"
              />
            </div>
          </el-form-item>
        </el-form>
      </div>
    </el-drawer>
    <div class="filter-container" style="margin-left:15px;margin-top:25px;">
      <el-input v-model="search" style="width: 200px;" placeholder="查询" @input="select_input">
        <i slot="prefix" class="el-input__icon el-icon-search" />
      </el-input>
    </div>
    <el-table
      ref="multipleTable"
      v-loading="loading"
      :data="tableData"
      border
      fit
      stripe
      highlight-current-row
      style="width: 100%;margin-left:15px;margin-right:30px"
      @sort-change="sortChange"
      @row-click="data_update"
    >
      <el-table-column
        prop="contract_id"
        show-overflow-tooltip
        label="ID"
        @click="data_update(row);drawer = true"
      />
      <el-table-column
        prop="sign_contract_shop"
        v-loading="loading"
        show-overflow-tooltip
        border
        fit
        stripe
        highlight-current-row
        label="签约商户"
        width="400"
        @click="data_update(row);drawer = true"
      >
        <template slot-scope="{row}">
          <div v-if="row.tags === '断约'">
            <el-popover
              placement="top-start"
              width="400"
              trigger="hover"
              @show="get_shop_edit(row.shop_id)"
            >
              <div v-for="(item,index) in shop_edits">
                <el-input
                  v-model="shop_edits[index]['label']"
                  style="width:100%"
                  placeholder="备注信息"
                  :disabled="true"
                />
              </div>
              <span
                class="link-type"
                style="color:#606266"
                slot="reference"
                @click="data_update(row);drawer = true"
              >{{ row.sign_contract_shop }}</span>
            </el-popover>
            <el-tag type="warning" effect="dark">{{ row.tags }}</el-tag>
          </div>
          <div v-else-if="row.tags === '续约'">
            <el-popover
              placement="top-start"
              width="400"
              trigger="hover"
              @show="get_shop_edit(row.shop_id)"
            >
              <div v-for="(item,index) in shop_edits">
                <el-input
                  v-model="shop_edits[index]['label']"
                  style="width:100%"
                  placeholder="备注信息"
                  :disabled="true"
                />
              </div>
              <span
                class="link-type"
                slot="reference"
                style="color:#606266"
                @click="data_update(row);drawer = true"
              >{{ row.sign_contract_shop }}</span>
            </el-popover>
            <el-tag effect="dark">{{ row.tags }}</el-tag>
          </div>
          <div v-else-if="row.tags === '新签'">
            <el-popover
              placement="top-start"
              width="400"
              trigger="hover"
              @show="get_shop_edit(row.shop_id)"
            >
              <div v-for="(item,index) in shop_edits">
                <el-input
                  v-model="shop_edits[index]['label']"
                  style="width:100%"
                  placeholder="备注信息"
                  :disabled="true"
                />
              </div>
              <span
                class="link-type"
                slot="reference"
                style="color:#606266"
                @click="data_update(row);drawer = true"
              >{{ row.sign_contract_shop }}</span>
            </el-popover>
            <el-tag type="success" effect="dark">{{ row.tags }}</el-tag>
          </div>
          <!-- <div v-else>
            <el-popover
              placement="top-start"
              width="400"
              trigger="hover"
              @show="get_shop_edit(row.shop_id)"
            >
              <div v-for="(item,index) in shop_edits">
                <el-input
                  v-model="shop_edits[index]['label']"
                  style="width:100%"
                  placeholder="备注信息"
                  :disabled="true"
                />
              </div>
              <span
                class="link-type"
                style="color:#606266"
                @click="data_update(row);drawer = true"
              >{{ row.sign_contract_shop }}</span>
            </el-popover>
          </div>-->
        </template>
      </el-table-column>
      <el-table-column
        prop="order_date"
        show-overflow-tooltip
        label="下单日期"
        @click="data_update(row);drawer = true"
      />
      <el-table-column
        prop="order_start_date"
        show-overflow-tooltip
        label="开始时间"
        @click="data_update(row);drawer = true"
      />
      <el-table-column
        prop="shop_cooperation_duration"
        show-overflow-tooltip
        label="合作时长"
        @click="data_update(row);drawer = true"
      />
      <el-table-column
        prop="order_end_date"
        show-overflow-tooltip
        label="结束日期"
        @click="data_update(row);drawer = true"
      />
      <el-table-column
        prop="order_amount"
        show-overflow-tooltip
        label="收款金额"
        @click="data_update(row);drawer = true"
      />
      <el-table-column
        prop="order_contract_sales"
        show-overflow-tooltip
        label="签约销售"
        @click="data_update(row);drawer = true"
      />
      <el-table-column label="操作" width="210" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click.stop="jump_href(scope.row);">
            <i class="el-icon-check" />
          </el-button>
          <el-button size="mini" type="danger" @click.stop="open(scope.row)">
            <i class="el-icon-close" />
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <div style="text-align: center;margin-top: 30px;">
      <el-pagination
        :current-page="currentPage"
        background
        layout="prev, pager,jumper, next, sizes, total"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        style="margin-bottom:15px"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script>
import request from "@/utils/request";
import global from "@/store/modules/user";

export default {
  data() {
    return {
      tableData: [],
      user_data: [],
      shop_add_form: [],
      title: "",
      month: "",
      loading: true,
      xiaoshou_value: "",
      xiaoshou_options: "",
      cooperation_duration: [
        {
          id: 1,
          label: "1个月",
        },
        {
          id: 2,
          label: "2个月",
        },
        {
          id: 3,
          label: "3个月",
        },
        {
          id: 4,
          label: "4个月",
        },
        {
          id: 5,
          label: "5个月",
        },
        {
          id: 6,
          label: "6个月",
        },
        {
          id: 7,
          label: "7个月",
        },
        {
          id: 8,
          label: "8个月",
        },
        {
          id: 9,
          label: "9个月",
        },
        {
          id: 10,
          label: "10个月",
        },
        {
          id: 11,
          label: "11个月",
        },
        {
          id: 12,
          label: "12个月",
        },
      ],
      total: 0,
      pagesize: 10,
      currentPage: 1,
      drawer: false,
      roles: "",
      formLabelWidth: "80px",
      categorys: [
        {
          id: "美发",
          label: "美发",
        },
        {
          id: "美容/SPA",
          label: "美容/SPA",
        },
        {
          id: "美甲美睫",
          label: "美甲美睫",
        },
        {
          id: "医学美容",
          label: "医学美容",
        },
        {
          id: "瑜伽",
          label: "瑜伽",
        },
        {
          id: "舞蹈",
          label: "舞蹈",
        },
        {
          id: "纹绣",
          label: "纹绣",
        },
        {
          id: "瘦身纤体",
          label: "瘦身纤体",
        },
        {
          id: "纹身",
          label: "纹身",
        },
        {
          id: "祛痘",
          label: "祛痘",
        },
        {
          id: "化妆品",
          label: "化妆品",
        },
        {
          id: "产后塑形",
          label: "产后塑形",
        },
        {
          id: "养发",
          label: "养发",
        },
        {
          id: "全部",
          label: "全部",
        },
      ],
      order_by: 0,
      admin: "",
      search: "",
      shop_edits: [],
      order_edit: {
        contract_id_edit: undefined,
        order_date_edit: undefined,
        order_start_date_edit: undefined,
        sign_contract_shop_edit: undefined,
        customer_source_edit: undefined,
        contract_status_edit: undefined,
        shop_industry_edit: undefined,
        shop_kp_name_edit: undefined,
        shop_telephonenumber_edit: undefined,
        order_numbers_edit: undefined,
        shop_cooperation_duration_edit: undefined,
        cost_fees: undefined,
        shop_kp_wechat_id_edit: undefined,
        tags:undefined,
        order_end_date_edit: undefined,
        order_amount_edit: undefined,
        payment_method_edit: undefined,
        order_contract_sales_edit: undefined,
        shop_remark_edit: undefined,
        order_form_edit: undefined,
        shop_id: undefined,
        order_commission: undefined,
        dialogImageUrl: undefined,
      },
    };
  },
  created: function () {
    this.roles = global.state["avatar"];
    if (
      global.state["avatar"] === "admin" ||
      global.state["avatar"] === "super_admin"
    ) {
      this.get_xiaoshou_data();
    } else {
      this.$router.push({ path: "/dashboard" });
      this.$message.error("暂无权限访问");
    }
    this.addUser();
    this.user_data_xiaoshou();
    this.select_user();
  },
  mounted() {
    this.addUser();
  },
  methods: {
    handleClose(done) {
      this.drawer = false;
    },
    select_user() {
      this.axios
        .get("http://127.0.0.1:8000/app/select_user/", {
          params: {
            username: global.state["first_name"],
          },
        })
        .then((res) => {
          this.admin = res.data.data;
          console.log("admin", this.admin);
        })
        .catch(function (error) {
          this.loading = false;
          console.log(error);
        });
    },
    get_shop_edit(shop_id) {
      console.log(shop_id);
      this.axios
        .get("http://127.0.0.1:8000/app/table_simple_get_edit/", {
          params: {
            // 每页显示的条数
            shop_id: shop_id,
            leixing: "公海",
          },
        })
        .then((res) => {
          this.shop_edits = res.data.data;
          // console.log("编辑信息", this.shop_edits);
        })
        .catch(function (error) {
          this.loading = false;
          console.log(error);
        });
    },
    get_xiaoshou_data() {
      this.axios
        .get("http://127.0.0.1:8000/app/get_xiaoshou_data/", {
          params: {
            // 每页显示的条数
            username: global.state["first_name"],
          },
        })
        .then((body) => {
          this.xiaoshou_options = body.data.data;
        });
    },
    addUser() {
      this.axios
        .get("http://127.0.0.1:8000/app/shenhe_order_select/", {
          params: {
            // 每页显示的条数
            pagesize: this.pagesize,
            // 显示第几页
            currentPage: this.currentPage,
            username: global.state["first_name"],
            search: this.search,
            xiaoshou: this.xiaoshou_value,
          },
        })
        .then((res) => {
          this.tableData = res.data.data;
          this.total = res.data.total;
          this.loading = false;
        })
        .catch(function (error) {
          this.loading = false;
          console.log(error);
        });
    },
    jump_href(row) {
      if (row.order_contract_sales == global.state["first_name"] && global.state["first_name"] != '超级管理员') {
        this.$notify({
          title: "失败",
          message: "不能审核自己的订单",
          type: "error",
        });
      } else {
        this.$confirm("确定审核通过吗? 是否继续?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
          .then(() => {
            this.axios
              .get("http://127.0.0.1:8000/app/create_order/", {
                params: {
                  contract_id: row.contract_id,
                  order_date: row.order_date,
                  order_start_date: row.order_start_date,
                  sign_contract_shop: row.sign_contract_shop,
                  customer_source: row.customer_source,
                  contract_status: row.contract_status,
                  contracted_projects: row.contracted_projects,
                  shop_industry: row.shop_industry,
                  shop_kp_name: row.shop_kp_name,
                  shop_telephonenumber: row.shop_telephonenumber,
                  order_numbers: row.order_numbers,
                  cost_fees: row.cost_fees,
                  shop_cooperation_duration: row.shop_cooperation_duration,
                  order_end_date: row.order_end_date,
                  order_amount: row.order_amount,
                  payment_method: row.payment_method,
                  order_contract_sales: row.order_contract_sales,
                  shop_remark: row.shop_remark,
                  tags:row.tags,
                  order_form: JSON.stringify(row.order_form),
                  shop_id: row.shop_id,
                  city: row.city
                },
              })
              .then((res) => {
                if (res.data.state == 0) {
                  this.$notify({
                    title: "审核成功",
                    message: "审核成功，订单已创建",
                    type: "success",
                  });
                  this.addUser();
                } else {
                  this.$notify({
                    title: "创建失败",
                    message: "原因:" + res.data.msg + ",请联系管理员",
                    type: "error",
                  });
                }
              })
              .catch(function (error) {
                this.$notify({
                  title: "创建失败",
                  message: "创建失败",
                  type: "error",
                });
              });
          })
          .catch(() => {
            this.$notify({
              title: "已取消",
              message: "",
              type: "info",
            });
          });
      }
    },
    select_input() {
      this.addUser();
    },
    select_month() {
      this.addUser();
    },
    xiaoshou_change() {
      this.addUser();
    },
    data_update(row) {
      this.drawer = true;
      this.order_edit.contract_id_edit = row.contract_id;
      this.order_edit.order_date_edit = row.order_date;
      this.order_edit.order_start_date_edit = row.order_start_date;
      this.order_edit.sign_contract_shop_edit = row.sign_contract_shop;
      this.order_edit.customer_source_edit = row.customer_source;
      this.order_edit.contract_status_edit = row.contract_status;
      this.order_edit.contracted_projects_edit = row.contracted_projects;
      this.order_edit.shop_industry_edit = row.shop_industry;
      this.order_edit.shop_kp_name_edit = row.shop_kp_name;
      this.order_edit.shop_telephonenumber_edit = row.shop_telephonenumber;
      this.order_edit.order_numbers_edit = row.order_numbers;
      this.order_edit.shop_cooperation_duration_edit =
        row.shop_cooperation_duration;
      this.order_edit.shop_kp_wechat_id_edit = row.shop_kp_wechat_id;
      this.get_shop_edit(row.shop_id);
      this.order_edit.order_end_date_edit = row.order_end_date;
      this.order_edit.order_amount_edit = row.order_amount;
      this.order_edit.payment_method_edit = row.payment_method;
      this.order_edit.order_contract_sales_edit = row.order_contract_sales;
      this.order_edit.shop_remark_edit = row.shop_remark;
      this.order_edit.order_form_edit = row.order_form;
      this.order_edit.order_commission = row.order_commission;
      this.order_edit.shop_id = row.shop_id;
      this.order_edit.cost_fees = row.cost_fees;
      this.shop_add_form = row.order_form;
      this.order_edit.dialogImageUrl = row.dialogImageUrl;
    },
    edit_shop_add_form(index, value) {
      this.axios
        .get("http://127.0.0.1:8000/app/edit_order_form_data/", {
          params: {
            // 每页显示的条数
            shop_id: this.order_edit.sign_contract_shop_edit,
            index: index,
            value: value,
          },
        })
        .then((res) => {})
        .catch(function (error) {
          this.loading = false;
          console.log(error);
        });
    },
    user_data_xiaoshou() {
      this.axios
        .get("http://127.0.0.1:8000/app/get_xiaoshou_data/", {
          params: {
            // 每页显示的条数
            username: global.state["first_name"],
          },
        })
        .then((res) => {
          this.user_data = res.data.data;
        })
        .catch(function (error) {
          this.loading = false;
          console.log(error);
        });
    },
    open(row) {
      this.$prompt("请输入审核不通过原因", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /\S/,
        inputErrorMessage: "不能为空",
      })
        .then(({ value }) => {
          this.$confirm("确定审核失败吗? 是否继续?", "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning",
          }).then(() => {
            this.axios
              .get("http://127.0.0.1:8000/app/delete_shenhe/", {
                params: {
                  order_id: row.contract_id,
                  value: value,
                  username: row.order_contract_sales,
                  tags: row.tags,
                  sign_contract_shop: row.sign_contract_shop,
                  city: row.city,
                  order_numbers: row.order_numbers,
                  shop_cooperation_duration: row.shop_cooperation_duration,
                  order_amount: row.order_amount,
                  order_form: JSON.stringify(row.order_form),
                },
              })
              .then((res) => {
                if (res.data.state == 0) {
                  this.$notify({
                    title: "提交成功",
                    message: "",
                    type: "success",
                  });
                  this.addUser();
                } else {
                  this.$notify({
                    title: "提交失败",
                    message: "",
                    type: "error",
                  });
                }
              })
              .catch(function (error) {
                this.$notify({
                  title: "已取消",
                  message: "",
                  type: "info",
                });
              });
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消输入",
          });
        });
    },
    delete_order(row) {
      console.log(row);
      this.$confirm("确定要删除订单吗? 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
        this.axios
          .get("http://127.0.0.1:8000/app/delete_order/", {
            params: {
              order_id: row.contract_id,
              shop_id: row.shop_id,
            },
          })
          .then((res) => {
            if (res.data.state == 1) {
              this.$notify({
                title: "删除成功",
                message: "",
                type: "success",
              });
              this.addUser();
            } else {
              this.$notify({
                title: "删除失败",
                message: "",
                type: "error",
              });
            }
          })
          .catch(function (error) {
            this.loading = false;
            console.log(error);
          });
      });
    },
    sortChange: function (column, prop, order) {
      this.order_by = column.order;
      this.addUser();
    },
    // 分页
    // 每页显示的条数
    handleSizeChange(val) {
      // 改变每页显示的条数
      this.pagesize = val;
      // 点击每页显示的条数时，显示第一页
      this.addUser();
      this.qryTableDate();
      // 注意：在改变每页显示的条数时，要将页码显示到第一页
    },
    // 显示第几页
    handleCurrentChange(val) {
      console.log("第几页", val);
      // 改变默认的页数
      this.currentPage = val;
      // 切换页码时，要获取每页显示的条数
      this.addUser();
      this.qryTableDate();
    },
  },
};
</script>
<style>
.el-drawer {
  overflow-y: auto;
  width: 51%;
}
@media only screen and (max-width: 500px) {
  .el-drawer {
    width: 100%;
  }
}
</style>
