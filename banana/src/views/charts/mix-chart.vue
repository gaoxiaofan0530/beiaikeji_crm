<template>
  <div @click="noclick">
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
              ref="chooseKpi55"
              @blur="chooseKpi55"
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
          <el-form-item label="签约销售" :label-width="formLabelWidth">
            <el-input
              v-model="order_edit.order_contract_sales_edit"
              style="width:80%"
              placeholder="签约销售"
              :disabled="true"
            />
          </el-form-item>
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
          <el-divider />
          <el-form-item label="操作" :label-width="formLabelWidth">
            <el-tooltip class="item" effect="dark" content="订单编辑" placement="top-start">
                <el-button
                  size="medium"
                  type="success"
                  content="订单编辑"
                  placement="top"
                  @click="update_order()"
                >
                  <i class="el-icon-edit-outline" />
                </el-button>
            </el-tooltip>
            <el-tooltip class="item" effect="dark" content="切换销售" placement="top-start">
              <el-button
                size="medium"
                type="warning"
                content="切换销售"
                placement="top"
                @click="transfer_order()"
              >
                <svg-icon icon-class="qiehuan" />
              </el-button>
            </el-tooltip>
            <el-tooltip class="item" effect="dark" content="订单删除" placement="top-start">
              <el-button
                size="medium"
                type="danger"
                content="订单删除"
                placement="top"
                @click="delete_order()"
              >
                <i class="el-icon-delete" />
              </el-button>
            </el-tooltip>
          </el-form-item>
        </el-form>
      </div>
    </el-drawer>
    <el-dialog title="订单修改" :visible.sync="dialogFormVisible_update" width="50%"> 
      <el-form ref="update" :rules="rules_update" :model="update" label-width="100px">
        <el-form-item label="订单ID">
          <el-input v-model="order_edit.contract_id_edit" :disabled="true" autocomplete="off" style="width:80%"/>
        </el-form-item>
        <el-form-item label="店名">
          <el-input v-model="order_edit.sign_contract_shop_edit" :disabled="true" autocomplete="off" style="width:80%"/>
        </el-form-item>
        <el-form-item label="下单日期" prop="order_date_edit">
          <el-date-picker
              class="diangdan"
              v-model="update.order_date_edit"
              type="date"
              placeholder="选择日期"
              ref="datePicker_update1"
              @focus="datePicker_click1"
              style="width:80%"
          />
          <!-- <el-input class="diangdan" v-model="order_edit.order_date_edit" autocomplete="off" /> -->
        </el-form-item>
        <el-form-item label="开始日期"  prop="order_start_date_edit">
          <el-date-picker
              class="diangdan"
              v-model="update.order_start_date_edit"
              type="date"
              placeholder="选择日期"
              ref="datePicker_update2"
              @focus="datePicker_click2"
              @change="change_order_date"
              style="width:80%"
          />
        </el-form-item>
        <el-form-item label="合作时长" prop="shop_cooperation_duration_edit">
          <el-select
          v-model="update.shop_cooperation_duration_edit"
          filterable
          ref="chooseKpi5"
          class="diangdan"
          value-key="id"
          placeholder="请选合作时长"
          @blur="chooseKpi5"
          style="width:80%"
          @change="change_shop_cooperation_duration"
        >
          <el-option
            v-for="item in cooperation_duration"
            :key="item.id"
            :label="item.label"
            :value="item"
          />
        </el-select>
        </el-form-item>
        <el-form-item label="结束日期">
          <el-input v-model="order_edit.order_end_date_edit" :disabled="true" autocomplete="off" style="width:80%"/>
        </el-form-item>
        <el-form-item label="门店数">
          <el-input v-model="order_edit.order_numbers_edit" :disabled="true" autocomplete="off" style="width:80%"/>
        </el-form-item>
        <el-form-item label="签约金额" prop="order_amount_edit">
          <el-input class="diangdan" v-model="update.order_amount_edit" autocomplete="off" style="width:80%"/>
        </el-form-item>
        <el-form-item label="成本费" prop="cost_fees">
          <el-input class="diangdan" v-model="update.cost_fees" autocomplete="off" style="width:80%"/>
        </el-form-item>
        <el-form-item label="城市">
          <el-input v-model="order_edit.city"  :disabled="true" autocomplete="off" style="width:80%"/>
        </el-form-item>
        <el-form-item label="签约销售">
            <el-input
              v-model="order_edit.order_contract_sales_edit"
              placeholder="签约销售"
              :disabled="true"
              style="width:80%"
            />
        </el-form-item>
        <el-form-item
          v-for="(domain, index) in shop_add_form"
          :key="domain.key"
          :label="domain.label"
        >
            <span v-if="domain.type === '文本类型'">
              <el-input
                v-model="domain.value"
                :disabled="true"
                style="width:80%"
                @blur="edit_shop_add_form(index,domain.value)"
              />
            </span>
            <span v-if="domain.type === '日期类型'">
              <el-date-picker
                v-model="domain.value"
                type="date"
                placeholder="选择日期"
                :disabled="true"
                style="width:80%"
                @change="edit_shop_add_form(index,domain.value)"
              />
            </span>
            <span v-if="domain.type === '选择下拉框'">
              <el-select
                v-model="domain.value"
                type="date"
                :disabled="true"
                placeholder="选择内容"
                style="width:80%"
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
                style="width:80%"
                @blur="edit_shop_add_form(index,domain.value)"
              />
            </span>
        </el-form-item>
        <el-form-item label="备注" :disabled="true">
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
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible_update = false">取 消</el-button>
        <el-button type="primary" @click="update_order_ok('update');resetForm()">确 定</el-button>
      </div>
    </el-dialog>
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
      <span v-if="roles === 'admin' || roles === 'super_admin'">
        <el-select ref="chooseKpi4" v-model="xiaoshou_value" @blur="city_select" clearable filterable placeholder="请选择" @change="xiaoshou_change(xiaoshou_value)">
          <el-option
            v-for="item in xiaoshou_options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </span>
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
          <div v-else-if="row.tags === '退款中'">
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
            <el-tag type="warning" effect="dark">{{ row.tags }}</el-tag>
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
        sortable
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
      <!-- <el-table-column label="操作" width="210" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <span v-if="roles === 'super_admin' || roles === 'admin'">
            <el-tooltip class="item" effect="dark" content="删除" placement="top-start">
              <el-button
                size="mini"
                type="danger"
                content="删除"
                placement="top"
                @click.stop="delete_order(scope.row)"
              >
                <i class="el-icon-delete" />
              </el-button>
            </el-tooltip>
          </span>
          <el-tooltip class="item" effect="dark" content="详细数据" placement="top-start">
            <el-button
              size="mini"
              type="success"
              content="详细数据"
              placement="top"
              @click="pull_get(scope.row);"
            >
              <i class="el-icon-edit-outline" />
            </el-button>
          </el-tooltip>
          <span v-if="roles === 'super_admin' || roles === 'admin'">
            <el-tooltip class="item" effect="dark" content="切换销售" placement="top-start">
              <el-button
                size="mini"
                type="warning"
                content="切换销售"
                placement="top"
                @click.stop="transfer_order(scope.row);"
              >
                <i class="el-icon-refresh-left" />
              </el-button>
            </el-tooltip>
          </span>
        </template>
      </el-table-column> -->
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
    <el-dialog title="订单转移" :visible.sync="dialogFormVisible">
      <el-form ref="form" :model="form" :rules="rules">
        <el-form-item label="当前销售" :label-width="formLabelWidth">
          <el-input v-model="now_admin" style="width:100%" placeholder :disabled="true" />
        </el-form-item>
        <el-form-item
          label="转移销售"
          :label-width="formLabelWidth"
          prop="xiaoshou_value_transfer"
        >
          <el-select v-model="form.xiaoshou_value_transfer" ref="chooseKpi44" @blur="chooseKpi44" clearable filterable placeholder="请选择要转给谁">
            <el-option
              v-for="item in xiaoshou_options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="transfer_update('form')">确 定</el-button>
      </div>
    </el-dialog>
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
      dialogFormVisible_update:false,
      form: {
        xiaoshou_value_transfer: ''
      },
      title: '',
      month:'',
      loading: true,
      xiaoshou_value:'',
      xiaoshou_options:'',
      cooperation_duration: [
        {
          id: 1,
          label: '1个月'
        },
        {
          id: 2,
          label: '2个月'
        },
        {
          id: 3,
          label: '3个月'
        },
        {
          id: 4,
          label: '4个月'
        },
        {
          id: 5,
          label: '5个月'
        },
        {
          id: 6,
          label: '6个月'
        },
        {
          id: 7,
          label: '7个月'
        },
        {
          id: 8,
          label: '8个月'
        },
        {
          id: 9,
          label: '9个月'
        },
        {
          id: 10,
          label: '10个月'
        },
        {
          id: 11,
          label: '11个月'
        },
        {
          id: 12,
          label: '12个月'
        }
      ],
      total: 0,
      pagesize: 10,
      currentPage: 1,
      count:1,
      drawer: false,
      roles:'',
      formLabelWidth: '80px',
      dialogFormVisible:false,
      categorys: [
        {
          id: '美发',
          label: '美发'
        },
        {
          id: '美容/SPA',
          label: '美容/SPA'
        },
        {
          id: '美甲美睫',
          label: '美甲美睫'
        },
        {
          id: '医学美容',
          label: '医学美容'
        },
        {
          id: '瑜伽',
          label: '瑜伽'
        },
        {
          id: '舞蹈',
          label: '舞蹈'
        },
        {
          id: '纹绣',
          label: '纹绣'
        },
        {
          id: '瘦身纤体',
          label: '瘦身纤体'
        },
        {
          id: '纹身',
          label: '纹身'
        },
        {
          id: '祛痘',
          label: '祛痘'
        },
        {
          id: '化妆品',
          label: '化妆品'
        },
        {
          id: '产后塑形',
          label: '产后塑形'
        },
        {
          id: '养发',
          label: '养发'
        },
        {
          id: '全部',
          label: '全部'
        }
      ],
      order_by: 0,
      row:'',
      now_admin:'',
      admin: '',
      shop_edits:[],
      update:{
        contract_id: undefined,
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
        cost_fees:undefined,
        city:undefined,
        shop_kp_wechat_id_edit: undefined,
        order_end_date_edit: undefined,
        order_amount_edit: undefined,
        payment_method_edit: undefined,
        order_contract_sales_edit: undefined,
        shop_remark_edit: undefined,
        order_form_edit: undefined,
        shop_id: undefined,
        order_commission: undefined
      },
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
        cost_fees:undefined,
        city:undefined,
        shop_kp_wechat_id_edit: undefined,
        order_end_date_edit: undefined,
        order_amount_edit: undefined,
        payment_method_edit: undefined,
        order_contract_sales_edit: undefined,
        shop_remark_edit: undefined,
        order_form_edit: undefined,
        shop_id: undefined,
        order_commission: undefined,
        tags: undefined
      },
      rules: {
        xiaoshou_value_transfer: [
          { required: true, message: '请选择要转移到的销售', trigger: 'blur' }
        ]
      },
      rules_update:{
        order_date_edit: [
          { required: true, message: '请选择签约时间', trigger: 'blur' }
        ],
        order_start_date_edit: [
          { required: true, message: '请选择开始时间', trigger: 'blur' }
        ],
        shop_cooperation_duration_edit: [
          { required: true, message: '请选择合作时长', trigger: 'blur' }
        ],
        order_amount_edit: [
          { required: true, message: '请输入签约金额', trigger: 'blur' }
        ],
        cost_fees: [
          { required: true, message: '请输入成本费', trigger: 'blur' }
        ],
      },
      cooperation_duration: [
        {
          id: 1,
          label: '1个月'
        },
        {
          id: 2,
          label: '2个月'
        },
        {
          id: 3,
          label: '3个月'
        },
        {
          id: 4,
          label: '4个月'
        },
        {
          id: 5,
          label: '5个月'
        },
        {
          id: 6,
          label: '6个月'
        },
        {
          id: 7,
          label: '7个月'
        },
        {
          id: 8,
          label: '8个月'
        },
        {
          id: 9,
          label: '9个月'
        },
        {
          id: 10,
          label: '10个月'
        },
        {
          id: 11,
          label: '11个月'
        },
        {
          id: 12,
          label: '12个月'
        },
        {
          id: 13,
          label: '13个月'
        },
        {
          id: 14,
          label: '14个月'
        },
        {
          id: 15,
          label: '15个月'
        },
        {
          id: 16,
          label: '16个月'
        },
        {
          id: 17,
          label: '17个月'
        },
        {
          id: 18,
          label: '18个月'
        },
        {
          id: 19,
          label: '19个月'
        },
        {
          id: 20,
          label: '20个月'
        },
        {
          id: 21,
          label: '21个月'
        },
        {
          id: 22,
          label: '22个月'
        },
        {
          id: 23,
          label: '23个月'
        },
        {
          id: 24,
          label: '24个月'
        }
      ],
    }
  },
  created: function() {
    this.roles = global.state['avatar']
    if (global.state['avatar'] === 'admin' || global.state['avatar'] === 'super_admin') {
      this.get_xiaoshou_data()
    }
    this.addUser()
    this.user_data_xiaoshou()
    this.select_user()
  },
  methods: {
    chooseKpi55(){
      this.$refs.chooseKpi55.blur();
    },
    chooseKpi5(){
      this.$refs.chooseKpi5.blur();
    },
    noclick(val){
      if (this.count == 1){
        this.count = 3
      }else if (this.count == 3){
        this.$refs.datePicker.hidePicker();
        this.$refs.datePicker_update1.hidePicker();
        this.$refs.datePicker_update2.hidePicker();
        this.count = 1
      }
    },
    datePicker_click(){
      this.count = 1
    },
    datePicker_click1(){
      this.count = 1
    },
    datePicker_click2(){
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
    city_select() {
      this.$refs.chooseKpi4.blur();
    },
    chooseKpi44(){
      this.$refs.chooseKpi44.blur();
    },
    select_user() {
      this.axios
        .get('http://127.0.0.1:8000/app/select_user/', {
          params: {
            username: global.state['first_name']
          }
        })
        .then(res => {
          this.admin = res.data.data
          console.log('admin', this.admin)
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    transfer_order() {
      this.now_admin = this.order_edit.order_contract_sales_edit
      this.$confirm('确定要转移任务吗? 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.dialogFormVisible = true
      })
    },
    transfer_update(formName) {
      this.$confirm('确定要转移订单吗? 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.axios
              .get('http://127.0.0.1:8000/app/transfer_update_order/', {
                params: {
                  order_id: this.order_edit.contract_id_edit,
                  username: this.form.xiaoshou_value_transfer,
                }
              })
              .then(res => {
                if (res.data.state == 1) {
                  this.dialogFormVisible = false
                  this.$notify({
                    title: '转移成功',
                    message: '',
                    type: 'success'
                  })
                  this.order_edit.order_contract_sales_edit = this.form.xiaoshou_value_transfer
                  this.addUser()
                  this.form.xiaoshou_value_transfer = ''
                } else {
                  this.$notify({
                    title: '转移失败',
                    message: '',
                    type: 'error'
                  })
                }
              })
              .catch(function(error) {
                this.loading = false
                console.log(error)
              })
          } else {
            console.log('error submit!!')
            return false
          }
        })
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
    get_xiaoshou_data() {
      this.axios
        .get('http://127.0.0.1:8000/app/get_xiaoshou_data/',{
          params: {
            // 每页显示的条数
            username: global.state['first_name']
          }
        })
        .then(body => {
          this.xiaoshou_options = body.data.data
        })
    },
    addUser(n1, n2) {
      this.axios
        .get('http://127.0.0.1:8000/app/table_simple_order_data_all/', {
          params: {
            // 每页显示的条数
            pagesize: this.pagesize,
            // 显示第几页
            currentPage: this.currentPage,
            username: this.xiaoshou_value,
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
            payment_method: payment_method,
            shop_remark: shop_remark
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
            this.currentPage
          )
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    select_input() {
      console.log(this.title)
      this.loading = true;
      this.addUser(
        this.pagesize,
        this.currentPage
      )
    },
    select_month() {
      this.loading = true;
      this.addUser(
        this.pagesize,
        this.currentPage
      )
    },
    xiaoshou_change() {
      this.loading = true;
      this.addUser(
        this.pagesize,
        this.currentPage
      )
      this.$forceUpdate();
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
      this.order_edit.shop_cooperation_duration_edit = row.shop_cooperation_duration
      this.order_edit.shop_kp_wechat_id_edit = row.shop_kp_wechat_id
      this.get_shop_edit(row.shop_id)
      this.order_edit.order_end_date_edit = row.order_end_date
      this.order_edit.order_amount_edit = row.order_amount
      this.order_edit.payment_method_edit = row.payment_method
      this.order_edit.order_contract_sales_edit = row.order_contract_sales
      this.order_edit.shop_remark_edit = row.shop_remark
      this.order_edit.order_form_edit = row.order_form
      this.order_edit.order_commission = row.order_commission
      this.order_edit.shop_id = row.shop_id
      this.order_edit.cost_fees = row.cost_fees
      this.order_edit.city = row.city
      this.order_edit.tags = row.tags
      this.shop_add_form = row.order_form
      this.update.order_start_date_edit = row.order_start_date
    },
    update_order(){
      if (global.state['avatar'] != 'super_admin' && global.state['avatar'] != 'admin'){
        this.$notify({
          title: '没有权限',
          type: 'error'
        });
      }else{
        this.$confirm('确定要修改订单吗? 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.update.order_date_edit = this.order_edit.order_date_edit
          this.update.order_start_date_edit = this.order_edit.order_start_date_edit
          this.update.shop_cooperation_duration_edit = this.order_edit.shop_cooperation_duration_edit
          this.update.order_amount_edit = this.order_edit.order_amount_edit
          this.update.cost_fees = this.order_edit.cost_fees
          this.dialogFormVisible_update=true
        })
      }
    },
    update_order_ok(formName){
      this.$refs[formName].validate((valid) => {
          if (valid) {
            // if (this.update.shop_cooperation_duration_edit.id == undefined){
            //     this.update.shop_cooperation_duration_edit = this.order_edit.shop_cooperation_duration_edit
            // }
            console.log(this.order_edit.shop_cooperation_duration_edit)
            console.log(this.update.shop_cooperation_duration_edit)
            this.axios
              .get('http://127.0.0.1:8000/app/create_tuikuan_order/', {
                params: {
                    order_date_before: this.order_edit.order_date_edit,
                    order_date_after: this.update.order_date_edit,
                    order_start_date_before:this.order_edit.order_start_date_edit,
                    order_start_date_after:this.update.order_start_date_edit,
                    shop_cooperation_duration_before:this.order_edit.shop_cooperation_duration_edit,
                    shop_cooperation_duration_after:this.update.shop_cooperation_duration_edit,
                    order_amount_before:this.order_edit.order_amount_edit,
                    order_amount_after:this.update.order_amount_edit,
                    cost_fees_before:this.order_edit.cost_fees,
                    cost_fees_after:this.update.cost_fees,
                    order_id:this.order_edit.contract_id_edit,
                    order_contract_sales:this.order_edit.order_contract_sales_edit,
                    order_end_date:this.order_edit.order_end_date_edit,
                    sign_contract_shop:this.order_edit.sign_contract_shop_edit,
                    tags:this.order_edit.tags,
                    username:global.state['first_name'],
                    shop_name:this.order_edit.sign_contract_shop_edit
                }
              })
              .then(res => {
                if (res.data.state == 1){
                  this.$notify({
                    title: '已经提交过退款申请，请耐心等待审核',
                    type: 'warning'
                  });
                }else if (res.data.state == 2){
                  this.$notify({
                    title: '提交退款申请成功',
                    type: 'success'
                  });
                  this.addUser(
                    this.pagesize,
                    this.currentPage
                  )
                }
                this.dialogFormVisible_update=false
              })
          } else {
            console.log('error submit!!')
            return false
          }
        })
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
        })
    },
    user_data_xiaoshou() {
      this.axios
        .get('http://127.0.0.1:8000/app/get_xiaoshou_data/',{
          params: {
            // 每页显示的条数
            username: global.state['first_name']
          }
        })
        .then(res => {
          this.user_data = res.data.data
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    delete_order() {
      this.$confirm('确定要删除订单吗? 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.axios
          .get('http://127.0.0.1:8000/app/delete_order/', {
            params: {
              order_id: this.order_edit.contract_id_edit,
              shop_id: this.order_edit.shop_id
            }
          })
          .then(res => {
            if (res.data.state == 1) {
              this.$notify({
                title: '删除成功',
                message: '',
                type: 'success'
              })
              this.addUser(
                this.pagesize,
                this.currentPage
              )
            } else {
              this.$notify({
                title: '删除失败',
                message: '',
                type: 'error'
              })
            }
          })
          .catch(function(error) {
            this.loading = false
            console.log(error)
          })
      })
    },
    sortChange: function(column, prop, order) {
      this.loading = true;
      this.order_by = column.order
      this.addUser(this.pagesize, this.currentPage)
    },
    // 分页
    // 每页显示的条数
    handleSizeChange(val) {
      // 改变每页显示的条数
      this.pagesize = val
      // 点击每页显示的条数时，显示第一页
      this.loading = true
      this.addUser(val, this.currentPage)
      this.qryTableDate()
      // 注意：在改变每页显示的条数时，要将页码显示到第一页
    },
    // 显示第几页
    handleCurrentChange(val) {
      // 改变默认的页数
      this.currentPage = val
      this.loading = true
      // 切换页码时，要获取每页显示的条数
      this.addUser(this.pagesize, val)
      this.qryTableDate()
    },  
    change_shop_cooperation_duration(data) {
      this.order_edit.order_end_date_edit = this.computeYmd(
        this.update.order_start_date_edit,
        this.update.shop_cooperation_duration_edit.id

      )
      this.update.shop_cooperation_duration_edit = this.update.shop_cooperation_duration_edit.id
    },
    computeYmd(val, data) {
      const str = val.split('-')
      var d = new Date(str[0], str[1], str[2])
      // 因为getMonth()获取的月份的值只能在0~11之间所以我们在进行setMonth()之前先给其减一
      d.setMonth(d.getMonth() - 1 + data)
      var yy1 = d.getFullYear()
      var mm1 = d.getMonth() + 1
      console.log(mm1)
      var dd1 = d.getDate()
      console.log(mm1)
      if (mm1 < 10) {
        mm1 = '0' + mm1
      }
      if (dd1 < 10) {
        dd1 = '0' + dd1
      }
      return yy1 + '-' + mm1 + '-' + dd1
    },
    change_order_date(data) {
      if (this.update.shop_cooperation_duration_edit.id == undefined){
        data = this.update.shop_cooperation_duration_edit
      }else{
        data = this.update.shop_cooperation_duration_edit.id
      }
      if (this.update.shop_cooperation_duration_edit == '') {
        console.log('为空')
      } else {
        this.order_edit.order_end_date_edit = this.computeYmd(
          this.update.order_start_date_edit.getFullYear() +
            '-' +
            (this.update.order_start_date_edit.getMonth() + 1) +
            '-' +
            (this.update.order_start_date_edit.getDate()),
          Number(data)
        )
      }
    },
  }
}
</script>
<style>
.el-drawer {
  overflow-y: auto;
  width: 51%;
}
.diangdan input.el-input__inner {
  border-color:#fede4d
}
@media only screen and (max-width : 500px) {
  .el-drawer {
    width: 100%;
  }
}
</style>
