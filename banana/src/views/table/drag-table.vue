<template>
  <div>
    <el-drawer
      class="drawer_body"
      title="店铺信息"
      :visible.sync="drawer"
      :direction="direction"
      :before-close="handleClose"
      size="100"
    >
      <div class="demo-drawer__content">
        <el-form :model="form">
          <el-form-item label="点评ID" :label-width="formLabelWidth">
            <el-input
              v-model="shop_edit.shop_id_edit"
              autocomplete="off"
              style="width:80%"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="店名" :label-width="formLabelWidth">
            <el-input
              v-model="shop_edit.shop_name_edit"
              style="width:80%"
              placeholder="请选择活动区域"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="电话" :label-width="formLabelWidth">
            <el-input
              v-model="shop_edit.shop_telephonenumber_edit"
              style="width:80%"
              placeholder="请选择活动区域"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="城市" :label-width="formLabelWidth">
            <el-input
              v-model="shop_edit.shop_city_edit"
              style="width:80%"
              placeholder="请选择活动区域"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="城区" :label-width="formLabelWidth">
            <el-select
              v-model="shop_edit.shop_business_district_edit"
              class="filter-item"
              value-key="id"
              filterable
              placeholder="请选择门店所在城区"
              :disabled="true"
              @change="business_district_edit"
            >
              <el-option v-for="item in regions" :key="item.id" :label="item.label" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="商圈" :label-width="formLabelWidth">
            <el-select
              v-model="shop_edit.shop_category_edit"
              class="filter-item"
              value-key="id"
              filterable
              :disabled="true"
              placeholder="请选择门店所在商圈"
              @change="category_edit"
            >
              <el-option
                v-for="item in business_districts"
                :key="item.id"
                :label="item.label"
                :value="item"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="品类" :label-width="formLabelWidth">
            <el-select
              v-model="shop_edit.shop_region_edit"
              class="filter-item"
              value-key="id"
              :disabled="true"
              filterable
              placeholder="请选择门店所在品类"
              @change="regions_data_edit"
            >
              <el-option
                v-for="item in categorys"
                :key="item.id"
                :label="item.label"
                :value="item"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="地址" :label-width="formLabelWidth">
            <el-input
              v-model="shop_edit.shop_address_edit"
              style="width:80%"
              placeholder="请输入门店地址"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="效果" :label-width="formLabelWidth">
            <el-input
              v-model="shop_edit.shop_effect_edit"
              style="width:80%"
              placeholder
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="服务" :label-width="formLabelWidth">
            <el-input
              v-model="shop_edit.shop_service_edit"
              style="width:80%"
              placeholder
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="环境" :label-width="formLabelWidth">
            <el-input
              v-model="shop_edit.shop_surroundings_edit"
              style="width:80%"
              placeholder
              :disabled="true"
            />
          </el-form-item>
          <el-form-item v-if="shop_add_form === ''" />
          <el-form-item v-else>
            <el-divider>客户信息</el-divider>
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
                placeholder="选择内容"
                style="width:200%"
                :disabled="true"
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
          <el-divider>备注信息</el-divider>
          <el-form-item label="备注内容" :label-width="formLabelWidth">
            <el-input
              v-model="shop_edit.text_edit"
              style="width:80%"
              placeholder="备注内容"
              type="textarea"
            />
          </el-form-item>
          <el-form-item label="备注信息" :label-width="formLabelWidth">
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
    <el-dialog title="添加拜访" :visible.sync="dialogFormVisible">
      <el-form ref="dynamicValidateForm" :model="dynamicValidateForm">
        <span v-for="(domain, index) in dynamicValidateForm.shop_add_form_baifang">
          <span v-if="domain.type === '文本类型'">
            <span v-if="domain.label === '联系电话'">
              <el-form-item
                :key="domain.key"
                :label="domain.label"
                style="width:80%"
                :label-width="formLabelWidth"
                :prop="'shop_add_form_baifang.' + index + '.value'"
                :rules="[
                  { required: true, message: '请输入手机号', trigger: 'blur' },
                  {
                    pattern: /^0{0,1}(13[0-9]|15[7-9]|153|156|18[7-9])[0-9]{8}$/,
                    message: '手机号格式不对',
                    trigger: 'blur'
                  }
                ]"
              >
                <el-input v-model.trim="domain.value" />
              </el-form-item>
            </span>
            <span v-else>
              <el-form-item
                :key="domain.key"
                :label="domain.label"
                style="width:80%"
                :label-width="formLabelWidth"
                :prop="'shop_add_form_baifang.' + index + '.value'"
                :rules="{
                  required: true, message: '不能为空', trigger: 'blur'}"
              >
                <el-input v-model.trim="domain.value" />
              </el-form-item>
            </span>
          </span>
          <span v-if="domain.type === '日期类型'">
            <el-form-item
              :key="domain.key"
              :label="domain.label"
              style="width:80%"
              :label-width="formLabelWidth"
              :prop="'shop_add_form_baifang.' + index + '.value'"
              :rules="{
                required: true, message: '不能为空', trigger: 'blur'}"
            >
              <el-date-picker v-model="domain.value" type="date" placeholder="选择日期" />
            </el-form-item>
          </span>
          <span v-if="domain.type === '选择下拉框'">
            <el-form-item
              :key="domain.key"
              :label="domain.label"
              style="width:80%"
              :label-width="formLabelWidth"
              :prop="'shop_add_form_baifang.' + index + '.value'"
              :rules="{
                required: true, message: '不能为空', trigger: 'blur'}"
            >
              <el-select v-model="domain.value" type="date" placeholder="选择内容">
                <el-option
                  v-for="item in domain.select"
                  :key="item.label"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </span>
          <span v-if="domain.type === '大文本框'">
            <el-form-item
              :key="domain.key"
              :label="domain.label"
              style="width:80%"
              :label-width="formLabelWidth"
              :prop="'shop_add_form_baifang.' + index + '.value'"
              :rules="{
                required: true, message: '不能为空', trigger: 'blur'}"
            >
              <el-input v-model.trim="domain.value" type="textarea" />
            </el-form-item>
          </span>
        </span>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="submit_shop_add_name_baifang('dynamicValidateForm')">确 定</el-button>
      </div>
    </el-dialog>
    <div class="filter-container" style="margin-left:15px;margin-top:25px;">
      <el-input
        v-model="listQuery.title"
        style="width: 200px;"
        placeholder="全部"
        @input="select_input"
      >
        <i slot="prefix" class="el-input__icon el-icon-search" />
      </el-input>
      <el-select
        ref="chooseKpi4"
        v-model="city"
        multiple
        collapse-tags
        value-key="id"
        style="width:180px;"
        placeholder="城市"
        @blur="city_select"
        @change="select_urban_area"
      >
        <el-option v-for="item in cities" :key="item.id" :label="item.label" :value="item.id" />
      </el-select>
      <el-select
        v-model="region"
        ref="chooseKpi"
        multiple
        collapse-tags
        value-key="id"
        style="width:180px;"
        placeholder="城区"
        @blur="region_select"
        @change="search_business_circle"
      >
        <el-option v-for="item in regions" :key="item.id" :label="item.label" :value="item.id" />
      </el-select>
      <el-select
        v-model="business_district"
        ref="chooseKpi2"
        multiple
        collapse-tags
        style="width:180px;"
        value-key="id"
        @blur="business_district_select"
        placeholder="商圈"
      >
        <el-option
          v-for="item in business_districts"
          :key="item.id"
          :label="item.label"
          :value="item.id"
        />
      </el-select>
      <el-select
        v-model="category"
        ref="chooseKpi3"
        multiple
        collapse-tags
        filterable
        value-key="id"
        style="width:180px;"
        @blur="category_select"
        placeholder="品类"
      >
        <el-option v-for="item in categorys" :key="item.id" :label="item.label" :value="item.id" />
      </el-select>
      <el-select
        v-model="type"
        filterable
        ref="chooseKpi5"
        style="width:130px;"
        value-key="id"
        placeholder="类型"
        @blur="type_select"
        @change="type_data"
      >
        <el-option v-for="item in types" :key="item.id" :label="item.label" :value="item" />
      </el-select>
      <span v-if="roles === 'admin'">
        <el-select
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
      @row-click="data_update"
    >
      <!-- <el-table-column type="selection" width="55"></el-table-column> -->
      <el-table-column prop="shop_id" label="商户ID" show-overflow-tooltip />
      <el-table-column label="店名" show-overflow-tooltip prop="shop_name" width="450">
        <template slot-scope="{row}">
          <div v-if="row.shop_tags === '新店'">
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
                slot="reference"
                class="link-type"
                style="color:#606266"
                @click="data_update(row);drawer = true"
              >{{ row.shop_name }}</span>
            </el-popover>

            <el-tag type="danger" effect="dark">{{ row.shop_tags }}</el-tag>
            <span v-if="row.shop_kp_category != ''">
              <el-tag type effect="dark">{{ row.shop_kp_category }}</el-tag>
            </span>
          </div>
          <div v-else-if="row.shop_tags === '断约'">
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
                slot="reference"
                class="link-type"
                style="color:#606266"
                @click="data_update(row);drawer = true"
              >{{ row.shop_name }}</span>
            </el-popover>
            <el-tag type="warning" effect="dark">{{ row.shop_tags }}</el-tag>
            <span v-if="row.shop_kp_category != ''">
              <el-tag type effect="dark">{{ row.shop_kp_category }}</el-tag>
            </span>
          </div>
          <div v-else-if="row.shop_tags === '续约'">
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
                slot="reference"
                class="link-type"
                style="color:#606266"
                @click="data_update(row);drawer = true"
              >{{ row.shop_name }}</span>
            </el-popover>
            <el-tag effect="dark">{{ row.shop_tags }}</el-tag>
            <span v-if="row.shop_kp_category != ''">
              <el-tag type effect="dark">{{ row.shop_kp_category }}</el-tag>
            </span>
          </div>
          <div v-else-if="row.shop_tags === '新签'">
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
                slot="reference"
                class="link-type"
                style="color:#606266"
                @click="data_update(row);drawer = true"
              >{{ row.shop_name }}</span>
            </el-popover>
            <el-tag type="success" effect="dark">{{ row.shop_tags }}</el-tag>
            <span v-if="row.shop_kp_category != ''">
              <el-tag type effect="dark">{{ row.shop_kp_category }}</el-tag>
            </span>
          </div>
          <div v-else>
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
                slot="reference"
                class="link-type"
                style="color:#606266"
                @click="data_update(row);drawer = true"
              >{{ row.shop_name }}</span>
            </el-popover>
            <span v-if="row.shop_kp_category != ''">
              <el-tag type effect="dark">{{ row.shop_kp_category }}</el-tag>
            </span>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="shop_start" label="星级" show-overflow-tooltip />
      <el-table-column prop="shop_review_count" show-overflow-tooltip label="评论数" />
      <el-table-column prop="shop_business_district" show-overflow-tooltip label="区域">
        <!-- <template slot="header">
          <el-input v-model="search" size="mini" placeholder="输入关键字搜索" />
        </template>-->
      </el-table-column>
      <el-table-column prop="shop_category" show-overflow-tooltip label="商圈" />
      <el-table-column prop="shop_region" show-overflow-tooltip label="品类" />
      <!-- <el-table-column prop="shop_per_capita_consumption" label="人均消费" width="150"></el-table-column> -->
      <el-table-column prop="shop_telephonenumber" show-overflow-tooltip label="电话" />
      <el-table-column label="操作" width="210" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-tooltip class="item" effect="dark" content="访问" placement="top-start">
            <el-button size="mini" type="success" @click.stop="jump_href(scope.$index, scope.row);">
              <i class="el-icon-sort" />
            </el-button>
          </el-tooltip>
          <el-tooltip class="item" effect="dark" content="添加拜访" placement="top-start">
            <el-button size="mini" type="primary" @click.stop="handleEdit(scope.row)">
              <i class="el-icon-plus" />
            </el-button>
          </el-tooltip>
          <el-tooltip class="item" effect="dark" content="回退" placement="top-start">
            <el-button size="mini" type="danger" @click.stop="open(scope.row);">
              <i class="el-icon-refresh-left" />
            </el-button>
          </el-tooltip>
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
import qs from "qs";
// axios.defaults.headers.get['Content-Type'] = 'text/plain'
export default {
  name: "DataList",
  row: "",
  data() {
    return {
      dialogFormVisible: false,
      dynamicValidateForm: {
        shop_add_form_baifang: [],
      },
      regions: [],
      loading: true,
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
          id: "行业",
          label: "行业",
        },
      ],
      business_districts: "",
      types: [
        {
          id: "新签",
          label: "新签",
        },
        {
          id: "断约",
          label: "断约",
        },
        {
          id: "续约",
          label: "续约",
        },
        {
          id: "新店",
          label: "新店",
        },
        {
          id: "合作状态",
          label: "合作状态",
        },
      ],
      listQuery: {
        title: undefined,
      },
      shop_kp_position: [
        { id: "大老板", label: "大老板" },
        { id: "合伙人", label: "合伙人" },
        { id: "经理", label: "经理" },
        { id: "店长", label: "店长" },
        { id: "前台", label: "前台" },
        { id: "技师", label: "技师" },
      ],
      shop_kp_city: [
        { id: "北京市", label: "北京市" },
        { id: "上海市", label: "上海市" },
        { id: "天津市", label: "天津市" },
        { id: "武汉市", label: "武汉市" },
        { id: "南京市", label: "南京市" },
        { id: "青岛市", label: "青岛市" },
        { id: "成都市", label: "成都市" },
        { id: "厦门市", label: "厦门市" },
        { id: "宁波市", label: "宁波市" },
        { id: "杭州市", label: "杭州市" },
        { id: "西安市", label: "西安市" },
        { id: "武汉市", label: "武汉市" },
        { id: "深圳市", label: "深圳市" },
      ],
      shop_edits: [],
      shop_categorys: "",
      shop_kp_categorys: [
        { id: "初次联系（微信/电话沟通）", label: "初次联系（微信/电话沟通）" },
        { id: "待约见客户未见面（意向）", label: "待约见客户未见面（意向）" },
        { id: "已到店可跟（潜在）", label: "已到店可跟（潜在）" },
        { id: "已到店意向不大", label: "已到店意向不大" },
        { id: "已签约客户（新签）", label: "已签约客户（新签）" },
        { id: "已签约老客户（续约）", label: "已签约老客户（续约）" },
      ],
      shop_add_form: "",
      shop_add_form_edit: "",
      shop_edit: {
        shop_table_row: undefined,
        shop_id_edit: undefined,
        shop_name_edit: undefined,
        shop_effect_edit: undefined,
        shop_service_edit: undefined,
        shop_surroundings_edit: undefined,
        shop_tags_edit: undefined,
        shop_kp_name_edit: undefined,
        shop_telephonenumber_edit: undefined,
        shop_kp_position_edit: undefined,
        shop_kp_city_edit: undefined,
        shop_kp_category_edit: undefined,
        shop_business_district_edit: undefined,
        shop_region_edit: undefined,
        shop_kp_wechat_id_edit: undefined,
        shop_address_edit: undefined,
        user_edit: undefined,
        text_edit: undefined,
        shop_city_edit: undefined,
        shop_add_form_edit: undefined,
      },
      type: "合作状态",
      region: "区域",
      category: "行业",
      business_district: "商圈",
      tableData: [],
      multipleSelection: [],
      cities: "城市",
      city: "城市",
      total: 0,
      pagesize: 10,
      currentPage: 1,
      select_loading: true,
      drawer: false,
      direction: "rtl",
      options: [],
      updated_time: "2020-02-14",
      formLabelWidth: "80px",
      timer: null,
      editData: {},
      roles: "",
      remoteFuncs: {},
      dynamicData: {},
      time: "",
      xiaoshou_value: "",
      xiaoshou_options: [],
    };
  },
  created: function () {
    this.roles = global.state["avatar"];
    if (global.state["avatar"] === "admin") {
      this.get_xiaoshou_data();
    }
    this.get_cities();
    this.addUser(
      this.pagesize,
      this.currentPage,
      this.region,
      this.business_district,
      this.category,
      this.type,
      "",
      this.xiaoshou_value
    );
    // this.shangquan("商圈");
  },
  mounted() {
    if (this.timer) {
      clearInterval(this.timer);
    } else {
      this.timer = setInterval(() => {
        if (
          this.category.length === 0 &&
          this.region.length === 0 &&
          this.business_district.length === 0
        ) {
          this.addUser(
            this.pagesize,
            this.currentPage,
            "区域",
            "商圈",
            "行业",
            this.type,
            this.listQuery.title,
            this.xiaoshou_value
          );
        } else if (
          this.category.length > 0 &&
          this.region.length === 0 &&
          this.business_district.length === 0
        ) {
          this.addUser(
            this.pagesize,
            this.currentPage,
            "区域",
            "商圈",
            JSON.stringify(this.category),
            this.type,
            this.listQuery.title,
            this.xiaoshou_value
          );
        } else if (
          this.category.length > 0 &&
          this.region.length > 0 &&
          this.business_district.length === 0
        ) {
          this.addUser(
            this.pagesize,
            this.currentPage,
            JSON.stringify(this.region),
            "商圈",
            JSON.stringify(this.category),
            this.type,
            this.listQuery.title,
            this.xiaoshou_value
          );
        } else if (
          this.category.length === 0 &&
          this.region.length > 0 &&
          this.business_district.length === 0
        ) {
          this.addUser(
            this.pagesize,
            this.currentPage,
            JSON.stringify(this.region),
            "商圈",
            "行业",
            this.type,
            this.listQuery.title,
            this.xiaoshou_value
          );
        } else if (
          this.category.length === 0 &&
          this.region.length > 0 &&
          this.business_district.length >= 0
        ) {
          this.addUser(
            this.pagesize,
            this.currentPage,
            JSON.stringify(this.region),
            JSON.stringify(this.business_district),
            "行业",
            this.type,
            this.listQuery.title,
            this.xiaoshou_value
          );
        } else if (
          this.category.length === 0 &&
          this.region.length === 0 &&
          this.business_district.length > 0
        ) {
          this.addUser(
            this.pagesize,
            this.currentPage,
            "区域",
            JSON.stringify(this.business_district),
            "行业",
            this.type,
            this.listQuery.title,
            this.xiaoshou_value
          );
        } else {
          this.addUser(
            this.pagesize,
            this.currentPage,
            JSON.stringify(this.region),
            JSON.stringify(this.business_district),
            JSON.stringify(this.category),
            this.type,
            this.listQuery.title,
            this.xiaoshou_value
          );
        }
      }, 1000);
    }
  },
  methods: {
    type_select() {
      this.$refs.chooseKpi5.blur();
    },
    business_district_select() {
      this.$refs.chooseKpi2.blur();
    },
    region_select() {
      this.$refs.chooseKpi.blur();
    },
    category_select() {
      this.$refs.chooseKpi3.blur();
    },
    city_select() {
      this.$refs.chooseKpi4.blur();
    },
    get_cities() {
      this.axios
        .get("http://127.0.0.1:8000/app/get_cities/", {
          params: {
            // 每页显示的条数
            username: global.state["first_name"],
          },
        })
        .then((res) => {
          this.cities = res.data.data;
        })
        .catch(function (error) {
          this.loading = false;
          console.log(error);
        });
    },
    select_urban_area() {
      this.axios
        .get("http://127.0.0.1:8000/app/select_urban_area_user/", {
          params: {
            // 每页显示的条数
            city: JSON.stringify(this.city),
          },
        })
        .then((res) => {
          // this.business_districts = res.data.data
          this.regions = res.data.data;
          this.business_loading = false;
        })
        .catch(function (error) {
          this.business_loading = false;
          console.log(error);
        });
    },
    search_business_circle(data) {
      console.log(data);
      this.axios
        .get("http://127.0.0.1:8000/app/search_business_circle/", {
          params: {
            city: JSON.stringify(this.city),
            // 每页显示的条数
            region: JSON.stringify(data),
          },
        })
        .then((res) => {
          this.business_districts = res.data.data;
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
            username: global.state["first_name"],
          },
        })
        .then((body) => {
          this.xiaoshou_options = body.data.data;
        });
    },
    handleClose() {
      this.drawer = false;
      this.edit_shop();
    },
    open(row) {
      this.$confirm("确定要将客户退回到公海吗? 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.axios
            .get("http://127.0.0.1:8000/app/pull_back/", {
              params: {
                // 每页显示的条数
                username: global.state["first_name"],
                shop_id: row.shop_id,
                shop_name: row.shop_name,
                shop_start: row.shop_start,
                shop_review_count: row.shop_review_count,
                shop_bad_review: row.shop_bad_review,
                shop_per_capita_consumption: row.shop_per_capita_consumption,
                shop_effect: row.shop_effect,
                shop_surroundings: row.shop_surroundings,
                shop_service: row.shop_service,
                shop_region: row.shop_region,
                shop_business_district: row.shop_business_district,
                shop_category: row.shop_category,
                shop_address: row.shop_address,
                shop_telephonenumber: row.shop_telephonenumber,
                shop_edit: row.shop_edit,
                shop_tags: row.shop_tags,
                shop_kp_name: row.shop_kp_name,
                shop_kp_wechat_id: row.shop_kp_wechat_id,
                shop_kp_city: row.shop_kp_city,
                shop_kp_category: row.shop_kp_category,
                shop_kp_position: row.shop_kp_position,
                shop_city: row.shop_city,
                shop_add_form: JSON.stringify(row.shop_add_form),
              },
            })
            .then((res) => {
              this.$notify({
                title: "回退成功",
                message: "",
                type: "success",
              });
            })
            .catch(function (error) {
              this.loading = false;
              console.log(error);
            });
        })
        .catch(() => {
          this.$notify({
            title: "已取消退回",
            message: "",
            type: "info",
          });
        });
    },
    xuanze(data) {
      console.log("data", data.id);
      this.shop_categorys = data.id;
      console.log(this.shop_categorys);
    },
    // 查找商户数据
    addUser(
      n1,
      n2,
      region,
      business_district,
      category,
      type,
      search,
      username
    ) {
      if (username === "") {
        username = global.state["first_name"];
      }
      this.axios
        .get("http://127.0.0.1:8000/app/table_simple_user_data/", {
          params: {
            // 每页显示的条数
            pagesize: n1,
            // 显示第几页
            currentPage: n2,
            shop_business_district: region,
            shop_category: business_district,
            shop_region: category,
            shop_type: type,
            search: search,
            username: username,
            city: JSON.stringify(this.city),
          },
        })
        .then((res) => {
          this.tableData = res.data.data;
          this.total = res.data.total;
          this.loading = false;
        });
    },
    edit_shop() {
      console.log("1");
      console.log(this.shop_edit.text_edit);
      console.log(this.shop_edit.shop_id_edit);
      if (this.shop_edit.text_edit == "" || this.shop_edit.text_edit == null) {
        console.log("空的");
      } else {
        this.axios
          .get("http://127.0.0.1:8000/app/table_simple_user_data_edit/", {
            params: {
              shop_edit: this.shop_edit.text_edit,
              shop_id: this.shop_edit.shop_id_edit,
              username: global.state["first_name"],
            },
          })
          .then((res) => {
            this.$notify({
              title: "操作成功",
              message: "",
              type: "success",
            });
            this.shop_edit.text_edit = null;
          })
          .catch(function (error) {
            this.loading = false;
            console.log(error);
          });
      }
    },
    pull_get(row) {
      console.log("用户名", row);
      this.axios
        .get("http://127.0.0.1:8000/app/pull_back/", {
          params: {
            // 每页显示的条数
            username: global.state["first_name"],
            shop_id: row.shop_id,
            shop_name: row.shop_name,
            shop_start: row.shop_start,
            shop_review_count: row.shop_review_count,
            shop_bad_review: row.shop_bad_review,
            shop_per_capita_consumption: row.shop_per_capita_consumption,
            shop_effect: row.shop_effect,
            shop_surroundings: row.shop_surroundings,
            shop_service: row.shop_service,
            shop_region: row.shop_region,
            shop_business_district: row.shop_business_district,
            shop_category: row.shop_category,
            shop_address: row.shop_address,
            shop_telephonenumber: row.shop_telephonenumber,
            shop_edit: row.shop_edit,
            shop_tags: row.shop_tags,
            shop_kp_name: row.shop_kp_name,
            shop_kp_wechat_id: row.shop_kp_wechat_id,
            shop_kp_city: row.shop_kp_city,
            shop_kp_category: row.shop_kp_category,
            shop_kp_position: row.shop_kp_position,
            shop_city: row.shop_city,
            shop_add_form: JSON.stringify(row.shop_add_form),
          },
        })
        .then((res) => {
          if (res.data.state == 1) {
            this.$notify({
              title: "回退成功",
              message: "",
              type: "success",
            });
          } else {
            this.$notify({
              title: "回退失败",
              message: "请联系管理员",
              type: "success",
            });
          }
        })
        .catch(function (error) {
          this.loading = false;
          console.log(error);
        });
    },
    get_shop_edit(shop_id) {
      this.axios
        .get("http://127.0.0.1:8000/app/table_simple_get_edit/", {
          params: {
            // 每页显示的条数
            shop_id: shop_id,
            leixing: "私海",
          },
        })
        .then((res) => {
          this.shop_edits = res.data.data;
          console.log("编辑信息", this.shop_edits);
        })
        .catch(function (error) {
          this.loading = false;
          console.log(error);
        });
    },
    get_shop_add_form(shop_id) {
      this.shop_add_form = "";
      this.axios
        .get("http://127.0.0.1:8000/app/table_simple_get_form/", {
          params: {
            // 每页显示的条数
            shop_id: shop_id,
            leixing: "私海",
          },
        })
        .then((res) => {
          this.shop_add_form = res.data.data;
          console.log("编辑信息", this.shop_add_form);
          for (var i = 0, len = this.shop_add_form.length; i < len; i++) {
            this.shop_edit[i] = undefined;
          }
          console.log(this.shop_edit);
        })
        .catch(function (error) {
          this.loading = false;
          console.log(error);
        });
    },
    get_shop_add_form_baifang(shop_id) {
      this.axios
        .get("http://127.0.0.1:8000/app/get_form/", {})
        .then((res) => {
          this.dynamicValidateForm.shop_add_form_baifang = res.data.data;
          for (
            var i = 0,
              len = this.dynamicValidateForm.shop_add_form_baifang.length;
            i < len;
            i++
          ) {
            this.shop_edit[i] = undefined;
          }
          console.log(this.dynamicValidateForm.shop_add_form_baifang.length);
        })
        .catch(function (error) {
          this.loading = false;
          console.log(error);
        });
    },
    // 查找商圈,根据选择的城区
    shangquan(region) {
      this.axios
        .get("http://127.0.0.1:8000/app/search_business_circle/", {
          params: {
            // 每页显示的条数
            region: region,
          },
        })
        .then((res) => {
          this.business_districts = res.data.data;
        })
        .catch(function (error) {
          this.loading = false;
          console.log(error);
        });
    },
    // 根据城区查找数据
    regions_data(data) {
      this.region = data.label;
      if (this.business_district != "商圈") {
        this.business_district = "商圈";
      }
      this.shangquan(data.label);
      // this.addUser(
      //   this.pagesize,
      //   this.currentPage,
      //   data.label,
      //   this.business_district,
      //   this.category,
      //   this.type,
      //   this.listQuery.title,
      //   this.xiaoshou_value
      // )
      this.qryTableDate();
    },
    edit_shop_add_form(index, value) {
      console.log("失去焦点", this.shop_edit.shop_id_edit, index, value);
      this.axios
        .get("http://127.0.0.1:8000/app/edit_shop_add_form_data/", {
          params: {
            // 每页显示的条数
            shop_id: this.shop_edit.shop_id_edit,
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
    edit_shop_add_form_baifang(index, value) {
      console.log(
        "this.shop_add_form_baifang",
        this.dynamicValidateForm.shop_add_form_baifang
      );
      this.axios
        .get("http://127.0.0.1:8000/app/edit_shop_add_form_data/", {
          params: {
            // 每页显示的条数
            shop_id: this.row.shop_id,
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
    // 根据商圈查找数据
    business_district_data(data) {
      // 如果上面:value赋的是对象，则可以将返回的对象赋予其他变量，这里的data是选中的对象，那么data.label则是reasonTypes中的label值，如果下拉中选中美国，那么this.selectVal 值为“美国”
      this.business_district = data.label;
      this.shangquan(this.region);
      // this.addUser(
      //   this.pagesize,
      //   this.currentPage,
      //   this.region,
      //   data.label,
      //   this.category,
      //   this.type,
      //   this.listQuery.title,
      //   this.xiaoshou_value
      // )
      this.qryTableDate();
    },
    // 根据品类查找数据
    category_data(data) {
      this.category = data.label;
      // this.addUser(
      //   this.pagesize,
      //   this.currentPage,
      //   this.region,
      //   this.business_district,
      //   data.label,
      //   this.type,
      //   this.listQuery.title,
      //   this.xiaoshou_value
      // )
    },
    // 修改城区数据
    business_district_edit(data) {
      this.shop_edit.shop_business_district_edit = data.label;
      this.shangquan(data.label);
    },
    // 修改商圈数据
    category_edit(data) {
      this.shangquan(this.shop_edit.shop_business_district_edit);
      this.shop_edit.shop_category_edit = data.label;
    },
    // 修改品类数据
    regions_data_edit(data) {
      this.shop_edit.shop_region_edit = data.label;
    },
    // 修改客户类别数据
    kp_category_edit(data) {
      this.shop_edit.shop_kp_category_edit = data.label;
    },
    // 修改客户所在城市数据
    kp_city_edit(data) {
      this.shop_edit.shop_kp_city_edit = data.label;
    },
    // 修改客户类别数据
    kp_position_edit(data) {
      this.shop_edit.shop_kp_position_edit = data.label;
    },
    select_shop_data(n1, n2, data) {
      this.axios
        .get("http://127.0.0.1:8000/app/select_shop_data/", {
          params: {
            // 每页显示的条数
            shop_name: data,
            pagesize: n1,
            // 显示第几页
            currentPage: n2,
          },
        })
        .then((res) => {})
        .catch(function (error) {
          this.loading = false;
          console.log(error);
        });
    },
    // 根据类型查找数据
    type_data(data) {
      this.type = data.label;
      // this.addUser(
      //   this.pagesize,
      //   this.currentPage,
      //   this.region,
      //   this.business_district,
      //   this.category,
      //   data.label,
      //   this.listQuery.title,
      //   this.xiaoshou_value
      // )
    },
    // 查询框
    select_input(e) {
      console.log(this.listQuery.title);
      this.listQuery.title = e;
      // this.addUser(
      //   this.pagesize,
      //   this.currentPage,
      //   this.region,
      //   this.business_district,
      //   this.category,
      //   this.type,
      //   e,
      //   this.xiaoshou_value
      // )
    },
    // 表格单击事件(弹出抽屉修改)
    data_update(row, event, column) {
      this.shop_edit.text_edit = "";
      this.drawer = true;
      this.shop_edit.shop_table_row = row;
      this.shop_edit.shop_id_edit = row.shop_id;
      this.shop_edit.shop_name_edit = row.shop_name;
      if (row.shop_tags == "新签") {
        this.shop_edit.shop_tags_edit = 1;
      } else if (row.shop_tags == "断约") {
        this.shop_edit.shop_tags_edit = 2;
      } else if (row.shop_tags == "续约") {
        this.shop_edit.shop_tags_edit = 3;
      } else if (row.shop_tags == "新店") {
        this.shop_edit.shop_tags_edit = 4;
      } else {
        this.shop_edit.shop_tags_edit = 0;
      }
      this.get_shop_edit(row.shop_id);
      this.get_shop_add_form(row.shop_id);
      this.shop_edit.shop_kp_name_edit = row.shop_kp_name;
      this.shop_edit.shop_city_edit = row.shop_city;
      this.shop_edit.shop_telephonenumber_edit = row.shop_telephonenumber;
      this.shop_edit.shop_kp_position_edit = row.shop_kp_position;
      this.shop_edit.shop_kp_city_edit = row.shop_kp_city;
      this.shop_edit.shop_kp_category_edit = row.shop_kp_category;
      this.shop_edit.shop_business_district_edit = row.shop_business_district;
      this.shop_edit.shop_category_edit = row.shop_category;
      this.shop_edit.shop_region_edit = row.shop_region;
      this.shop_edit.shop_kp_wechat_id_edit = row.shop_kp_wechat_id;
      this.shop_edit.shop_address_edit = row.shop_address;
      this.shop_edit.user_edit = global.state["first_name"];
      this.shop_edit.shop_add_form_edit = row.shop_add_form;
      this.shop_edit.shop_effect_edit = row.shop_effect;
      this.shop_edit.shop_service_edit = row.shop_service;
      this.shop_edit.shop_surroundings_edit = row.shop_surroundings;
    },
    handleEdit(row, event, column) {
      this.dialogFormVisible = true;
      this.get_shop_add_form_baifang();
      this.row = row;
    },
    submit_shop_add_name_baifang(formName) {
      for (let i = 0; i < this.dynamicValidateForm.shop_add_form_baifang.length; i++) {
        delete this.dynamicValidateForm.shop_add_form_baifang[i]["select"]
      } 
      console.log(this.dynamicValidateForm.shop_add_form_baifang)
      //删除字典里的SELECT值
      this.$refs[formName].validate((valid) => {
        if (valid) {
          var date = new Date();
          var seperator1 = "-";
          var year = date.getFullYear();
          var month = date.getMonth() + 1;
          var strDate = date.getDate();
          if (month >= 1 && month <= 9) {
            month = "0" + month;
          }
          if (strDate >= 0 && strDate <= 9) {
            strDate = "0" + strDate;
          }
          this.time = year + seperator1 + month + seperator1 + strDate;
          this.axios
            .get("http://127.0.0.1:8000/app/edit_shop_add_form_data_baifang/", {
              params: {
                // 每页显示的条数
                shop_id: this.row.shop_id,
                shop_name: this.row.shop_name,
                shop_kp_categorys: this.shop_categorys,
                username: global.state["first_name"],
                time: this.time,
                form_data: JSON.stringify(this.dynamicValidateForm.shop_add_form_baifang),
              },
            })
            .then((res) => {
              this.$notify({
                title: "添加成功",
                message: "",
                type: "success",
              });
              this.dialogFormVisible = false;
            })
            .catch(function (error) {
              this.loading = false;
              console.log(error);
            });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    current_change: function (currentPage) {
      this.currentPage = currentPage;
    },
    // 跳转到大众点评商户页面
    jump_href(href, row) {
      console.log(row);
      window.open("https://www.dianping.com/shop/" + row.shop_id);
    },
    // 分页
    // 每页显示的条数
    handleSizeChange(val) {
      // 改变每页显示的条数
      this.pagesize = val;
      // 点击每页显示的条数时，显示第一页
      if (
        this.category.length === 0 &&
        this.region.length === 0 &&
        this.business_district.length === 0
      ) {
        this.addUser(
          val,
          this.currentPage,
          "区域",
          "商圈",
          "行业",
          this.type,
          this.listQuery.title,
          this.xiaoshou_value
        );
      } else if (
        this.category.length > 0 &&
        this.region.length === 0 &&
        this.business_district.length === 0
      ) {
        this.addUser(
          val,
          this.currentPage,
          "区域",
          "商圈",
          JSON.stringify(this.category),
          this.type,
          this.listQuery.title,
          this.xiaoshou_value
        );
      } else if (
        this.category.length > 0 &&
        this.region.length > 0 &&
        this.business_district.length === 0
      ) {
        this.addUser(
          val,
          this.currentPage,
          JSON.stringify(this.region),
          "商圈",
          JSON.stringify(this.category),
          this.type,
          this.listQuery.title,
          this.xiaoshou_value
        );
      } else if (
        this.category.length === 0 &&
        this.region.length > 0 &&
        this.business_district.length === 0
      ) {
        this.addUser(
          val,
          this.currentPage,
          JSON.stringify(this.region),
          "商圈",
          "行业",
          this.type,
          this.listQuery.title,
          this.xiaoshou_value
        );
      } else if (
        this.category.length === 0 &&
        this.region.length > 0 &&
        this.business_district.length >= 0
      ) {
        this.addUser(
          val,
          this.currentPage,
          JSON.stringify(this.region),
          JSON.stringify(this.business_district),
          "行业",
          this.type,
          this.listQuery.title,
          this.xiaoshou_value
        );
      } else if (
        this.category.length === 0 &&
        this.region.length === 0 &&
        this.business_district.length > 0
      ) {
        this.addUser(
          val,
          this.currentPage,
          "区域",
          JSON.stringify(this.business_district),
          "行业",
          this.type,
          this.listQuery.title,
          this.xiaoshou_value
        );
      } else {
        this.addUser(
          val,
          this.currentPage,
          JSON.stringify(this.region),
          JSON.stringify(this.business_district),
          JSON.stringify(this.category),
          this.type,
          this.listQuery.title,
          this.xiaoshou_value
        );
      }
      this.qryTableDate();
      // 注意：在改变每页显示的条数时，要将页码显示到第一页
    },
    // 显示第几页
    handleCurrentChange(val) {
      console.log("第几页", val);
      // 改变默认的页数
      this.currentPage = val;
      // 切换页码时，要获取每页显示的条数
      if (
        this.category.length === 0 &&
        this.region.length === 0 &&
        this.business_district.length === 0
      ) {
        this.addUser(
          this.pagesize,
          val,
          "区域",
          "商圈",
          "行业",
          this.type,
          this.listQuery.title,
          this.xiaoshou_value
        );
      } else if (
        this.category.length > 0 &&
        this.region.length === 0 &&
        this.business_district.length === 0
      ) {
        this.addUser(
          this.pagesize,
          val,
          "区域",
          "商圈",
          JSON.stringify(this.category),
          this.type,
          this.listQuery.title,
          this.xiaoshou_value
        );
      } else if (
        this.category.length > 0 &&
        this.region.length > 0 &&
        this.business_district.length === 0
      ) {
        this.addUser(
          this.pagesize,
          val,
          JSON.stringify(this.region),
          "商圈",
          JSON.stringify(this.category),
          this.type,
          this.listQuery.title,
          this.xiaoshou_value
        );
      } else if (
        this.category.length === 0 &&
        this.region.length > 0 &&
        this.business_district.length === 0
      ) {
        this.addUser(
          this.pagesize,
          val,
          JSON.stringify(this.region),
          "商圈",
          "行业",
          this.type,
          this.listQuery.title,
          this.xiaoshou_value
        );
      } else if (
        this.category.length === 0 &&
        this.region.length > 0 &&
        this.business_district.length >= 0
      ) {
        this.addUser(
          this.pagesize,
          val,
          JSON.stringify(this.region),
          JSON.stringify(this.business_district),
          "行业",
          this.type,
          this.listQuery.title,
          this.xiaoshou_value
        );
      } else if (
        this.category.length === 0 &&
        this.region.length === 0 &&
        this.business_district.length > 0
      ) {
        this.addUser(
          this.pagesize,
          val,
          "区域",
          JSON.stringify(this.business_district),
          "行业",
          this.type,
          this.listQuery.title,
          this.xiaoshou_value
        );
      } else {
        this.addUser(
          this.pagesize,
          val,
          JSON.stringify(this.region),
          JSON.stringify(this.business_district),
          JSON.stringify(this.category),
          this.type,
          this.listQuery.title,
          this.xiaoshou_value
        );
      }
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
input[disabled],
input:disabled,
input.disabled {
  color: #333;
  -webkit-text-fill-color: #333;
  -webkit-opacity: 1;
  opacity: 1;
}
@media only screen and (max-width: 500px) {
  .el-drawer {
    width: 100%;
  }
}
</style>
