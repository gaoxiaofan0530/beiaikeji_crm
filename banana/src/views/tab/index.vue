<template>
  <div class="dashboard-editor-container" ref="box" @click="noclick">
    <el-date-picker
      ref="datePicker"
      v-model="month_data"
      type="month"
      placeholder="选择月"
      value-format="yyyy-MM"
      @change="formatTime"
      @focus="datePicker_click"
    />
    <span v-if="roles === 'admin' || roles === 'super_admin'">
      <el-select
        ref="chooseKpi"
        @blur="type_select"
        v-model="xiaoshou_value"
        clearable
        filterable
        placeholder="请选择"
        @change="xiaoshou_change(xiaoshou_value)"
      >
        <el-option
          v-for="item in xiaoshou_options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </span>
    <span v-if="roles === 'super_admin'">
      <el-button type="primary" @click="open_jj();">剩余待发奖金</el-button>
    </span>
    <el-row :gutter="40" class="panel-group">
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel" @click="handleSetLineChartData('newVisitis')">
          <div class="card-panel-icon-wrapper icon-people">
            <svg-icon icon-class="money" class-name="card-panel-icon" />
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">本月业绩</div>
            <div class="card-panel-num">{{ cost_fees }}</div>
            <span class="card-panel-num2">-</span>
            <div class="card-panel-num">{{ table_simple_data }}</div>
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">提成点</div>
            <span class="card-panel-num2">%</span>
            <div class="card-panel-num">{{ commission_point }}</div>
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">本月提成</div>
            <div class="card-panel-num">{{ table_simple_data_signing }}</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel" @click="handleSetLineChartData('messages')">
          <div class="card-panel-icon-wrapper icon-message">
            <svg-icon icon-class="money" class-name="card-panel-icon" />
          </div>
          <div class="card-panel-description3">
            <div class="card-panel-text">本月奖金</div>
            <div class="card-panel-num">{{ last_month_service_bonus }}</div>
            <span class="card-panel-num">/</span>
            <div class="card-panel-num">{{ month_service_bonus }}</div>
          </div>
          <div class="card-panel-description3">
            <div class="card-panel-text">下月奖金</div>
            <div class="card-panel-num">{{ next_month_service_bonus }}</div>
            <span class="card-panel-num">/</span>
            <div class="card-panel-num">{{ next_get_month_service_bonus }}</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel" @click="handleSetLineChartData('purchases')">
          <div class="card-panel-icon-wrapper icon-money">
            <svg-icon icon-class="form" class-name="card-panel-icon" />
          </div>
          <div class="card-panel-description4">
            <div class="card-panel-text">本月签单</div>
            <div class="card-panel-num">{{ user }}</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel" @click="handleSetLineChartData('shoppings')">
          <div class="card-panel-icon-wrapper icon-shopping">
            <svg-icon icon-class="peoples" class-name="card-panel-icon" />
          </div>
          <div class="card-panel-description4">
            <div class="card-panel-text">意向客户</div>
            <div class="card-panel-num">{{ table_simple_new_all_data }}</div>
          </div>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="12">
      <el-col :span="8">
        <el-card>
          <div class="card-fixed-header-db">
            待办事项
            <el-select
              v-model="todo_value"
              ref="chooseKpi1"
              @blur="type_select1"
              filterable
              placeholder="请选择"
              @change="get_shop_name_todo()"
            >
              <el-option
                v-for="item in todo_dict"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>
          <div class="box-card card-panel-col card-setting">
            <div v-if="to_do !== undefined && to_do.length > 0">
              <div v-for="(to_do, index) in to_do" :key="index" class="text item">
                <el-card shadow="never" class="card-bottom">
                  <div class="card-bottom-db" />
                  {{ to_do.shop_name }}【{{ to_do.project }}】
                  <el-button
                    type="danger"
                    icon="el-icon-check"
                    circle
                    style="padding:1px"
                    @click="select(index)"
                  />
                  <div class="bottom clearfix">
                    <i class="el-icon-alarm-clock time" />
                    <time class="time">截止时间：{{ to_do.time }}</time>
                    <class class="money">&nbsp;&nbsp;&nbsp;￥{{ to_do.money }}</class>
                    <class v-if="to_do.status === '审核未通过'">
                      <el-popover placement="top-start" width="400" trigger="hover">
                        <el-input
                          v-model="to_do.edit"
                          label="驳回原因"
                          style="width:100%"
                          :disabled="true"
                        />
                        <class
                          slot="reference"
                          class="money"
                          style="color:#f4516c;"
                        >&nbsp;&nbsp;&nbsp;{{ to_do.status }}</class>
                      </el-popover>
                    </class>
                    <class v-else>
                      <class
                        class="money"
                        style="color:#f4516c"
                      >&nbsp;&nbsp;&nbsp;{{ to_do.status }}</class>
                    </class>
                    <el-progress
                      :percentage="to_do.schedule"
                      :show-text="false"
                      style="width:30%;float:right;position: relative; bottom: -5px;"
                    />
                  </div>
                </el-card>
              </div>
            </div>
            <div v-else>
              <div class="div2">暂无</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <div class="card-fixed-header-dsh">
            待审核事项
            <el-select
              v-model="pending_review_value"
              ref="chooseKpi2"
              @blur="type_select2"
              filterable
              placeholder="请选择"
              @change="get_shop_name_pending_review()"
            >
              <el-option
                v-for="item in pending_review_dict"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>
          <div class="box-card card-panel-col card-setting">
            <div v-if="pending_review !== undefined && pending_review.length > 0">
              <div v-for="(pending_review, index) in pending_review" :key="index" class="text item">
                <el-card shadow="never" class="card-bottom">
                  <div class="card-bottom-sh" />
                  {{ pending_review.shop_name }}【{{ pending_review.project }}】
                  <div class="bottom clearfix">
                    <span class="time">截止时间</span>
                    <time class="time">{{ pending_review.time }}</time>
                    <class class="money">&nbsp;&nbsp;&nbsp;￥{{ pending_review.money }}</class>
                    <class
                      class="money"
                      style="color:#f0e68c"
                    >&nbsp;&nbsp;&nbsp;{{ pending_review.status }}</class>
                    <el-progress
                      :percentage="pending_review.schedule"
                      :show-text="false"
                      style="width:30%;float:right;position: relative; bottom: -5px;"
                    />
                  </div>
                </el-card>
              </div>
            </div>
            <div v-else>
              <div class="div2">暂无</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <div class="card-fixed-header-ywc">
            已完成事项
            <el-select
              v-model="completed_value"
              ref="chooseKpi3"
              @blur="type_select3"
              filterable
              placeholder="请选择"
              @change="get_shop_name_completed()"
            >
              <el-option
                v-for="item in completed_dict"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>
          <div class="box-card card-panel-col card-setting">
            <div v-if="completed !== undefined && completed.length > 0">
              <div v-for="(to_do, index) in completed" :key="index" class="text item">
                <el-card shadow="never" class="card-bottom">
                  <div class="card-bottom-wc" />
                  {{ to_do.shop_name }}【{{ to_do.project }}】
                  <div class="bottom clearfix">
                    <span class="time">截止时间</span>
                    <time class="time">{{ to_do.time }}</time>
                    <class class="money">&nbsp;&nbsp;&nbsp;￥{{ to_do.money }}</class>
                    <class class="money" style="color:#34bfa3">&nbsp;&nbsp;&nbsp;{{ to_do.status }}</class>
                    <el-progress
                      :percentage="to_do.schedule"
                      :show-text="false"
                      style="width:30%;float:right;position: relative; bottom: -5px;"
                    />
                  </div>
                </el-card>
              </div>
            </div>
            <div v-else>
              <div class="div2">暂无</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-dialog class="dialog" title="待办事项提交审核" :visible.sync="dialogFormVisible" center="true">
      <el-form :model="form">
        <el-form-item label="代办事项名称" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off" :disabled="true" />
        </el-form-item>
        <el-form-item label="备注信息" :label-width="formLabelWidth">
          <el-input v-model="edit" type="textarea" autocomplete="off" />
        </el-form-item>
        <el-form-item label="付款截图" :label-width="formLabelWidth">
          <el-upload
            action="http://127.0.0.1:8000/app/update_img/"
            list-type="picture-card"
            :on-preview="handlePictureCardPreview"
            :on-remove="handleRemove"
            :on-change="handlechange"
            v-model="update"
            name="image"
            limit="1">
            <i class="el-icon-plus"></i>
          </el-upload>
          <el-dialog :visible.sync="dialogVisible">
            <img width="100%" :src="dialogImageUrl" alt="">
          </el-dialog>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogFormVisible = false;handleclose(form)">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog
      class="dialog"
      title="奖金明细"
      :visible.sync="dialogFormVisible_jiangjinmingxi"
      center="true"
    >
      <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
        <el-tab-pane label="本月" name="first">
          <el-table :data="jiangjin" :label="本月服务奖金" style="width: 100%">
            <el-table-column property="shop_name" label="店名" width="200" />
            <el-table-column property="project" label="项目名称" width="200" />
            <el-table-column property="money" label="奖金" />
            <el-table-column property="time" label="截止时间" />
            <el-table-column property="status" label="状态">
              <template slot-scope="{row}">
                <div v-if="row.status === '未完成'">
                  <el-button type="text" class="link-type" style="color:#6495ED">{{ row.status }}</el-button>
                </div>
                <div v-else-if="row.status === '已过期'">
                  <el-button type="text" class="link-type" style="color:#FF0000">{{ row.status }}</el-button>
                </div>
                <div v-else-if="row.status === '已完成'">
                  <el-button type="text" class="link-type" style="color:#7CFC00">{{ row.status }}</el-button>
                </div>
                <div v-else-if="row.status === '待审核'">
                  <el-button type="text" class="link-type" style="color:#FFD700">{{ row.status }}</el-button>
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
        </el-tab-pane>
        <el-tab-pane label="下月" name="second">
          <el-table :data="jiangjin_xiayue" :label="下月服务奖金" style="width: 100%">
            <el-table-column property="shop_name" label="店名" width="200" />
            <el-table-column property="project" label="项目名称" width="200" />
            <el-table-column property="money" label="奖金" />
            <el-table-column property="time" label="截止时间" />
            <el-table-column property="status" label="状态">
              <template slot-scope="{row}">
                <div v-if="row.status === '未完成'">
                  <el-button type="text" class="link-type" style="color:#6495ED">{{ row.status }}</el-button>
                </div>
                <div v-else-if="row.status === '已过期'">
                  <el-button type="text" class="link-type" style="color:#FF0000">{{ row.status }}</el-button>
                </div>
                <div v-else-if="row.status === '已完成'">
                  <span class="link-type" style="color:#7CFC00">{{ row.status }}</span>
                </div>
                <div v-else-if="row.status === '待审核'">
                  <span class="link-type" style="color:#FFD700">{{ row.status }}</span>
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
              :total="total_xiayue"
              style="margin-bottom:15px"
              @size-change="handleSizeChange_xiayue"
              @current-change="handleCurrentChange_xiayue"
            />
          </div>
        </el-tab-pane>
      </el-tabs>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible_jiangjinmingxi = false">取 消</el-button>
        <el-button type="primary" @click="dialogFormVisible_jiangjinmingxi = false;">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="订单详情" :visible.sync="dialogTableVisible_benyueyeji">
      <el-table :data="benyueyeji_data">
        <el-table-column property="sign_contract_shop" label="签约店名" width="200"></el-table-column>
        <el-table-column property="order_date" label="签约日期" width="150"></el-table-column>
        <el-table-column property="order_amount" label="签约金额"></el-table-column>
        <el-table-column property="cost_fees" label="成本费"></el-table-column>
        <el-table-column property="shop_cooperation_duration" label="签约时长"></el-table-column>
        <el-table-column property="tags" label="签约状态">
          <template slot-scope="{row}">
            <div v-if="row.tags === '新签'">
              <el-button
                type="text"
                style="color:#00FF00"
                @click="shop_botton(row)"
              >{{ row.tags }}</el-button>
            </div>
            <div v-else-if="row.tags === '断约'">
              <el-button
                type="text"
                style="color:#FFFF00"
                @click="shop_botton(row)"
              >{{ row.tags }}</el-button>
            </div>
            <div v-else-if="row.tags === '续约'">
              <el-button
                type="text"
                style="color:#1E90FF"
                @click="shop_botton(row)"
              >{{ row.tags }}</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <div style="text-align: center;margin-top: 30px;">
        <el-pagination
          :current-page="currentPage_benyueyeji"
          background
          layout="prev, pager,jumper, next, sizes, total"
          :page-sizes="[10, 20, 50, 100]"
          :total="total_benyueyeji"
          style="margin-bottom:15px"
          @size-change="handleSizeChange_benyueyeji"
          @current-change="handleCurrentChange_benyueyeji"
        />
      </div>
    </el-dialog>
    <el-dialog title="本月业绩概览" :visible.sync="dialogTableVisible_shop_botten">
      <el-form :model="row_row">
        <el-form-item label="订单ID" :label-width="formLabelWidth">
          <el-input
            v-model="row_row.contract_id_edit"
            autocomplete="off"
            style="width:80%"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item label="店名" :label-width="formLabelWidth">
          <el-input
            v-model="row_row.sign_contract_shop_edit"
            style="width:80%"
            placeholder="请选择活动区域"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item label="状态" :label-width="formLabelWidth">
          <el-input
            v-model="row_row.tags"
            style="width:80%"
            placeholder="请选择活动区域"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item label="下单日期" :label-width="formLabelWidth">
          <el-date-picker
            v-model="row_row.order_date_edit"
            type="date"
            placeholder="选择日期"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item label="开始日期" :label-width="formLabelWidth">
          <el-date-picker
            v-model="row_row.order_start_date_edit"
            type="date"
            placeholder="选择日期"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item label="门店数" :label-width="formLabelWidth">
          <el-input-number
            v-model="row_row.order_numbers_edit"
            :min="1"
            :max="10"
            :disabled="true"
            label="描述文字"
          />
        </el-form-item>
        <el-form-item label="合作时长" :label-width="formLabelWidth">
          <el-select
            v-model="row_row.shop_cooperation_duration_edit"
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
            v-model="row_row.order_end_date_edit"
            type="date"
            placeholder="选择日期"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item label="签约金额" :label-width="formLabelWidth">
          <el-input
            v-model="row_row.order_amount_edit"
            style="width:80%"
            placeholder="请选择活动区域"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item label="成本费" :label-width="formLabelWidth">
          <el-input
            v-model="row_row.cost_fees"
            style="width:80%"
            placeholder="请选择活动区域"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item label="所在城市" :label-width="formLabelWidth">
          <el-input
            v-model="row_row.city"
            style="width:80%"
            placeholder="未标注城市"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item label="签约销售" :label-width="formLabelWidth">
          <el-input
            v-model="row_row.order_contract_sales_edit"
            style="width:80%"
            placeholder="签约销售"
            :disabled="true"
          />
        </el-form-item>
      </el-form>
    </el-dialog>
    <el-dialog
      class="dialog"
      title="剩余待发奖金"
      :visible.sync="dialogFormVisible_shengyu"
      center="true"
    >
      <el-row :gutter="40" class="panel-group2">
        <el-col :xs="24" :sm="24" :lg="6" class="card-panel-col" style="height:54px;weight:100%;">
          <div class="card-panel2">
            <div class="card-panel-description">
              <div class="card-panel-text">剩余待发奖金</div>
              <div class="card-panel-num">{{ money_jj }}</div>
            </div>
          </div>
        </el-col>
      </el-row>
      <el-date-picker
        ref="datePicker2"
        v-model="value2"
        type="month"
        placeholder="选择月"
        @change="clict_get_money_jj_1"
        @focus="datePicker_click"
        >
      </el-date-picker>
      <el-select
        ref="chooseKpi_jj"
        @blur="type_select"
        v-model="xiaoshou_value_jj"
        clearable
        filterable
        @change="clict_get_money_jj_2"
        placeholder="请选择"
      >
        <el-option
          v-for="item in xiaoshou_options_jj"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-table :data="benyueyeji_data_jj">
        <el-table-column property="shop_name" label="店名" width="200"></el-table-column>
        <el-table-column property="project" label="任务" width="150"></el-table-column>
        <el-table-column property="time" label="截止时间"></el-table-column>
        <el-table-column property="money" label="奖金"></el-table-column>
        <el-table-column property="username" label="销售"></el-table-column>
      </el-table>
      <div style="text-align: center;margin-top: 30px;">
        <el-pagination
          :current-page="currentPage_jj"
          background
          layout="prev, pager,jumper, next, sizes, total"
          :page-sizes="[5, 10, 20, 50, 100]"
          :total="total_jj"
          style="margin-bottom:15px"
          @size-change="handleSizeChange_jj"
          @current-change="handleCurrentChange_jj"
        />
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible_shengyu = false">取 消</el-button>
        <el-button type="primary" @click="dialogFormVisible_shengyu = false;">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import CountTo from "vue-count-to";
import request from "@/utils/request";
import global from "@/store/modules/user";
export default {
  components: {
    CountTo,
  },
  data() {
    return {
      lat: "",
      lng: "",
      activeName: "first",
      xiaoshou_value_jj:'',
      value2:'',
      money_jj:'',
      total_jj:0,
      pagesize_jj: 5,
      currentPage_jj: 1,
      username_data:'',
      dialogFormVisible_jiangjinmingxi: false,
      edit: "",
      dialogTableVisible_benyueyeji: false,
      dialogTableVisible_shop_botten:false,
      dialogFormVisible_shengyu:false,
      startVal: 0,
      table_simple_data: 0,
      table_simple_data_signing: 0,
      benyueyeji_data_jj:'',
      dialogFormVisible: false,
      last_month_service_bonus: 0,
      next_get_month_service_bonus: 0,
      next_month_service_bonus: 0,
      month_service_bonus: 0,
      user: 0,
      month_data: 0,
      jiangjin_xiayue: 0,
      currentPage_xiayue: 1,
      pagesize_xiayue: 10,
      total_xiayue: 0,
      cost_fees: 0,
      benyueyeji_data: [],
      currentPage_benyueyeji: 1,
      pagesize_benyueyeji: 10,
      total_benyueyeji: 0,
      jiangjin: [],
      date_year: 0,
      date_month: 0,
      commission_point: 0,
      table_simple_new_all_data: 0,
      currentPage: 1,
      pagesize: 10,
      to_do: [],
      completed: [],
      pending_review: [],
      total: 0,
      index: "",
      roles: "",
      formLabelWidth: "120px",
      form: {
        lat2: "",
        lng2: "",
        name: "",
        region: "",
        date1: "",
        date2: "",
        delivery: false,
        type: [],
        resource: "",
        desc: "",
      },
      todo_dict: [],
      todo_value: "待办事项",
      todo_shop_name: "",
      get_username: "",
      pending_review_dict: [],
      pending_review_value: "待审核事项",
      completed_dict: [],
      xiaoshou_value: "",
      completed_value: "已完成事项",
      xiaoshou_options: [],
      xiaoshou_options_jj: [],
      update: [
          {
            required: true,
            message: '请上传图片',
            trigger: 'change'
          }
      ],
      dialogImageUrl:'',
      row_row:{
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
        tags:undefined,
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
      count:1,
    };
  },
  created: function () {
    this.roles = global.state["avatar"];
    console.log("this.roles", this.roles);
    if (
      global.state["avatar"] === "admin" ||
      global.state["avatar"] === "super_admin"
    ) {
      this.get_xiaoshou_data();
    }
    var now = new Date();
    var year = now.getFullYear(); // 得到年份
    var month = now.getMonth() + 1;
    month = month.toString();
    if (month.length == 1) {
      month = "0" + month;
    }
    this.month_data = year.toString() + "-" + month.toString();
    this.date_year = year.toString();
    this.date_month = month.toString();
    console.log(year.toString() + "-" + month.toString());
    this.fetchData(global.state["first_name"]);
    this.get_to_do();
    this.get_shop_name(global.state["first_name"]);
    this.get_pending_review(global.state["first_name"]);
    this.get_completed(global.state["first_name"]);
    
  },
  methods: {
    open_jj(){
      this.dialogFormVisible_shengyu=true;
      this.axios.get("http://127.0.0.1:8000/app/get_xiaoshou_jj/").then((body) => {this.xiaoshou_options_jj = body.data.data});
      this.get_money_jj()
    },
    get_money_jj(){
      console.log(this.value2)
      console.log(this.xiaoshou_value_jj)
      if (this.value2 == null){
        this.axios.get("http://127.0.0.1:8000/app/get_money_jj/", {
          params: {
            username: this.xiaoshou_value_jj,
            month_data: '',
            pagesize: this.pagesize_jj,
            currentPage: this.currentPage_jj,
            title: this.total_jj,
          },
        })
        .then((body) => {
          this.benyueyeji_data_jj = body.data.data
          this.money_jj = body.data.money
          this.total_jj = body.data.total
        });
      }else{
        this.axios.get("http://127.0.0.1:8000/app/get_money_jj/", {
          params: {
            username: this.xiaoshou_value_jj,
            month_data: this.value2,
            pagesize: this.pagesize_jj,
            currentPage: this.currentPage_jj,
            title: this.total_jj,
          },
        })
        .then((body) => {
          console.log(body.data.money)
          this.benyueyeji_data_jj = body.data.data
          this.money_jj = body.data.money
          this.total_jj = body.data.total
        });
      }
    },
    clict_get_money_jj_1(){
      if (this.value2 == null){
        console.log('进入')
        this.get_money_jj()
      }else{
        var year = this.value2.getFullYear()
        var month = this.value2.getMonth() + 1
        if (month.toString().length == 1) {
          month = "0" + month;
          this.value2 = year.toString() + "-" + month.toString();
        }else{
          this.value2 = year.toString() + "-" + month.toString();
        }
        this.get_money_jj()
      }
    },
    clict_get_money_jj_2(){
      this.get_money_jj()
    },
    noclick(){
      if (this.count == 1){
        this.count = 3
      }else if (this.count == 3){
        this.$refs.datePicker.hidePicker();
        this.$refs.datePicker2.hidePicker();
        this.count = 1
      }
    },
    datePicker_click(){
      this.count = 1
    },
    handleRemove(file, fileList) {
        this.$message({
          message: '已删除',
          type: 'warning'
        });
    },
    handlePictureCardPreview(file) {
        this.dialogImageUrl = 'http://127.0.0.1:8000/media/'+file.name;
        // this.url = this.dialogImageUrl
        this.dialogVisible = true;
    },
    handlechange(file){
      if (file.status == 'success'){
        this.$message({
          message: '上传成功',
          type: 'success'
        });
        this.dialogImageUrl = 'http://127.0.0.1:8000/media/'+file.name;
      }
    },
    shop_botton(row) {
      this.dialogTableVisible_shop_botten = true
      this.row_row.contract_id_edit = row.contract_id
      this.row_row.order_date_edit = row.order_date
      this.row_row.order_start_date_edit = row.order_start_date
      this.row_row.sign_contract_shop_edit = row.sign_contract_shop
      this.row_row.customer_source_edit = row.customer_source
      this.row_row.contract_status_edit = row.contract_status
      this.row_row.contracted_projects_edit = row.contracted_projects
      this.row_row.shop_industry_edit = row.shop_industry
      this.row_row.shop_kp_name_edit = row.shop_kp_name
      this.row_row.shop_telephonenumber_edit = row.shop_telephonenumber
      this.row_row.order_numbers_edit = row.order_numbers
      this.row_row.shop_cooperation_duration_edit = row.shop_cooperation_duration
      this.row_row.shop_kp_wechat_id_edit = row.shop_kp_wechat_id
      this.row_row.order_end_date_edit = row.order_end_date
      this.row_row.order_amount_edit = row.order_amount
      this.row_row.payment_method_edit = row.payment_method
      this.row_row.order_contract_sales_edit = row.order_contract_sales
      this.row_row.shop_remark_edit = row.shop_remark
      this.row_row.order_form_edit = row.order_form
      this.row_row.order_commission = row.order_commission
      this.row_row.shop_id = row.shop_id
      this.row_row.cost_fees = row.cost_fees
      this.row_row.city = row.city,
      this.row_row.tags = row.tags
    },
    type_select() {
      this.$refs.chooseKpi.blur();
      this.$refs.chooseKpi_jj.blur();
      
    },
    type_select1() {
      this.$refs.chooseKpi1.blur();
    },
    type_select2() {
      this.$refs.chooseKpi2.blur();
    },
    type_select3() {
      this.$refs.chooseKpi2.blur();
      this.$refs.chooseKpi3.blur();
    },
    handleclose(index) {
      this.axios
        .get("http://127.0.0.1:8000/app/submit_review/", {
          params: {
            project: this.to_do[this.index].project,
            shop_name: this.to_do[this.index].shop_name,
            time: this.to_do[this.index].time,
            money: this.to_do[this.index].money,
            schedule: this.to_do[this.index].schedule,
            username: this.to_do[this.index].username,
            order_id: this.to_do[this.index].order_id,
            edit: this.edit,
            lat: this.lat,
            lng: this.lng,
            url: this.dialogImageUrl
          },
        })
        .then((body) => {
          if (body.data.state == 1){
            this.$notify({
              title: "提交成功",
              message: "",
              type: "success",
            });
            this.get_to_do(this.xiaoshou_value);
            this.get_pending_review(this.xiaoshou_value);
          }else{
            this.$notify({
              title: "提交失败",
              message: "已提交审核",
              type: "error",
            });
            this.get_to_do(this.xiaoshou_value);
            this.get_pending_review(this.xiaoshou_value);
          }
        });
    },
    get_benyuejiangjing() {
      if (this.xiaoshou_value === "") {
        this.axios
          .get("http://127.0.0.1:8000/app/get_benyuejiangjing/", {
            params: {
              pagesize: this.pagesize,
              // 显示第几页
              currentPage: this.currentPage,
              month: this.month_data,
              username: global.state["first_name"],
            },
          })
          .then((body) => {
            console.log("body", body);
            this.jiangjin = body.data.data;
            this.total = body.data.total;
          });
      } else {
        this.axios
          .get("http://127.0.0.1:8000/app/get_benyuejiangjing/", {
            params: {
              pagesize: this.pagesize,
              // 显示第几页
              currentPage: this.currentPage,
              month: this.month_data,
              username: this.xiaoshou_value,
            },
          })
          .then((body) => {
            this.jiangjin = body.data.data;
            this.total = body.data.total;
          });
      }
    },
    get_benyueyeji() {
      if (this.xiaoshou_value === "") {
        this.axios
          .get("http://127.0.0.1:8000/app/get_benyueyeji/", {
            params: {
              pagesize: this.pagesize_benyueyeji,
              // 显示第几页
              currentPage: this.currentPage_benyueyeji,
              month: this.month_data,
              username: global.state["first_name"],
            },
          })
          .then((body) => {
            this.benyueyeji_data = body.data.data;
            this.total_benyueyeji = body.data.total;
          });
      } else {
        this.axios
          .get("http://127.0.0.1:8000/app/get_benyueyeji/", {
            params: {
              pagesize: this.pagesize_benyueyeji,
              // 显示第几页
              currentPage: this.currentPage_benyueyeji,
              month: this.month_data,
              username: this.xiaoshou_value,
            },
          })
          .then((body) => {
            this.benyueyeji_data = body.data.data;
            this.total_benyueyeji = body.data.total;
          });
      }
    },
    get_benyuejiangjing_xiayue() {
      if (this.xiaoshou_value === "") {
        this.axios
          .get("http://127.0.0.1:8000/app/get_benyuejiangjing_xiayue/", {
            params: {
              pagesize: this.pagesize_xiayue,
              // 显示第几页
              currentPage: this.currentPage_xiayue,
              month: this.month_data,
              username: global.state["first_name"],
            },
          })
          .then((body) => {

            console.log("body", body);
            this.jiangjin_xiayue = body.data.data;
            this.total_xiayue = body.data.total;
          });
      } else {
        this.axios
          .get("http://127.0.0.1:8000/app/get_benyuejiangjing_xiayue/", {
            params: {
              pagesize: this.pagesize_xiayue,
              // 显示第几页
              currentPage: this.currentPage_xiayue,
              month: this.month_data,
              username: this.xiaoshou_value,
            },
          })
          .then((body) => {
            this.jiangjin_xiayue = body.data.data;
            this.total_xiayue = body.data.total;
          });
      }
    },
    get_xiaoshou_data() {
      this.axios
        .get("http://127.0.0.1:8000/app/get_xiaoshou_data/", {
          params: {
            username: global.state["first_name"],
          },
        })
        .then((body) => {
          this.xiaoshou_options = body.data.data;
        });
    },
    get_shop_name_todo(val) {
      if (this.xiaoshou_value != "") {
        this.axios
          .get("http://127.0.0.1:8000/app/get_to_do/", {
            params: {
              username: this.xiaoshou_value,
              shop_name: this.todo_value,
              month: this.month_data
            },
          })
          .then((body) => {
            this.to_do = body.data.data;
          });
      } else {
        this.axios
          .get("http://127.0.0.1:8000/app/get_to_do/", {
            
            params: {
              username: global.state["first_name"],
              shop_name: this.todo_value,
              month: this.month_data
            },
          })
          .then((body) => {
            this.to_do = body.data.data;
          });
      }
    },
    get_shop_name_pending_review(val) {
      if (this.xiaoshou_value != "") {
        this.axios
          .get("http://127.0.0.1:8000/app/get_pending_review/", {
            params: {
              username: this.xiaoshou_value,
              shop_name: this.pending_review_value,
              month: this.month_data
            },
          })
          .then((body) => {
            console.log(body.data.data);
            this.pending_review = body.data.data;
          });
      } else {
        this.axios
          .get("http://127.0.0.1:8000/app/get_pending_review/", {
            params: {
              username: global.state["first_name"],
              shop_name: this.pending_review_value,
              month: this.month_data
            },
          })
          .then((body) => {
            console.log(body.data.data);
            this.pending_review = body.data.data;
          });
      }
    },
    xunhuan_def() {
      for (var i = 0; i <= 10; i++) {
        if (i < 2) {
          this.get_to_do(global.state["first_name"]);
          this.get_shop_name(global.state["first_name"]);
          this.get_pending_review(global.state["first_name"]);
          this.get_completed(global.state["first_name"]);
        }
      }
    },
    get_shop_name_completed(val) {
      console.log(this.completed_value);
      if (this.xiaoshou_value != "") {
        this.axios
          .get("http://127.0.0.1:8000/app/get_completed/", {
            params: {
              username: this.xiaoshou_value,
              shop_name: this.completed_value,
              month: this.month_data
            },
          })
          .then((body) => {
            this.completed = body.data.data;
          });
      } else {
        this.axios
          .get("http://127.0.0.1:8000/app/get_completed/", {
            params: {
              username: global.state["first_name"],
              shop_name: this.completed_value,
              month: this.month_data
            },
          })
          .then((body) => {
            console.log(body.data.data);
            this.completed = body.data.data;
          });
      }
    },
    get_shop_name(val) {
      this.axios
        .get("http://127.0.0.1:8000/app/get_shop_name/", {
          params: {
            // 每页显示的条数
            username: val,
            month: this.month_data
          },
        })
        .then((res) => {
          this.todo_dict = res.data.todo_dict;
          this.pending_review_dict = res.data.pending_review_dict;
          this.completed_dict = res.data.completed_dict;
        })
        .catch(function (error) {
          this.loading = false;
          console.log(error);
        });
    },
    formatTime() {
      this.todo_value="待办事项"
      this.pending_review_value="待审核事项"
      this.completed_value="已完成事项"
      if (this.username_data == "") {
        this.fetchData(global.state["first_name"]);
        this.get_to_do(global.state["first_name"]);
        this.get_shop_name(global.state["first_name"]);
        this.get_pending_review(global.state["first_name"]);
        this.get_completed(global.state["first_name"]);
      } else {
        this.fetchData(this.username_data);
        this.get_to_do(this.username_data);
        this.get_shop_name(this.username_data);
        this.get_pending_review(this.username_data);
        this.get_completed(this.username_data);
      }
      if (this.xiaoshou_value === "") {
        this.xiaoshou_value = global.state["first_name"];
      }
      this.axios
        .get("http://127.0.0.1:8000/app/order_count/", {
          params: {
            username: this.xiaoshou_value,
            month_data: this.month_data,
          },
        })
        .then((body) => {
          this.table_simple_data = body.data.table_simple_data;
          this.table_simple_data_signing = body.data.table_simple_data_signing;
          this.user = body.data.user;
          this.commission_point = body.data.commission_point;
          this.table_simple_new_all_data = body.data.table_simple_new_all_data;
          this.cost_fees = body.data.cost_fees;
          this.last_month_service_bonus = body.data.last_month_service_bonus;
          this.month_service_bonus = body.data.month_service_bonus;
          this.next_get_month_service_bonus =
            body.data.next_get_month_service_bonus;
          this.next_month_service_bonus = body.data.next_month_service_bonus;
        });
    },
    handleSetLineChartData(type) {
      if (type === "newVisitis") {
        this.dialogTableVisible_benyueyeji = true;
        this.get_benyueyeji();
      } else if (type === "shoppings") {
        window.location.href = "http://www.beiai.tech/#/table/dynamic-table";
      } else if (type === "messages") {
        this.dialogFormVisible_jiangjinmingxi = true;
        this.get_benyuejiangjing();
        this.get_benyuejiangjing_xiayue();
      } else if (type === "purchases") {
        window.location.href =
          "http://www.beiai.tech/#/charts/%E6%88%91%E7%9A%84%E8%AE%A2%E5%8D%95";
      } else {
        this.$notify({
          title: "找不到地址",
          message: "",
          type: "error",
        });
      }
    },
    fetchData: function (val) {
      this.axios
        .get("http://127.0.0.1:8000/app/order_count/", {
          params: {
            username: val,
            month_data: this.month_data,
          },
        })
        .then((body) => {
          this.table_simple_data = body.data.table_simple_data;
          this.table_simple_data_signing = body.data.table_simple_data_signing;
          this.user = body.data.user;
          this.commission_point = body.data.commission_point;
          this.table_simple_new_all_data = body.data.table_simple_new_all_data;
          this.last_month_service_bonus = body.data.last_month_service_bonus;
          this.month_service_bonus = body.data.month_service_bonus;
          this.cost_fees = body.data.cost_fees;
          this.next_get_month_service_bonus = body.data.next_get_month_service_bonus;
          this.next_month_service_bonus = body.data.next_month_service_bonus;
        });
    },
    select(index) {
      var now = new Date();
      var year = now.getFullYear(); // 得到年份
      var month = now.getMonth() + 1;
      var date = now.getDate();
      month = month.toString();
      if (month.length === 1) {
        month = "0" + month;
      }
      var date1 = new Date(year + "-" + month + "-" + date);
      var date2 = new Date(this.to_do[index].time);
      var Difference_In_Time = date2.getTime() - date1.getTime();
      var Difference_In_Days = Difference_In_Time / (1000 * 3600 * 24);
      if (date1.getTime() > date2.getTime()) {
        this.$notify({
          title: "提交失败",
          message: "已超时",
          type: "error",
        });
      } else if (Difference_In_Days > 15) {
        this.$notify({
          title: "提交失败",
          message: "截止日期之前15天内提交",
          type: "error",
        });
      } else {
        this.form.name = this.to_do[index].shop_name + "【" + this.to_do[index].project + "】";
        this.dialogFormVisible = true;
        this.index = index;
      } 
    },
    get_to_do(val) {
      if (this.xiaoshou_value != "") {
        this.axios
          .get("http://127.0.0.1:8000/app/get_to_do/", {
            params: {
              username: this.xiaoshou_value,
              shop_name: this.todo_value,
              month: this.month_data,
            },
          })
          .then((body) => {
            this.to_do = body.data.data;
          });
      } else {
        this.axios
          .get("http://127.0.0.1:8000/app/get_to_do/", {
            params: {
              username: global.state["first_name"],
              shop_name: this.todo_value,
              month: this.month_data,
            },
          })
          .then((body) => {
            this.to_do = body.data.data;
          });
      }
    },
    xiaoshou_change(username) {
      this.todo_value="待办事项"
      this.pending_review_value="待审核事项"
      this.completed_value="已完成事项"

      if (username === "") {
        this.fetchData(global.state["first_name"]);
        this.get_to_do(global.state["first_name"]);
        this.get_shop_name(global.state["first_name"]);
        this.get_pending_review(global.state["first_name"]);
        this.get_completed(global.state["first_name"]);
      } else {
        this.username_data = username
        this.fetchData(username);
        this.get_to_do(username);
        this.get_shop_name(username);
        this.get_pending_review(username);
        this.get_completed(username);
      }
      this.$forceUpdate();
    },
    get_pending_review(val) {
      if (this.xiaoshou_value != "") {
        this.axios
          .get("http://127.0.0.1:8000/app/get_pending_review/", {
            params: {
              username: this.xiaoshou_value,
              shop_name: this.pending_review_value,
              month: this.month_data,
            },
          })
          .then((body) => {
            console.log(body.data.data);
            this.pending_review = body.data.data;
          });
      } else {
        this.axios
          .get("http://127.0.0.1:8000/app/get_pending_review/", {
            params: {
              username: global.state["first_name"],
              shop_name: this.pending_review_value,
              month: this.month_data,
            },
          })
          .then((body) => {
            console.log(body.data.data);
            this.pending_review = body.data.data;
          });
      }
    },
    get_completed(val) {
      if (this.xiaoshou_value != "") {
        this.axios
          .get("http://127.0.0.1:8000/app/get_completed/", {
            params: {
              username: this.xiaoshou_value,
              shop_name: this.completed_value,
              month: this.month_data,
            },
          })
          .then((body) => {
            this.completed = body.data.data;
          });
      } else {
        this.axios
          .get("http://127.0.0.1:8000/app/get_completed/", {
            params: {
              username: global.state["first_name"],
              shop_name: this.completed_value,
              month: this.month_data,
            },
          })
          .then((body) => {
            this.completed = body.data.data;
          });
      }
    },
    handleSizeChange(val) {
      // 改变每页显示的条数
      this.pagesize = val;
      this.get_benyuejiangjing();
      // 点击每页显示的条数时，显示第一页
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      this.get_benyuejiangjing();
    },
    handleSizeChange_xiayue(val) {
      // 改变每页显示的条数
      this.pagesize_xiayue = val;
      this.get_benyuejiangjing_xiayue();
      // 点击每页显示的条数时，显示第一页
    },
    handleCurrentChange_xiayue(val) {
      this.currentPage_xiayue = val;
      this.get_benyuejiangjing_xiayue();
    },
    handleSizeChange_benyueyeji(val) {
      // 改变每页显示的条数
      this.pagesize_benyueyeji = val;
      this.get_benyueyeji();
      // 点击每页显示的条数时，显示第一页
    },
    handleCurrentChange_benyueyeji(val) {
      this.currentPage_benyueyeji = val;
      this.get_benyueyeji();
    },
    handleCurrentChange_jj(val) {
      this.currentPage_jj = val;
      this.get_money_jj();
    },
    handleSizeChange_jj(val) {
      // 改变每页显示的条数
      this.pagesize_jj = val;
      this.get_money_jj();
      // 点击每页显示的条数时，显示第一页
    },
  },
};
</script>

<style lang="scss" scoped>
.div2 {
  width: 100%;
  height: 415px;
  text-align: center;
  line-height: 400px;
}
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
      .card-panel-text {
        // float: right;
        line-height: 10px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-left: -15px;
      }

      .card-panel-num {
        margin-top: -17px;
        margin-right: 5px;
        float: right;
        font-size: 18px;
      }
      .card-panel-num2 {
        margin-top: -17px;
        margin-right: 5px;
        float: right;
        font-size: 18px;
      }
    }
    .card-panel-description4 {
      // float: inherit;
      // float: right;
      font-weight: bold;
      // margin: 10px;
      margin: 45px;
      margin-right: 0px;
      .card-panel-text {
        // float: right;
        line-height: 10px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-left: -15px;
      }

      .card-panel-num {
        margin-top: -17px;
        margin-right: 5px;
        float: right;
        font-size: 18px;
      }
    }
    .card-panel-description3 {
      // float: inherit;
      // float: right;
      font-weight: bold;
      // margin: 10px;
      margin: 26px;
      margin-right: 0px;
      .card-panel-text {
        // float: right;
        line-height: 10px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-left: -15px;
      }

      .card-panel-num {
        margin-top: -17px;
        margin-right: 5px;
        float: right;
        font-size: 18px;
      }
    }
  }
}
.map {
  width: 100%;
  height: 400px;
}
.panel-group2 {
  margin-top: 18px;

  .card-panel-col {
    margin-bottom: 32px;
  }
  .card-panel2 {
    height: 50px;
    width: 250px;
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
      .card-panel-text {
        // float: right;
        line-height: 10px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-left: -15px;
      }

      .card-panel-num {
        margin-top: -17px;
        margin-right: 5px;
        float: right;
        font-size: 18px;
      }
      .card-panel-num2 {
        margin-top: -17px;
        margin-right: 5px;
        float: right;
        font-size: 18px;
      }
    }
    .card-panel-description4 {
      // float: inherit;
      // float: right;
      font-weight: bold;
      // margin: 10px;
      margin: 45px;
      margin-right: 0px;
      .card-panel-text {
        // float: right;
        line-height: 10px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-left: -15px;
      }

      .card-panel-num {
        margin-top: -17px;
        margin-right: 5px;
        float: right;
        font-size: 18px;
      }
    }
    .card-panel-description3 {
      // float: inherit;
      // float: right;
      font-weight: bold;
      // margin: 10px;
      margin: 26px;
      margin-right: 0px;
      .card-panel-text {
        // float: right;
        line-height: 10px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-left: -15px;
      }

      .card-panel-num {
        margin-top: -17px;
        margin-right: 5px;
        float: right;
        font-size: 18px;
      }
    }
  }
}
.card-bottom {
  margin-bottom: 20px;
  padding-left: -20px;
}
.card-bottom-db {
  margin-left: -20px;
  margin-top: -20px;
  margin-bottom: -20px;
  height: 84.6px;
  width: 7px;
  background-color: red;
  float: left;
  white-space: nowrap;
}

.card-bottom-sh {
  margin-left: -20px;
  margin-top: -20px;
  margin-bottom: -20px;
  height: 84.6px;
  width: 7px;
  background-color: #f0e68c;
  float: left;
}
.card-bottom-wc {
  margin-left: -20px;
  margin-top: -20px;
  margin-bottom: -20px;
  height: 84.6px;
  width: 7px;
  background-color: #34bfa3;
  float: left;
}

.time {
  font-size: 13px;
  color: #999;
}

.money {
  font-size: 13px;
  color: #ffa500;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.card-setting::-webkit-scrollbar {
  display: none;
}

.card-setting {
  overflow-x: scroll;
  width: 100%;
  height: 415px;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.clearfix:after {
  clear: both;
}

.card-fixed-header-dsh {
  margin-top: -20px;
  margin-left: -20px;
  margin-right: -20px;
  padding: 20px;
  background-color: #f0e68c;
}

.card-fixed-header-db {
  margin-top: -20px;
  margin-left: -20px;
  margin-right: -20px;
  padding: 20px;
  background-color: #f4516c;
}

.card-fixed-header-ywc {
  margin-top: -20px;
  margin-left: -20px;
  margin-right: -20px;
  padding: 20px;
  background-color: #34bfa3;
}

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
@media (max-width: 550px) {
  .el-col {
    width: 100%;
  }
}
</style>
