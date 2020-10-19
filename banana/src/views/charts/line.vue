<template>
  <div @click="noclick">
    <el-drawer
      class="drawer"
      title="订单详情"
      :visible.sync="drawer"
      :direction="direction"
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
          <el-form-item label="商户ID" :label-width="formLabelWidth">
            <el-input
              v-model="order_edit.shop_id"
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
              label="描述文字"
              :disabled="true"
              @change="handleChange"
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
          <el-form-item label="所在城市" :label-width="formLabelWidth">
            <el-input
              v-model="order_edit.city"
              style="width:80%"
              placeholder="未标注城市"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="提成" :label-width="formLabelWidth">
            <el-input
              v-model="order_edit.order_commission"
              autocomplete="off"
              style="width:80%"
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
              <el-input v-model="domain.value" :disabled="true" @blur="edit_shop_add_form(index,domain.value)" />
            </span>
            <span v-if="domain.type === '日期类型'">
              <el-date-picker
                v-model="domain.value"
                type="date"
                :disabled="true"
                placeholder="选择日期"
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
                type="textarea"
                :disabled="true"
                @blur="edit_shop_add_form(index,domain.value)"
              />
            </span>
          </el-form-item>
          <el-divider>备注</el-divider>
          <el-form-item label="备注" :label-width="formLabelWidth">
            <el-input v-model="order_edit.shop_remark_edit" type="textarea" placeholder="备注信息" />
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
      <el-input
        v-model="title"
        style="width: 200px;"
        placeholder="查询"
        @input="select_input"
      >
        <i slot="prefix" class="el-input__icon el-icon-search" />
      </el-input>
      <el-date-picker
        ref="datePicker"
        v-model="month"
        type="month"
        @change="select_month"
        @focus="datePicker_click"
        placeholder="选择月">
      </el-date-picker>
      <!-- <span v-if="roles === 'admin'">
        <el-select v-model="xiaoshou_value" clearable filterable placeholder="请选择" @change="xiaoshou_change(xiaoshou_value)">
          <el-option
            v-for="item in xiaoshou_options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </span> -->
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
        show-overflow-tooltip
        label="签约商户"
        width="450"
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
          </div> -->
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
        prop="remaining_number_of_days"
        show-overflow-tooltip
        label="剩余天数"
        @click="data_update(row);drawer = true"
      >
        <template slot-scope="{row}">
          <div v-if="row.zhuangtai === '已到期'">
            <span
              class="link-type"
              style="color:#008000"
              @click="data_update(row);drawer = true"
            >{{ row.remaining_number_of_days }}</span>
          </div>
          <div v-else>
            <span
              class="link-type"
              style="color:#FF0000"
              @click="data_update(row);drawer = true"
            >{{ row.remaining_number_of_days }}</span>
          </div>
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
import request from '@/utils/request'
import global from '@/store/modules/user'

export default {
  data() {
    return {
      tableData: [],
      user_data: [],
      shop_add_form: [],
      shop_edits:[],
      loading: true,
      total: 0,
      pagesize: 10,
      currentPage: 1,
      title: '',
      count:1,
      month:'',
      drawer: false,
      formLabelWidth: '80px',
      order_by: 0,
      order_edit: {
        contract_id_edit: undefined,
        order_date_edit: undefined,
        order_start_date_edit: undefined,
        sign_contract_shop_edit: undefined,
        customer_source_edit: undefined,
        contract_status_edit: undefined,
        shop_industry_edit: undefined,
        shop_kp_name_edit: undefined,
        cost_fees:undefined,
        shop_telephonenumber_edit: undefined,
        order_numbers_edit: undefined,
        shop_cooperation_duration_edit: undefined,
        shop_kp_wechat_id_edit: undefined,
        order_end_date_edit: undefined,
        order_amount_edit: undefined,
        payment_method_edit: undefined,
        city:undefined,
        order_contract_sales_edit: undefined,
        shop_remark_edit: undefined,
        shop_id: undefined,
        order_form_edit: undefined,
        order_commission: undefined
      }
    }
  },
  created: function() {
    this.addUser(this.pagesize, this.currentPage, global.state['first_name'])
    this.user_data_xiaoshou()
  },
  mounted() {
    this.addUser()
  },
  methods: {
    noclick(){
      console.log(this.count)
      if (this.count == 1){
        this.count = 3
      }else if (this.count == 3){
        this.$refs.datePicker.hidePicker();
        this.count = 1
      }
    },
    datePicker_click(){
      this.count = 1
    },
    handleClose(done) {
      this.drawer = false
      this.edit_shop(
        this.order_edit.contract_id_edit,
        this.order_edit.customer_source_edit,
        this.order_edit.contract_status_edit,
        this.order_edit.contracted_projects_edit,
        this.order_edit.shop_industry_edit,
        this.order_edit.shop_kp_name_edit,
        this.order_edit.shop_telephonenumber_edit,
        this.order_edit.order_numbers_edit,
        this.order_edit.payment_method_edit,
        this.order_edit.shop_id,
        this.order_edit.shop_remark_edit
      )
    },
    addUser(n1, n2, username) {
      this.axios
        .get('http://127.0.0.1:8000/app/table_simple_order_data/', {
          params: {
            // 每页显示的条数
            pagesize: n1,
            // 显示第几页
            currentPage: n2,
            username: global.state['first_name'],
            order_by: this.order_by,
            title: this.title,
            month: this.month
          }
        })
        .then(res => {
          this.tableData = res.data.data
          this.total = res.data.total
          this.loading = false
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    get_shop_edit(shop_id) {
      this.axios
        .get('http://127.0.0.1:8000/app/table_simple_get_edit/', {
          params: {
            // 每页显示的条数
            shop_id: shop_id,
            leixing: '公海'
          }
        })
        .then(res => {
          this.shop_edits = res.data.data
          // console.log("编辑信息", this.shop_edits);
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    edit_shop(
      contract_id,
      customer_source,
      contract_status,
      contracted_projects,
      shop_industry,
      shop_kp_name,
      shop_telephonenumber,
      order_numbers,
      payment_method,
      shop_id,
      shop_remark
    ) {
      this.axios
        .get('http://127.0.0.1:8000/app/order_select/', {
          params: {
            contract_id: contract_id,
            customer_source: customer_source,
            contract_status: contract_status,
            contracted_projects: contracted_projects,
            shop_industry: shop_industry,
            shop_kp_name: shop_kp_name,
            shop_telephonenumber: shop_telephonenumber,
            order_numbers: order_numbers,
            shop_id: shop_id,
            payment_method: payment_method,
            shop_remark: shop_remark,
            user_name: global.state['first_name']
          }
        })
        .then(res => {
          this.$notify({
            title: '操作成功',
            message: '',
            type: 'success'
          })
          this.addUser(
            this.pagesize,
            this.currentPage,
            global.state['first_name']
          )
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    data_update(row) {
      this.drawer = true
      this.order_edit.contract_id_edit = row.contract_id
      this.order_edit.order_date_edit = row.order_date
      this.order_edit.order_start_date_edit = row.order_start_date
      this.order_edit.sign_contract_shop_edit = row.sign_contract_shop
      this.order_edit.customer_source_edit = row.customer_source
      this.order_edit.contract_status_edit = row.contract_status
      this.order_edit.contracted_projects_edit = row.contracted_projects
      this.order_edit.shop_industry_edit = row.shop_industry
      this.order_edit.shop_kp_name_edit = row.shop_kp_name
      this.order_edit.shop_telephonenumber_edit = row.shop_telephonenumber
      this.order_edit.order_numbers_edit = row.order_numbers
      this.order_edit.shop_cooperation_duration_edit =
        row.shop_cooperation_duration
      this.order_edit.shop_kp_wechat_id_edit = row.shop_kp_wechat_id
      this.get_shop_edit(row.shop_id)
      this.order_edit.order_end_date_edit = row.order_end_date
      this.order_edit.order_amount_edit = row.order_amount
      this.order_edit.payment_method_edit = row.payment_method
      this.order_edit.order_contract_sales_edit = row.order_contract
      this.order_edit.shop_remark_edit = row.shop_remark
      this.order_edit.order_form_edit = row.order_form
      this.order_edit.shop_id = row.shop_id
      this.order_edit.order_commission = row.order_commission
      this.shop_add_form = row.order_form
      this.order_edit.cost_fees = row.cost_fees
      this.order_edit.city = row.city
    },
    edit_shop_add_form(index, value) {
      this.axios
        .get('http://127.0.0.1:8000/app/edit_order_form_data/', {
          params: {
            // 每页显示的条数
            shop_id: this.order_edit.sign_contract_shop_edit,
            index: index,
            value: value
          }
        })
        .then(res => {})
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    select_input() {
      this.addUser(
        this.pagesize,
        this.currentPage,
        global.state['first_name']
      )
    },
    select_month() {
      this.addUser(
        this.pagesize,
        this.currentPage,
        global.state['first_name']
      )
    },
    user_data_xiaoshou() {
      this.axios
        .get('http://127.0.0.1:8000/app/get_user_data/', {})
        .then(res => {
          this.user_data = res.data.data
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    sortChange: function(column, prop, order) {
      this.order_by = column.order
      this.addUser(this.pagesize, this.currentPage, global.state['first_name'])
    },
    // 分页
    // 每页显示的条数
    handleSizeChange(val) {
      // 改变每页显示的条数
      this.pagesize = val
      this.loading = true
      // 点击每页显示的条数时，显示第一页
      this.addUser(val, this.currentPage, global.state['first_name'])
      this.qryTableDate()
      // 注意：在改变每页显示的条数时，要将页码显示到第一页
    },
    // 显示第几页
    handleCurrentChange(val) {
      console.log('第几页', val)
      // 改变默认的页数
      this.currentPage = val
      this.loading = true
      // 切换页码时，要获取每页显示的条数
      this.addUser(this.pagesize, val, global.state['first_name'])
      this.qryTableDate()
    }
  }
}
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
