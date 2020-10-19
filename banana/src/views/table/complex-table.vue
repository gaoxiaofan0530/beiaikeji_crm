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
              :disabled="true"
              placeholder="请选择活动区域"
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
              :disabled="true"
              placeholder="请输入门店地址"
            />
          </el-form-item>
          <el-form-item label="效果" :label-width="formLabelWidth">
            <el-input
              v-model="shop_edit.shop_effect_edit"
              :disabled="true"
              style="width:80%"
              placeholder
            />
          </el-form-item>
          <el-form-item label="服务" :label-width="formLabelWidth">
            <el-input
              v-model="shop_edit.shop_service_edit"
              :disabled="true"
              style="width:80%"
              placeholder
            />
          </el-form-item>
          <el-form-item label="环境" :label-width="formLabelWidth">
            <el-input
              v-model="shop_edit.shop_surroundings_edit"
              :disabled="true"
              style="width:80%"
              placeholder
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
              <el-input v-model="domain.value" :disabled="true" @blur="edit_shop_add_form(index,domain.value)" />
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
              id="messageInput"
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
          <!-- <fm-generate-form
            :data="jsonData"
            :remote="remoteFuncs"
            :value="editData"
            :remote-option="dynamicData"
            ref="generateForm"
          ></fm-generate-form>-->
        </el-form>
      </div>
    </el-drawer>
    <el-dialog title="添加商户" :visible.sync="dialogFormVisible">
      <el-form ref="create" :rules="rules" :model="create">
        <el-form-item label="点评id" prop="shop_id" :label-width="formLabelWidth">
          <el-input v-model="create.shop_id" autocomplete="off" />
        </el-form-item>
        <el-form-item label="店名" prop="shop_name" :label-width="formLabelWidth">
          <el-input v-model="create.shop_name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="星级" prop="shop_start" :label-width="formLabelWidth">
          <el-input v-model="create.shop_start" autocomplete="off" />
        </el-form-item>
        <el-form-item label="评论数" prop="shop_review_count" :label-width="formLabelWidth">
          <el-input v-model="create.shop_review_count" autocomplete="off" />
        </el-form-item>
        <el-form-item label="人均消费" prop="shop_per_capita_consumption" :label-width="formLabelWidth">
          <el-input v-model="create.shop_per_capita_consumption" autocomplete="off" />
        </el-form-item>
        <el-form-item label="效果" prop="shop_effect" :label-width="formLabelWidth">
          <el-input v-model="create.shop_effect" autocomplete="off" />
        </el-form-item>
        <el-form-item label="服务" prop="shop_service" :label-width="formLabelWidth">
          <el-input v-model="create.shop_service" autocomplete="off" />
        </el-form-item>
        <el-form-item label="环境" prop="shop_surroundings" :label-width="formLabelWidth">
          <el-input v-model="create.shop_surroundings" autocomplete="off" />
        </el-form-item>
        <el-form-item label="地址" prop="shop_address" :label-width="formLabelWidth">
          <el-input v-model="create.shop_address" autocomplete="off" />
        </el-form-item>
        <el-form-item label="电话" prop="shop_telephonenumber" :label-width="formLabelWidth">
          <el-input v-model="create.shop_telephonenumber" autocomplete="off" />
        </el-form-item>
        <el-form-item label="城市" prop="shop_city" :label-width="formLabelWidth">
          <el-select
            ref="chooseKpi19"
            v-model="create.shop_city"
            class="filter-item"
            value-key="id"
            filterable
            placeholder="请选择门店所在城市"
            @blur="chooseKpi19"
            @change="shop_city_select"
          >
            <el-option v-for="item in shop_citys" :key="item.id" :label="item.label" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="区域" prop="shop_business_district" :label-width="formLabelWidth">
          <el-select
            ref="chooseKpi20"
            v-model="create.shop_business_district"
            class="filter-item"
            value-key="id"
            filterable
            placeholder="请选择门店所在城区"
            @blur="chooseKpi20"
            @change="shop_business_district_select"
          >
            <el-option v-for="item in select_regions" :key="item.id" :label="item.label" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="商圈" prop="shop_category" :label-width="formLabelWidth">
          <el-select
            v-model="create.shop_category"
            ref="chooseKpi21"
            class="filter-item"
            value-key="id"
            filterable
            placeholder="请选择门店所在商圈"
            @blur="chooseKpi21"
            @change="shop_category"
          >
            <el-option
              v-for="item in shop_category_create"
              :key="item.id"
              :label="item.label"
              :value="item"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="品类" prop="shop_region" :label-width="formLabelWidth">
          <el-select
            ref="chooseKpi22"
            v-model="create.shop_region"
            class="filter-item"
            value-key="id"
            filterable
            placeholder="请选择门店所在品类"
            @blur="chooseKpi22"
            @change="regions_data_edit_create"
          >
            <el-option v-for="item in categorys" :key="item.id" :label="item.label" :value="item" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="create_table('create');resetForm('create')">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="便捷添加商户" :visible.sync="dialogFormVisible_append">
      <el-form ref="create" :rules="rules" :model="create">
        <el-form-item label="点评网址" prop="url2" :label-width="formLabelWidth">
          <el-input v-model="create.url2" autocomplete="off" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible_append = false">取 消</el-button>
        <el-button type="success" @click="append_table('create');resetForm_append('create')">确 定</el-button>
      </div>
    </el-dialog>
    <div class="filter-container" style="margin-left:15px;margin-top:25px;">
      <el-input
        v-model="listQuery.title"
        style="width: 200px;"
        class="filter-item"
        placeholder="全部"
        @input="select_input"
      >
        <i slot="prefix" class="el-input__icon el-icon-search" />
      </el-input>
      <el-select
        ref="chooseKpi"
        v-model="region"
        multiple
        collapse-tags
        clearable
        class="filter-item"
        value-key="id"
        style="width:180px;"
        placeholder="城区"
        @blur="region_select"
        @focus="select_urban_area($event)"
        @change="blur_business_circle"
      >
        <el-option v-for="item in regions" :key="item.id" :label="item.label" :value="item.id" />
      </el-select>
      <el-select
        ref="chooseKpi2"
        v-model="business_district"
        multiple
        collapse-tags
        class="filter-item"
        style="width:180px;"
        value-key="id"
        @blur="business_district_select"
        placeholder="商圈"
        @change="addUser"
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
        class="filter-item"
        value-key="id"
        style="width:180px;"
        placeholder="品类"
        @blur="category_select"
        @change="addUser"
      >
        <el-option v-for="item in categorys" :key="item.id" :label="item.label" :value="item.id" />
      </el-select>
      <el-select
        v-model="type"
        ref="chooseKpi4"
        class="filter-item"
        style="width:130px;"
        value-key="id"
        placeholder="类型"
        @blur="type_select"
        @change="type_data"
      >
        <el-option v-for="item in types" :key="item.id" :label="item.label" :value="item" />
      </el-select>
      <el-button type="success" class="filter-item" @click="dialogFormVisible_append = true">便捷添加商户</el-button>
      <el-button type="primary" class="filter-item" @click="dialogFormVisible = true">添加商户</el-button>
      <span>更新时间：{{ num }}</span>
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
      @sort-change="sortChange"
    >
      <!-- <el-table-column type="selection" width="55"></el-table-column> -->
      <el-table-column prop="shop_id" label="商户ID" show-overflow-tooltip @click.stop />
      <el-table-column label="店名" prop="shop_name" width="450">
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
            <span v-if="row.shop_kp_category !== ''">
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
            <span
              v-if="row.shop_kp_category !== '' && row.shop_kp_category !== None && row.shop_kp_category !== Null"
            >
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
            <span v-if="row.shop_kp_category !== ''">
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
            <span v-if="row.shop_kp_category !== ''">
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
            <span v-if="row.shop_kp_category !== ''">
              <el-tag type effect="dark">{{ row.shop_kp_category }}</el-tag>
            </span>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="shop_start" label="星级" show-overflow-tooltip/>
      <el-table-column prop="shop_review_count" show-overflow-tooltip label="评论数" />
      <el-table-column prop="shop_business_district" show-overflow-tooltip label="区域">
        <!-- <template slot="header">
          <el-input v-model="search" size="mini" placeholder="输入关键字搜索" />
        </template>-->
      </el-table-column>
      <el-table-column prop="shop_category" show-overflow-tooltip label="商圈" />
      <el-table-column prop="shop_region" show-overflow-tooltip label="品类" />
      <!-- <el-table-column prop="shop_per_capita_consumption" label="人均消费" width="150"></el-table-column> -->
      <el-table-column
        prop="shop_telephonenumber"
        show-overflow-tooltip
        sortable="custom"
        label="电话"
      />
      <el-table-column label="操作" width="210" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-tooltip class="item" effect="dark" content="访问" placement="top-start">
            <el-button size="mini" type="success" @click.stop="jump_href(scope.$index, scope.row);">
              <i class="el-icon-sort" />
            </el-button>
          </el-tooltip>
          <el-tooltip class="item" effect="dark" content="查看" placement="top-start">
            <el-button
              size="mini"
              type="primary"
              content="查看"
              placement="top"
              @click="handleEdit(scope.$index, scope.row)"
            >
              <i class="el-icon-edit-outline" />
            </el-button>
          </el-tooltip>
          <el-tooltip class="item" effect="dark" content="拉入" placement="top-start">
            <el-button
              size="mini"
              type="danger"
              content="拉入"
              placement="top"
              @click.stop="pull_get(scope.row);"
            >
              <i class="el-icon-download" />
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
import request from '@/utils/request'
import global from '@/store/modules/user'
import city from '@/layout/components/Navbar'
import Utils from '@/api/util'

export default {
  name: 'DataList',
  data() {
    return {
      num: '2020',
      regions: [],
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
          id: '行业',
          label: '行业'
        }
      ],
      select_regions: [],
      dialogFormVisible_append:false,
      // business_districts: [{'label': '西单', 'id': '西单'}, {'label': '西直门/动物园', 'id': '西直门/动物园'}, {'label': '月坛', 'id': '月坛'}, {'label': '什刹海', 'id': '什刹海'}, {'label': '广外大街', 'id': '广外大街'}, {'label': '前门', 'id': '前门'}, {'label': '阜成门', 'id': '阜成门'}, {'label': '新街口', 'id': '新街口'}, {'label': '牛街', 'id': '牛街'}, {'label': '地安门', 'id': '地安门'}, {'label': '虎坊桥', 'id': '虎坊桥'}, {'label': '广内大街', 'id': '广内大街'}, {'label': '德外大街', 'id': '德外大街'}, {'label': '南菜园/白纸坊', 'id': '南菜园/白纸坊'}, {'label': '陶然亭', 'id': '陶然亭'}, {'label': '菜市口', 'id': '菜市口'}, {'label': '东花园', 'id': '东花园'}, {'label': '六里桥/丽泽桥', 'id': '六里桥/丽泽桥'}, {'label': '中关村', 'id': '中关村'}, {'label': '五道口', 'id': '五道口'}, {'label': '远大路', 'id': '远大路'}, {'label': '五棵松', 'id': '五棵松'}, {'label': '航天桥', 'id': '航天桥'}, {'label': '公主坟/万寿路', 'id': '公主坟/万寿路'}, {'label': '北太平庄', 'id': '北太平庄'}, {'label': '紫竹桥', 'id': '紫竹桥'}, {'label': '苏州桥', 'id': '苏州桥'}, {'label': '魏公村', 'id': '魏公村'}, {'label': '双榆树', 'id': '双榆树'}, {'label': '清 河', 'id': '清河'}, {'label': '上地', 'id': '上地'}, {'label': '知春路', 'id': '知春路'}, {'label': '北下关', 'id': '北下关'}, {'label': '颐和 园', 'id': '颐和园'}, {'label': '万柳', 'id': '万柳'}, {'label': '大钟寺', 'id': '大钟寺'}, {'label': '人民大学', 'id': '人民大学'}, {'label': '军博', 'id': '军博'}, {'label': '学院桥', 'id': '学院桥'}, {'label': '香山', 'id': '香山'}, {'label': '四季青', 'id': '四季青'}, {'label': '农业大学西区', 'id': '农业大学西区'}, {'label': '西三旗', 'id': '西三旗'}, {'label': '北沙滩', 'id': '北沙滩'}, {'label': '田村', 'id': '田村'}, {'label': '百望山森林公园/309医院', 'id': '百望山森林公园/309医院'}, {'label': '王府井/东单', 'id': '王府井/东单'}, {'label': '北新桥/簋街', 'id': '北新桥/簋街'}, {'label': '崇文门', 'id': '崇文门'}, {'label': '安定门', 'id': '安定门'}, {'label': '东直门', 'id': '东直门'}, {'label': ' 前门', 'id': '前门'}, {'label': '建国门/北京站', 'id': '建国门/北京站'}, {'label': '东四十条', 'id': '东四十条'}, {'label': '地安门', 'id': '地安门'}, {'label': '朝阳门', 'id': '朝阳门'}, {'label': '东四', 'id': '东四'}, {'label': '广渠门内', 'id': '广渠门内'}, {'label': '和平里', 'id': '和平里'}, {'label': '沙子口', 'id': '沙子口'}, {'label': '雍和宫/地坛', 'id': '雍和宫/地坛'}, {'label': '天坛', 'id': '天坛'}, {'label': '左安门', 'id': '左安门'}, {'label': '沙滩/美术馆灯市口', 'id': '沙滩/美术馆灯市口'}, {'label': '光明楼/龙潭湖', 'id': '光明楼/龙潭湖'}, {'label': '广渠门外', 'id': '广渠门外'}, {'label': '东花园', 'id': '东花园'}, {'label': '苹果园', 'id': '苹果园'}, {'label': '鲁谷', 'id': '鲁谷'}, {'label': '古城/八角', 'id': '古城/八角'}, {'label': '模式口', 'id': '模式口'}, {'label': '八大处', 'id': '八大处'}, {'label': '国贸', 'id': '国贸'}, {'label': '三里屯', 'id': '三里屯'}, {'label': '亚运村', 'id': '亚运村'}, {'label': '工人体育场', 'id': '工人体育场'}, {'label': '望京', 'id': '望京'}, {'label': '大望路', 'id': '大望路'}, {'label': '朝外大街', 'id': '朝外大街'}, {'label': '亮马桥/三元桥', 'id': '亮马桥/三元桥'}, {'label': '蓝色港湾', 'id': '蓝色港湾'}, {'label': '劲松/潘家园', 'id': '劲松/潘家园'}, {'label': '酒仙桥', 'id': '酒仙桥'}, {'label': '太阳宫', 'id': '太阳宫'}, {'label': '劲松/潘家园', 'id': '劲松/潘家园'}, {'label': '双井', 'id': '双井'}, {'label': '芍药居', 'id': '芍药居'}, {'label': '798/大山子', 'id': '798/大山子'}, {'label': '左家庄', 'id': '左家庄'}, {'label': '安贞', 'id': '安贞'}, {'label': '青年路', 'id': '青年路'}, {'label': '十里堡', 'id': '十里堡'}, {'label': '常营', 'id': '常营'}, {'label': '小营', 'id': '小营'}, {'label': '建外大街', 'id': '建外大街'}, {'label': '朝阳公园/团结湖', 'id': '朝阳公园/团结湖'}, {'label': '霄云路', 'id': '霄云路'}, {'label': '传媒大学/二外', 'id': '传媒大学/二外'}, {'label': '管庄', 'id': '管庄'}, {'label': '北苑家园', 'v': '北苑家园'}, {'label': '百子湾', 'id': '百子湾'}, {'label': '和平里', 'id': '和平 里'}, {'label': '大屯', 'id': '大屯'}, {'label': '对外经贸', 'id': '对外经贸'}, {'label': '东坝', 'id': '东坝'}, {'label': '慈云寺/八里庄', 'id': '慈云寺/八里庄'}, {'label': '十里河', 'id': '十里河'}, {'label': '高碑店', 'id': '高碑店'}, {'label': '四惠', 'id': '四惠'}, {'label': '甜水园', 'id': '甜水园'}, {'label': '双桥', 'id': '双桥'}, {'label': '石佛营', 'id': '石佛营'}, {'label': '北京欢乐谷', 'id': '北京欢乐谷'}, {'label': '马泉营', 'id': '马泉营'}, {'label': '定福庄', 'id': '定福庄'}, {'label': '孙河', 'id': '孙河'}, {'label': '北沙滩', 'id': '北沙滩'}, {'label': '燕莎/农业展览馆', 'id': '燕莎/农业展览馆'}, {'label': '东大桥', 'id': '东大桥'}, {'label': '十八里店', 'id': '十八里店'}, {'label': '姚家园', 'id': '姚家园'}, {'label': '立水桥', 'id': '立水桥'}, {'label': '小庄/红庙', 'id': '小庄/红庙'}, {'label': '草房', 'id': '草房'}, {'label': '北京东站', 'id': '北京东站'}, {'label': '分钟寺/成寿寺', 'id': '分钟寺/成寿寺'}, {'label': '世贸天阶', 'id': '世贸天阶'}, {'label': '朝阳公 园', 'id': '朝阳公园'}, {'label': '金盏', 'id': '金盏'}, {'label': '小红门', 'id': '小红门'}, {'label': '王四营', 'id': '王四营'}, {'label': ' 广渠门外', 'id': '广渠门外'}, {'label': '总部基地', 'id': '总部基地'}, {'label': '方庄', 'id': '方庄'}, {'label': '开阳里', 'id': '开阳里'}, {'label': '北大地', 'id': '北大地'}, {'label': '青塔', 'id': '青塔'}, {'label': '北京西站/六里桥', 'id': '北京西站/六里桥'}, {'label': '六里桥/丽泽桥', 'id': '六里桥/丽泽桥'}, {'label': '花乡', 'id': '花乡'}, {'label': '刘家窑', 'id': '刘家窑'}, {'label': '右安门', 'id': '右安门'}, {'label': '马家堡/角门', 'id': '马家堡/角门'}, {'label': '宋家庄', 'id': '宋家庄'}, {'label': '看丹桥', 'id': '看丹桥'}, {'label': '公益西桥', 'id': '公益西桥'}, {'label': '洋桥/木樨园', 'id': '洋桥/木樨园'}, {'label': '草桥', 'id': '草桥'}, {'label': '云岗', 'id': '云岗'}, {'label': '大红 门', 'id': '大红门'}, {'label': '槐房万达广场', 'id': '槐房万达广场'}, {'label': '丽泽桥/丰管路', 'id': '丽泽桥/丰管路'}, {'label': '夏家胡同/ 纪家庙', 'id': '夏家胡同/纪家庙'}, {'label': '石榴庄', 'id': '石榴庄'}, {'label': '分钟寺/成寿寺', 'id': '分钟寺/成寿寺'}, {'label': '南苑机场/德茂桥', 'id': '南苑机场/德茂桥'}, {'label': '世界公园', 'id': '世界公园'}, {'label': '国展', 'id': '国展'}, {'label': '后沙峪', 'id': '后沙峪'}, {'label': '顺义', 'id': '顺义'}, {'label': '首都机场', 'id': '首都机场'}, {'label': '石园', 'id': '石园'}, {'label': '马坡牛栏山', 'id': '马坡牛栏山'}, {'label': '南彩', 'id': '南彩'}, {'label': '小汤山/央美博艺艺术馆', 'id': '小汤山/央美博艺艺术馆'}, {'label': '莲花山滑雪场', 'id': '莲花山滑雪场'}, {'label': '长阳镇', 'id': '长阳镇'}, {'label': '城关镇', 'id': '城关镇'}, {'label': '良乡', 'id': '良乡'}, {'label': '十渡镇', 'id': '十渡镇'}, {'label': '窦店镇', 'id': '窦店镇'}, {'label': '河北镇', 'id': '河北镇'}, {'label': '阎村镇', 'id': '阎村镇'}, {'label': '燕山', 'id': '燕山'}, {'label': '青龙湖镇', 'id': '青龙湖镇'}, {'label': '华冠天地', 'id': '华冠天地'}, {'label': '上方山国家森林公园', 'id': '上方山国家森林公园'}, {'label': '云居滑雪场', 'id': '云居滑雪场'}, {'label': '仙栖洞', 'id': '仙栖洞'}, {'label': '霞云岭国家森林公园', 'id': '霞云岭国家森林公园'}, {'label': '亦庄', 'id': '亦庄'}, {'label': '黄村', 'id': '黄村'}, {'label': '旧宫', 'id': '旧宫'}, {'label': '西红门', 'id': '西红门'}, {'label': '庞各庄', 'id': '庞各庄'}, {'label': '南苑机场/德茂桥', 'id': '南苑机场/德茂桥'}, {'label': '天宫院', 'id': '天宫院'}, {'label': '龙湖天街购物中心', 'id': '龙湖天街购物中心'}, {'label': '回龙观', 'id': '回龙观'}, {'label': '天通苑', 'id': '沙河'}, {'label': '南口镇', 'id': '南口镇'}, {'label': '十三陵水库', 'id': '十三陵水库'}, {'label': '明十三陵', 'id': '明十三陵'}, {'label': '天居庸关长城宫院', 'id': '天居庸关长城宫院'}, {'label': '九棵树', 'id': '九棵树'}, {'label': '通州北苑', 'id': '通州北苑'}, {'label': '新华大街', 'id': '新华大街'}, {'label': '梨园', 'id': '梨园'}, {'label': '果园', 'id': '果园'}, {'label': '武夷花园', 'id': '武夷花园'}, {'label': '物资学院', 'id': '物资学院'}, {'label': '宋庄', 'id': '宋庄'}, {'label': '马驹桥', 'id': '马驹桥'}, {'label': '西集', 'id': '西集'}, {'label': '次渠', 'id': '次渠'}, {'label': '土桥', 'id': '土桥'}, {'label': '北关', 'id': '北关'}, {'label': '怀柔区', 'id': '怀柔区'}, {'label': '平谷区', 'id': '平谷区'}, {'label': '门头沟', 'id': '门头沟'}, {'label': '延庆区其他', 'id': '延庆区其他'}, {'label': '密云镇', 'id': '密云镇'}, {'label': '十里堡镇', 'id': '十里堡镇'}, {'label': '溪翁庄镇', 'id': '溪翁庄镇'}, {'label': '东邵渠镇', 'id': '东邵渠镇'}, {'label': '密云区其他', 'id': '密云区其他'}, {'label': '商圈', 'id': '商圈'}],
      business_districts: '',
      types: [
        {
          id: '新签',
          label: '新签'
        },
        {
          id: '断约',
          label: '断约'
        },
        {
          id: '续约',
          label: '续约'
        },
        {
          id: '新店',
          label: '新店'
        },
        {
          id: '合作状态',
          label: '合作状态'
        }
      ],
      listQuery: {
        title: undefined
      },
      shop_category_create: [],
      shop_kp_position: [
        { id: '大老板', label: '大老板' },
        { id: '合伙人', label: '合伙人' },
        { id: '经理', label: '经理' },
        { id: '店长', label: '店长' },
        { id: '前台', label: '前台' },
        { id: '技师', label: '技师' }
      ],
      shop_citys: [
        { id: '北京市', label: '北京市' },
        { id: '上海市', label: '上海市' },
        { id: '广州市', label: '广州市' },
        { id: '深圳市', label: '深圳市' },
        { id: '成都市', label: '成都市' },
        { id: '杭州市', label: '杭州市' },
        { id: '重庆市', label: '重庆市' },
        { id: '武汉市', label: '武汉市' },
        { id: '西安市', label: '西安市' },
        { id: '苏州市', label: '苏州市' },
        { id: '天津市', label: '天津市' },
        { id: '南京市', label: '南京市' }
      ],
      shop_edits: [],
      shop_kp_categorys: [
        { id: '初次联系（微信/电话沟通）', label: '初次联系（微信/电话沟通）' },
        { id: '待约见客户未见面（意向）', label: '待约见客户未见面（意向）' },
        { id: '已到店可跟（潜在）', label: '已到店可跟（潜在）' },
        { id: '已到店意向不大', label: '已到店意向不大' },
        { id: '已签约客户（新签）', label: '已签约客户（新签）' },
        { id: '已签约老客户（续约）', label: '已签约老客户（续约）' }
      ],
      shop_add_form: '',
      shop_add_form_edit: '',
      create: {
        shop_id: '',
        shop_name: '',
        shop_start: '',
        shop_review_count: '',
        shop_per_capita_consumption: '',
        shop_effect: '',
        shop_service: '',
        shop_surroundings: '',
        shop_address: '',
        shop_telephonenumber: '',
        shop_business_district: '',
        shop_category: '',
        shop_region: '',
        shop_city: '',
        url2: ''
      },
      rules: {
        shop_id: [
          { required: true, message: '请输入商户id', trigger: 'blur' }
        ],
        url2: [
          { required: true, message: '请输入商户点评网址', trigger: 'blur' }
        ],
        shop_name: [
          { required: true, message: '请输入商户名', trigger: 'blur' }
        ],
        shop_start: [
          { required: true, message: '请输入商户星级', trigger: 'blur' }
        ],
        shop_review_count: [
          { required: true, message: '请输入评论数', trigger: 'blur' },
          { message: '请输入数字值', pattern: /^[0-9]*[1-9][0-9]*$/ }
        ],
        shop_per_capita_consumption: [
          { required: true, message: '请输入人均消费', trigger: 'blur' }
        ],
        shop_effect: [
          { required: true, message: '请输入效果分', trigger: 'blur' },
          {
            message: '请输入正整数或小数',
            pattern: /^-?\d{1,5}(?:\.\d{1,3})?$/
          }
        ],
        shop_service: [
          { required: true, message: '请输入环境分', trigger: 'blur' },
          {
            message: '请输入正整数或小数',
            pattern: /^-?\d{1,5}(?:\.\d{1,3})?$/
          }
        ],
        shop_surroundings: [
          { required: true, message: '请输入服务分', trigger: 'blur' },
          {
            message: '请输入正整数或小数',
            pattern: /^-?\d{1,5}(?:\.\d{1,3})?$/
          }
        ],
        shop_address: [
          { required: true, message: '请输入地址', trigger: 'blur' }
        ],
        shop_telephonenumber: [
          { required: true, message: '请输入手机号', trigger: 'blur' }
        ],
        shop_city: [{ required: true, message: '请选择城市', trigger: 'blur' }],
        shop_business_district: [
          { required: true, message: '请输入区域', trigger: 'blur' }
        ],
        shop_category: [
          { required: true, message: '请输入商圈', trigger: 'blur' }
        ],
        shop_region: [
          { required: true, message: '请输入品类', trigger: 'blur' }
        ]
      },

      shop_edit: {
        shop_table_row: undefined,
        shop_id_edit: undefined,
        shop_name_edit: undefined,
        shop_tags_edit: undefined,
        shop_effect_edit: undefined,
        shop_service_edit: undefined,
        shop_surroundings_edit: undefined,
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
        shop_add_form_edit: undefined
      },
      type: '合作状态',
      region: '区域',
      category: '行业',
      category_data: '',
      business_district: '商圈',
      tableData: [],
      multipleSelection: [],
      total: 0,
      order_by: '',
      pagesize: 10,
      currentPage: 1,
      loading: true,
      business_loading: true,
      drawer: false,
      direction: 'rtl',
      options: [],
      formLabelWidth: '80px',
      timer: null,
      editData: {},
      remoteFuncs: {},
      city: '',
      dialogFormVisible: false,
      dynamicData: {},
      edit_pull:null,
    }
  },
  created: function() {
    this.select_city()
    this.city = global.state['introduction']
    this.addUser(
      this.pagesize,
      this.currentPage,
      this.region,
      this.business_district,
      this.category,
      this.type,
      ''
    )
    this.jump_xindian()
    // this.shangquan('商圈')
    var date = new Date()
    var seperator1 = '-'
    var year = date.getFullYear()
    var month = date.getMonth() + 1
    var strDate = date.getDate()
    if (month >= 1 && month <= 9) {
      month = '0' + month
    }
    if (strDate >= 0 && strDate <= 9) {
      strDate = '0' + strDate
    }
    strDate = strDate-1
    this.num = year + seperator1 + month + seperator1 + strDate
  },
  methods: {
    type_select(){
      this.$refs.chooseKpi4.blur()
    },
    chooseKpi19(){
      this.$refs.chooseKpi19.blur()
    },
    chooseKpi20(){
      this.$refs.chooseKpi20.blur()
    },
    chooseKpi21(){
      this.$refs.chooseKpi21.blur()
    },
    chooseKpi22(){
      this.$refs.chooseKpi22.blur()
    },
    business_district_select(){
      this.$refs.chooseKpi2.blur()
    },
    region_select(){
      this.$refs.chooseKpi.blur()
    },
    category_select(){
      this.$refs.chooseKpi3.blur()
    },
    select_urban_area() {
      if (this.city === '北京市') {
        this.regions = [{ id: '西城区', label: '西城区' },
          { id: '海淀区', label: '海淀区' },
          { id: '东城区', label: '东城区' },
          { id: '石景山区', label: '石景山区' },
          { id: '朝阳区', label: '朝阳区' },
          { id: '丰台区', label: '丰台区' },
          { id: '顺义区', label: '顺义区' },
          { id: '房山区', label: '房山区' },
          { id: '大兴区', label: '大兴区' },
          { id: '昌平区', label: '昌平区' },
          { id: '通州区', label: '通州区' },
          { id: '怀柔区', label: '怀柔区' },
          { id: '密云区', label: '密云区' },
          { id: '平谷区', label: '平谷区' },
          { id: '门头沟区', label: '门头沟区' },
          { id: '延庆区', label: '延庆区' }]
      } else if (this.city === '上海市') {
        this.regions = [{ id: '静安区', label: '静安区' },
          { id: '长宁区', label: '长宁区' },
          { id: '徐汇区', label: '徐汇区' },
          { id: '杨浦区', label: '杨浦区' },
          { id: '黄浦区', label: '黄浦区' },
          { id: '虹口区', label: '虹口区' },
          { id: '普陀区', label: '普陀区' },
          { id: '闵行区', label: '闵行区' },
          { id: '宝山区', label: '宝山区' },
          { id: '浦东新区', label: '浦东新区' },
          { id: '松江区', label: '松江区' },
          { id: '嘉定区', label: '嘉定区' },
          { id: '青浦区', label: '青浦区' },
          { id: '金山区', label: '金山区' },
          { id: '奉贤区', label: '奉贤区' },
          { id: '崇明区', label: '崇明区' }]
      } else if (this.city === '广州市') {
        this.regions = [{ id: '越秀区', label: '越秀区' },
          { id: '荔湾区', label: '荔湾区' },
          { id: '天河区', label: '天河区' },
          { id: '海珠区', label: '海珠区' },
          { id: '黄埔区', label: '黄埔区' },
          { id: '番禺区', label: '番禺区' },
          { id: '白云区', label: '白云区' },
          { id: '增城区', label: '增城区' },
          { id: '花都区', label: '花都区' },
          { id: '从化区', label: '从化区' },
          { id: '南沙区', label: '南沙区' }]
      } else if (this.city === '深圳市') {
        this.regions = [{ id: '福田区', label: '福田区' },
          { id: '南山区', label: '南山区' },
          { id: '罗湖区', label: '罗湖区' },
          { id: '盐田区', label: '盐田区' },
          { id: '龙华区', label: '龙华区' },
          { id: '龙岗区', label: '龙岗区' },
          { id: '宝安区', label: '宝安区' },
          { id: '坪山区', label: '坪山区' },
          { id: '光明区', label: '光明区' }]
      } else if (this.city === '天津市') {
        this.regions = [{ id: '和平区', label: '和平区' },
          { id: '南开区', label: '南开区' },
          { id: '河西区', label: '河西区' },
          { id: '河北区', label: '河北区' },
          { id: '红桥区', label: '红桥区' },
          { id: '河东区', label: '河东区' },
          { id: '西青区', label: '西青区' },
          { id: '东丽区', label: '东丽区' },
          { id: '滨海新区', label: '滨海新区' },
          { id: '津南区', label: '津南区' },
          { id: '北辰区', label: '北辰区' },
          { id: '武清区', label: '武清区' },
          { id: '静海区', label: '静海区' },
          { id: '蓟州区', label: '蓟州区' },
          { id: '宝坻区', label: '宝坻区' },
          { id: '宁河区', label: '宁河区' }]
      } else if (this.city === '杭州市') {
        this.regions = [{ id: '上城区', label: '上城区' },
          { id: '西湖区', label: '西湖区' },
          { id: '拱墅区', label: '拱墅区' },
          { id: '滨江区', label: '滨江区' },
          { id: '下城区', label: '下城区' },
          { id: '江干区', label: '江干区' },
          { id: '萧山区', label: '萧山区' },
          { id: '余杭区', label: '余杭区' },
          { id: '富阳区', label: '富阳区' },
          { id: '临安', label: '临安' },
          { id: '建德市', label: '建德市' },
          { id: '桐庐县', label: '桐庐县' },
          { id: '淳安县', label: '淳安县' }]
      } else if (this.city === '南京市') {
        this.regions = [{ id: '秦淮区', label: '秦淮区' },
          { id: '鼓楼区', label: '鼓楼区' },
          { id: '玄武区', label: '玄武区' },
          { id: '建邺区', label: '建邺区' },
          { id: '雨花台区', label: '雨花台区' },
          { id: '栖霞区', label: '栖霞区' },
          { id: '江宁区', label: '江宁区' },
          { id: '浦口区', label: '浦口区' },
          { id: '六合区', label: '六合区' },
          { id: '溧水区', label: '溧水区' },
          { id: '高淳区', label: '高淳区' }]
      } else if (this.city === '苏州市') {
        this.regions = [{ id: '姑苏区', label: '姑苏区' },
          { id: '虎丘区', label: '虎丘区' },
          { id: '工业园区', label: '工业园区' },
          { id: '吴中区', label: '吴中区' },
          { id: '相城区', label: '相城区' },
          { id: '昆山', label: '昆山' },
          { id: '常熟', label: '常熟' },
          { id: '吴江', label: '吴江' },
          { id: '张家港', label: '张家港' },
          { id: '太仓', label: '太仓' },
          { id: '甪直', label: '甪直' }]
      } else if (this.city === '成都市') {
        this.regions = [{ id: '都江堰市', label: '都江堰市' },
          { id: '彭州市', label: '彭州市' },
          { id: '锦江区', label: '锦江区' },
          { id: '青羊区', label: '青羊区' },
          { id: '武侯区', label: '武侯区' },
          { id: '成华区', label: '成华区' },
          { id: '金牛区', label: '金牛区' },
          { id: '龙泉驿区', label: '龙泉驿区' },
          { id: '双流区', label: '双流区' },
          { id: '郫都区', label: '郫都区' },
          { id: '新都区', label: '新都区' },
          { id: '温江区', label: '温江区' },
          { id: '崇州市', label: '崇州市' },
          { id: '金堂县', label: '金堂县' },
          { id: '青白江区', label: '青白江区' },
          { id: '邛崃市', label: '邛崃市' },
          { id: '简阳市', label: '简阳市' },
          { id: '大邑县', label: '大邑县' },
          { id: '新津县', label: '新津县' },
          { id: '蒲江县', label: '蒲江县' }]
      } else if (this.city === '武汉市') {
        this.regions = [{ id: '江汉区', label: '江汉区' },
          { id: '江岸区', label: '江岸区' },
          { id: '武昌区', label: '武昌区' },
          { id: '汉阳区', label: '汉阳区' },
          { id: '硚口区', label: '硚口区' },
          { id: '青山区', label: '青山区' },
          { id: '洪山区', label: '洪山区' },
          { id: '江夏区', label: '江夏区' },
          { id: '蔡甸区', label: '蔡甸区' },
          { id: '东西湖区', label: '东西湖区' },
          { id: '黄陂区', label: '黄陂区' },
          { id: '新洲区', label: '新洲区' },
          { id: '汉南区', label: '汉南区' }]
      } else if (this.city === '重庆市') {
        this.regions = [{ id: '渝中区', label: '渝中区' },
          { id: '江北区', label: '江北区' },
          { id: '南岸区', label: '南岸区' },
          { id: '渝北区', label: '渝北区' },
          { id: '沙坪坝区', label: '沙坪坝区' },
          { id: '九龙坡区', label: '九龙坡区' },
          { id: '北碚区', label: '北碚区' },
          { id: '大渡口区', label: '大渡口区' },
          { id: '巴南区', label: '巴南区' },
          { id: '万州区', label: '万州区' },
          { id: '合川区', label: '合川区' },
          { id: '永川区', label: '永川区' },
          { id: '江津区', label: '江津区' },
          { id: '涪陵区', label: '涪陵区' },
          { id: '开州区', label: '开州区' },
          { id: '长寿区', label: '长寿区' },
          { id: '大足区', label: '大足区' },
          { id: '綦江区', label: '綦江区' },
          { id: '璧山区', label: '璧山区' },
          { id: '云阳县', label: '云阳县' },
          { id: '荣昌区', label: '荣昌区' },
          { id: '铜梁区', label: '铜梁区' },
          { id: '奉节县', label: '奉节县' },
          { id: '南川区', label: '南川区' },
          { id: '潼南区', label: '潼南区' },
          { id: '垫江县', label: '垫江县' },
          { id: '黔江区', label: '黔江区' },
          { id: '巫山县', label: '巫山县' },
          { id: '丰都县', label: '丰都县' },
          { id: '巫溪县', label: '巫溪县' },
          { id: '梁平区', label: '梁平区' },
          { id: '酉阳土家族苗族自治县', label: '酉阳土家族苗族自治县' },
          { id: '忠县', label: '忠县' },
          { id: '秀山土家族苗族自治县', label: '秀山土家族苗族自治县' },
          { id: '石柱土家族自治县', label: '石柱土家族自治县' },
          { id: '彭水苗族土家族自治县', label: '彭水苗族土家族自治县' },
          { id: '武隆区', label: '武隆区' },
          { id: '城口县', label: '城口县' }]
      } else if (this.city === '西安市') {
        this.regions = [{ id: '碑林区', label: '碑林区' },
          { id: '高新区', label: '高新区' },
          { id: '莲湖区', label: '莲湖区' },
          { id: '新城区', label: '新城区' },
          { id: '雁塔区', label: '雁塔区' },
          { id: '未央区', label: '未央区' },
          { id: '长安区', label: '长安区' },
          { id: '灞桥区', label: '灞桥区' },
          { id: '鄠邑区', label: '鄠邑区' },
          { id: '临潼区', label: '临潼区' },
          { id: '高陵区', label: '高陵区' },
          { id: '周至县', label: '周至县' },
          { id: '阎良区', label: '阎良区' },
          { id: '蓝田县', label: '蓝田县' }]
      }
    },
    select_business_circle(val) {
      this.axios
        .get('http://127.0.0.1:8000/app/select_business_circle/', {
          params: {
            // 每页显示的条数
            city: this.city,
            business_circle: JSON.stringify(val)
          }
        })
        .then(res => {
          // this.business_districts = res.data.data
          this.business_districts = res.data.data
        })
        .catch(function(error) {
          this.loading = false
        })
    },
    blur_business_circle(data) {
      this.addUser()
      this.axios
        .get('http://127.0.0.1:8000/app/shop_business_district_select/', {
          params: {
            shop_category_create: JSON.stringify(this.region)
          }})
        .then(res => {
          this.business_districts = res.data.data
        })
        .catch(function(error) {
          this.loading = false
        })
        this.$forceUpdate();
    },
    select_city(username) {
      this.axios
        .get('http://127.0.0.1:8000/app/select_city/', {
          params: {
            // 每页显示的条数
            username: global.state['first_name']
          }
        })
        .then(res => {
          this.city = res.data.data
        })
        .catch(function(error) {
          this.loading = false
        })
    },
    shop_business_district_select(data) {
      this.axios
        .get('http://127.0.0.1:8000/app/shop_business_district_select_create/', {
          params: {
            shop_category_create: data.label
          }})
        .then(res => {
          this.shop_category_create = res.data.data
        })
        .catch(function(error) {
          this.loading = false
        })
    },
    shop_city_select(data) {
      this.create.shop_business_district = ''
      if (data.label === '北京市') {
        this.select_regions = [{ id: '西城区', label: '西城区' },
          { id: '海淀区', label: '海淀区' },
          { id: '东城区', label: '东城区' },
          { id: '石景山区', label: '石景山区' },
          { id: '朝阳区', label: '朝阳区' },
          { id: '丰台区', label: '丰台区' },
          { id: '顺义区', label: '顺义区' },
          { id: '房山区', label: '房山区' },
          { id: '大兴区', label: '大兴区' },
          { id: '昌平区', label: '昌平区' },
          { id: '通州区', label: '通州区' },
          { id: '怀柔区', label: '怀柔区' },
          { id: '密云区', label: '密云区' },
          { id: '平谷区', label: '平谷区' },
          { id: '门头沟区', label: '门头沟区' },
          { id: '延庆区', label: '延庆区' }]
      } else if (data.label === '上海市') {
        this.select_regions = [{ id: '静安区', label: '静安区' },
          { id: '长宁区', label: '长宁区' },
          { id: '徐汇区', label: '徐汇区' },
          { id: '杨浦区', label: '杨浦区' },
          { id: '黄浦区', label: '黄浦区' },
          { id: '虹口区', label: '虹口区' },
          { id: '普陀区', label: '普陀区' },
          { id: '闵行区', label: '闵行区' },
          { id: '宝山区', label: '宝山区' },
          { id: '浦东新区', label: '浦东新区' },
          { id: '松江区', label: '松江区' },
          { id: '嘉定区', label: '嘉定区' },
          { id: '青浦区', label: '青浦区' },
          { id: '金山区', label: '金山区' },
          { id: '奉贤区', label: '奉贤区' },
          { id: '崇明区', label: '崇明区' }]
      } else if (data.label === '广州市') {
        this.select_regions = [{ id: '越秀区', label: '越秀区' },
          { id: '荔湾区', label: '荔湾区' },
          { id: '天河区', label: '天河区' },
          { id: '海珠区', label: '海珠区' },
          { id: '黄埔区', label: '黄埔区' },
          { id: '番禺区', label: '番禺区' },
          { id: '白云区', label: '白云区' },
          { id: '增城区', label: '增城区' },
          { id: '花都区', label: '花都区' },
          { id: '从化区', label: '从化区' },
          { id: '南沙区', label: '南沙区' }]
      } else if (data.label === '深圳市') {
        this.select_regions = [{ id: '福田区', label: '福田区' },
          { id: '南山区', label: '南山区' },
          { id: '罗湖区', label: '罗湖区' },
          { id: '盐田区', label: '盐田区' },
          { id: '龙华区', label: '龙华区' },
          { id: '龙岗区', label: '龙岗区' },
          { id: '宝安区', label: '宝安区' },
          { id: '坪山区', label: '坪山区' },
          { id: '光明区', label: '光明区' }]
      } else if (data.label === '天津市') {
        this.select_regions = [{ id: '和平区', label: '和平区' },
          { id: '南开区', label: '南开区' },
          { id: '河西区', label: '河西区' },
          { id: '河北区', label: '河北区' },
          { id: '红桥区', label: '红桥区' },
          { id: '河东区', label: '河东区' },
          { id: '西青区', label: '西青区' },
          { id: '东丽区', label: '东丽区' },
          { id: '滨海新区', label: '滨海新区' },
          { id: '津南区', label: '津南区' },
          { id: '北辰区', label: '北辰区' },
          { id: '武清区', label: '武清区' },
          { id: '静海区', label: '静海区' },
          { id: '蓟州区', label: '蓟州区' },
          { id: '宝坻区', label: '宝坻区' },
          { id: '宁河区', label: '宁河区' }]
      } else if (data.label === '杭州市') {
        this.select_regions = [{ id: '上城区', label: '上城区' },
          { id: '西湖区', label: '西湖区' },
          { id: '拱墅区', label: '拱墅区' },
          { id: '滨江区', label: '滨江区' },
          { id: '下城区', label: '下城区' },
          { id: '江干区', label: '江干区' },
          { id: '萧山区', label: '萧山区' },
          { id: '余杭区', label: '余杭区' },
          { id: '富阳区', label: '富阳区' },
          { id: '临安', label: '临安' },
          { id: '建德市', label: '建德市' },
          { id: '桐庐县', label: '桐庐县' },
          { id: '淳安县', label: '淳安县' }]
      } else if (data.label === '南京市') {
        this.select_regions = [{ id: '秦淮区', label: '秦淮区' },
          { id: '鼓楼区', label: '鼓楼区' },
          { id: '玄武区', label: '玄武区' },
          { id: '建邺区', label: '建邺区' },
          { id: '雨花台区', label: '雨花台区' },
          { id: '栖霞区', label: '栖霞区' },
          { id: '江宁区', label: '江宁区' },
          { id: '浦口区', label: '浦口区' },
          { id: '六合区', label: '六合区' },
          { id: '溧水区', label: '溧水区' },
          { id: '高淳区', label: '高淳区' }]
      } else if (data.label === '苏州市') {
        this.select_regions = [{ id: '姑苏区', label: '姑苏区' },
          { id: '虎丘区', label: '虎丘区' },
          { id: '工业园区', label: '工业园区' },
          { id: '吴中区', label: '吴中区' },
          { id: '相城区', label: '相城区' },
          { id: '昆山', label: '昆山' },
          { id: '常熟', label: '常熟' },
          { id: '吴江', label: '吴江' },
          { id: '张家港', label: '张家港' },
          { id: '太仓', label: '太仓' },
          { id: '甪直', label: '甪直' }]
      } else if (data.label === '成都市') {
        this.select_regions = [{ id: '都江堰市', label: '都江堰市' },
          { id: '彭州市', label: '彭州市' },
          { id: '锦江区', label: '锦江区' },
          { id: '青羊区', label: '青羊区' },
          { id: '武侯区', label: '武侯区' },
          { id: '成华区', label: '成华区' },
          { id: '金牛区', label: '金牛区' },
          { id: '龙泉驿区', label: '龙泉驿区' },
          { id: '双流区', label: '双流区' },
          { id: '郫都区', label: '郫都区' },
          { id: '新都区', label: '新都区' },
          { id: '温江区', label: '温江区' },
          { id: '崇州市', label: '崇州市' },
          { id: '金堂县', label: '金堂县' },
          { id: '青白江区', label: '青白江区' },
          { id: '邛崃市', label: '邛崃市' },
          { id: '简阳市', label: '简阳市' },
          { id: '大邑县', label: '大邑县' },
          { id: '新津县', label: '新津县' },
          { id: '蒲江县', label: '蒲江县' }]
      } else if (data.label === '武汉市') {
        this.select_regions = [{ id: '江汉区', label: '江汉区' },
          { id: '江岸区', label: '江岸区' },
          { id: '武昌区', label: '武昌区' },
          { id: '汉阳区', label: '汉阳区' },
          { id: '硚口区', label: '硚口区' },
          { id: '青山区', label: '青山区' },
          { id: '洪山区', label: '洪山区' },
          { id: '江夏区', label: '江夏区' },
          { id: '蔡甸区', label: '蔡甸区' },
          { id: '东西湖区', label: '东西湖区' },
          { id: '黄陂区', label: '黄陂区' },
          { id: '新洲区', label: '新洲区' },
          { id: '汉南区', label: '汉南区' }]
      } else if (data.label === '重庆市') {
        this.select_regions = [{ id: '渝中区', label: '渝中区' },
          { id: '江北区', label: '江北区' },
          { id: '南岸区', label: '南岸区' },
          { id: '渝北区', label: '渝北区' },
          { id: '沙坪坝区', label: '沙坪坝区' },
          { id: '九龙坡区', label: '九龙坡区' },
          { id: '北碚区', label: '北碚区' },
          { id: '大渡口区', label: '大渡口区' },
          { id: '巴南区', label: '巴南区' },
          { id: '万州区', label: '万州区' },
          { id: '合川区', label: '合川区' },
          { id: '永川区', label: '永川区' },
          { id: '江津区', label: '江津区' },
          { id: '涪陵区', label: '涪陵区' },
          { id: '开州区', label: '开州区' },
          { id: '长寿区', label: '长寿区' },
          { id: '大足区', label: '大足区' },
          { id: '綦江区', label: '綦江区' },
          { id: '璧山区', label: '璧山区' },
          { id: '云阳县', label: '云阳县' },
          { id: '荣昌区', label: '荣昌区' },
          { id: '铜梁区', label: '铜梁区' },
          { id: '奉节县', label: '奉节县' },
          { id: '南川区', label: '南川区' },
          { id: '潼南区', label: '潼南区' },
          { id: '垫江县', label: '垫江县' },
          { id: '黔江区', label: '黔江区' },
          { id: '巫山县', label: '巫山县' },
          { id: '丰都县', label: '丰都县' },
          { id: '巫溪县', label: '巫溪县' },
          { id: '梁平区', label: '梁平区' },
          { id: '酉阳土家族苗族自治县', label: '酉阳土家族苗族自治县' },
          { id: '忠县', label: '忠县' },
          { id: '秀山土家族苗族自治县', label: '秀山土家族苗族自治县' },
          { id: '石柱土家族自治县', label: '石柱土家族自治县' },
          { id: '彭水苗族土家族自治县', label: '彭水苗族土家族自治县' },
          { id: '武隆区', label: '武隆区' },
          { id: '城口县', label: '城口县' }]
      } else if (data.label === '西安市') {
        this.select_regions = [{ id: '碑林区', label: '碑林区' },
          { id: '高新区', label: '高新区' },
          { id: '莲湖区', label: '莲湖区' },
          { id: '新城区', label: '新城区' },
          { id: '雁塔区', label: '雁塔区' },
          { id: '未央区', label: '未央区' },
          { id: '长安区', label: '长安区' },
          { id: '灞桥区', label: '灞桥区' },
          { id: '鄠邑区', label: '鄠邑区' },
          { id: '临潼区', label: '临潼区' },
          { id: '高陵区', label: '高陵区' },
          { id: '周至县', label: '周至县' },
          { id: '阎良区', label: '阎良区' },
          { id: '蓝田县', label: '蓝田县' }]
      }
    },
    shop_category(data) {
      this.create.shop_category = data.label
    },
    jump_xindian() {
      this.axios
        .get('http://127.0.0.1:8000/app/get_jump_href/')
        .then(res => {
          if (res.data.dic === '新店') {
            this.type = '新店'
          }
          this.axios
            .get('http://127.0.0.1:8000/app/update_jump_href/')
            .then(res => {
            })
            .catch(function(error) {
              this.loading = false
            })
            // this.tableData = res.data.data
        })
        .catch(function(error) {
          this.loading = false
        })
    },
    handleClose(done) {
      this.drawer = false
      if (this.shop_edit.text_edit === '') {
        this.shop_edit.text_edit = None
      }
      this.edit_shop(
        this.shop_edit.shop_id_edit,
        this.shop_edit.shop_tags_edit,
        this.shop_edit.shop_kp_name_edit,
        this.shop_edit.shop_telephonenumber_edit,
        this.shop_edit.shop_kp_position_edit,
        this.shop_edit.shop_kp_city_edit,
        this.shop_edit.shop_kp_category_edit,
        this.shop_edit.shop_kp_wechat_id_edit,
        this.shop_edit.shop_category_edit,
        this.shop_edit.shop_region_edit,
        this.shop_edit.shop_business_district_edit,
        this.shop_edit.shop_address_edit,
        this.shop_edit.user_edit,
        this.shop_edit.text_edit,
        this.shop_edit.shop_effect_edit,
        this.shop_edit.shop_service_edit,
        this.shop_edit.shop_surroundings_edit
      )
    },
    // 查找商户数据
    addUser() {
      this.axios
        .get('http://127.0.0.1:8000/app/table_simple_data/', {
          params: {
            // 每页显示的条数
            pagesize: this.pagesize,
            // 显示第几页
            currentPage: this.currentPage,
            shop_business_district: JSON.stringify(this.region),
            shop_category: JSON.stringify(this.business_district),
            shop_region: JSON.stringify(this.category),
            shop_type: this.type,
            search: this.listQuery.title,
            order: this.order_by,
            city: this.city
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
    append_table(formName) {
      this.axios
        .get('http://127.0.0.1:8000/app/append_table/', {
          params: {
            url: this.create.url2,
          }
        })
        .then(res => {
          if (res.data.state === 1) {
            this.$notify({
              title: '添加成功',
              message: '',
              type: 'success'
            })
            this.addUser()
            this.dialogFormVisible_append = false
            this.this.create.url2 = ''
            this.$rules[formName].resetFields()
          
          } else if (res.data.state === 2) {
            this.$notify({
              title: '已存在公海',
              message: '',
              type: 'error'
            })
            this.dialogFormVisible_append = false
            this.$rules[formName].resetFields()
          } else if (res.data.state === 3) {
            this.$notify({
              title: '已存在私海',
              message: '',
              type: 'error'
            })
            this.dialogFormVisible_append = false
            this.$rules[formName].resetFields()
          } else if (res.data.state === 4) {
              this.$notify({
                title: '添加失败',
                message: '请手动添加',
                type: 'error'
              })
              this.dialogFormVisible_append = false
              this.$rules[formName].resetFields()
          }
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    create_table(formName) {
      console.log(formName)
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.axios
            .get('http://127.0.0.1:8000/app/create_table/', {
              params: {
                shop_id: this.create.shop_id,
                shop_name: this.create.shop_name,
                shop_start: this.create.shop_start,
                shop_review_count: this.create.shop_review_count,
                shop_per_capita_consumption: this.create
                  .shop_per_capita_consumption,
                shop_effect: this.create.shop_effect,
                shop_service: this.create.shop_service,
                shop_surroundings: this.create.shop_surroundings,
                shop_address: this.create.shop_address,
                shop_telephonenumber: this.create.shop_telephonenumber,
                shop_business_district: this.create.shop_business_district.label,
                shop_category: this.create.shop_category,
                shop_region: this.create.shop_region,
                shop_city: this.city
              }
            })
            .then(res => {
              if (res.data.state === 1) {
                this.$notify({
                  title: '添加成功',
                  message: '',
                  type: 'success'
                })
                this.addUser()
                this.dialogFormVisible = false
                this.$refs[formName].resetFields()
              } else if (res.data.state === 2) {
                this.$notify({
                  title: '已存在公海',
                  message: '',
                  type: 'error'
                })
                this.dialogFormVisible = false
                this.$refs[formName].resetFields()
              } else if (res.data.state === 3) {
                this.$notify({
                  title: '已存在私海',
                  message: '',
                  type: 'error'
                })
                this.dialogFormVisible = false
                this.$refs[formName].resetFields()
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
    },
    edit_shop(
      shop_id,
      shop_tags,
      shop_kp_name,
      shop_telephonenumber,
      shop_kp_position,
      shop_kp_city,
      shop_kp_category,
      shop_kp_wechat_id,
      shop_category,
      shop_region,
      shop_business_district,
      shop_address,
      user_edit,
      text_edit,
      shop_effect,
      shop_service,
      shop_surroundings
    ) {
      this.axios
        .get('http://127.0.0.1:8000/app/table_simple_data_edit/', {
          params: {
            shop_id: shop_id,
            shop_tags: shop_tags,
            shop_kp_name: shop_kp_name,
            shop_telephonenumber: shop_telephonenumber,
            shop_kp_position: shop_kp_position,
            shop_kp_city: shop_kp_city,
            shop_kp_category: shop_kp_category,
            shop_kp_wechat_id: shop_kp_wechat_id,
            shop_region: shop_region,
            shop_business_district: shop_business_district,
            shop_category: shop_category,
            shop_address: shop_address,
            user_name: user_edit,
            shop_edit: text_edit,
            shop_effect: shop_effect,
            shop_service: shop_service,
            shop_surroundings: shop_surroundings
          }
        })
        .then(res => {
          this.$notify({
            title: '操作成功',
            message: '',
            type: 'success'
          })
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    pull_get(row) {
      // console.log('用户名',global.state["first_name"]);
      this.axios
        .get('http://127.0.0.1:8000/app/get_shop_edit_pull/', {
          params: {
            // 每页显示的条数
            shop_id: row.shop_id,
          }
        })
        .then(res => {
          console.log(res)
          console.log(res.data.data)
          this.axios
          .get('http://127.0.0.1:8000/app/pull_add/', {
            params: {
              // 每页显示的条数
              username: global.state['first_name'],
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
              shop_edit: res.data.data,
              shop_tags: row.shop_tags,
              shop_kp_name: row.shop_kp_name,
              shop_kp_wechat_id: row.shop_kp_wechat_id,
              shop_kp_city: row.shop_kp_city,
              shop_kp_category: row.shop_kp_category,
              shop_kp_position: row.shop_kp_position,
              shop_add_form: JSON.stringify(row.shop_add_form),
              shop_city: row.shop_city
            }
          })
          .then(res => {
            this.edit_pull = null
            if (res.data.state === 3) {
              this.$notify({
                title: '私海商户数量达到允许最大值',
                message: '',
                type: 'error'
              })
            } else if (res.data.state === 4) {
              this.$notify({
                title: '不能拉入新签或续约商户',
                message: '',
                type: 'error'
              })
            } else if (res.data.state === 5) {
              this.$notify({
                title: '商户已存在私海',
                message: '',
                type: 'error'
              })
            } else {
              this.$notify({
                title: '拉入成功',
                message: '',
                type: 'success'
              })
              this.addUser()
            }
          })
          .catch(function(error) {
            this.loading = false
            console.log(error)
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
    get_shop_add_form(shop_id) {
      this.shop_add_form = ''
      this.axios
        .get('http://127.0.0.1:8000/app/table_simple_get_form/', {
          params: {
            // 每页显示的条数
            shop_id: shop_id,
            leixing: '公海'
          }
        })
        .then(res => {
          this.shop_add_form = ''
          this.shop_add_form = res.data.data
          console.log('编辑信息', this.shop_add_form)
          for (var i = 0, len = this.this.shop_add_form.length; i < len; i++) {
            this.shop_edit[i] = undefined
          }
          console.log(this.shop_edit)
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    // 查找商圈,根据选择的城区
    shangquan(region) {
      this.axios
        .get('http://127.0.0.1:8000/app/search_business_circle/', {
          params: {
            // 每页显示的条数
            region: region
          }
        })
        .then(res => {
          this.business_districts = res.data.data
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    shangquan_search_business_circle(region) {
      console.log('选择', region)
      this.axios
        .get('http://127.0.0.1:8000/app/search_business_circle/', {
          params: {
            // 每页显示的条数
            region: region
          }
        })
        .then(res => {
          this.shop_category_create = res.data.data
          console.log('确定', this.shop_category_create)
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    // 根据城区查找数据
    regions_data(data) {
      this.region = data.label
      if (this.business_district !== '商圈') {
        this.business_district = '商圈'
      }
      console.log(data.label)
      this.shangquan(data.label)
      this.addUser(
        this.pagesize,
        this.currentPage,
        data.label,
        this.business_district,
        this.category,
        this.type,
        this.listQuery.title
      )
    },
    edit_shop_add_form(index, value) {
      console.log('失去焦点', this.shop_edit.shop_id_edit, index, value)
      this.axios
        .get('http://127.0.0.1:8000/app/edit_shop_add_form_data/', {
          params: {
            // 每页显示的条数
            shop_id: this.shop_edit.shop_id_edit,
            index: index,
            value: value
          }
        })
        .then(res => {
        })
        .catch(function(error) {
          this.loading = false
        })
    },
    sortChange(column, prop, order) {
      this.order_by = column.order
      this.addUser()
    },
    // 根据商圈查找数据
    business_district_data(data) {
      // 如果上面:value赋的是对象，则可以将返回的对象赋予其他变量，这里的data是选中的对象，那么data.label则是reasonTypes中的label值，如果下拉中选中美国，那么this.selectVal 值为“美国”
      this.business_district = data.label
      // this.shangquan(this.region)
      this.addUser(
        this.pagesize,
        this.currentPage,
        this.region,
        data.label,
        this.category,
        this.type,
        this.listQuery.title
      )
      // this.qryTableDate()
    },
    // 根据品类查找数据
    category_data(data) {
      this.category = data.label
      this.addUser(
        this.pagesize,
        this.currentPage,
        this.region,
        this.business_district,
        data.label,
        this.type,
        this.listQuery.title
      )
    },
    // 修改城区数据
    business_district_edit(data) {
      this.shop_edit.shop_business_district_edit = data.label
      this.shangquan(data.label)
    },
    // 修改商圈数据
    category_edit(data) {
      this.shangquan(this.shop_edit.shop_business_district_edit)
      this.shop_edit.shop_category_edit = data.label
    },
    // 修改品类数据
    regions_data_edit(data) {
      this.shop_edit.shop_region_edit = data.label
    },
    regions_data_edit_create(data) {
      this.create.shop_region = data.label
    },
    // 修改客户类别数据
    kp_category_edit(data) {
      this.shop_edit.shop_kp_category_edit = data.label
    },
    // 修改客户所在城市数据
    kp_city_edit(data) {
      this.shop_edit.shop_kp_city_edit = data.label
    },
    // 修改客户类别数据
    kp_position_edit(data) {
      this.shop_edit.shop_kp_position_edit = data.label
    },
    // 根据类型查找数据
    type_data(data) {
      this.type = data.label
      this.addUser()
    },
    // 查询框
    select_input(e) {
      this.listQuery.title = e
      this.addUser(
        this.pagesize,
        this.currentPage,
        this.region,
        this.business_district,
        this.category,
        this.type,
        e
      )
    },
    // 表格单击事件(弹出抽屉修改)
    data_update(row, event, column) {
      this.shop_edit.text_edit = ''
      this.drawer = true
      this.shop_edit.shop_table_row = row
      this.shop_edit.shop_id_edit = row.shop_id
      this.shop_edit.shop_name_edit = row.shop_name
      this.shop_edit.shop_city_edit = row.shop_city
      if (row.shop_tags === '新签') {
        this.shop_edit.shop_tags_edit = 1
      } else if (row.shop_tags === '断约') {
        this.shop_edit.shop_tags_edit = 2
      } else if (row.shop_tags === '续约') {
        this.shop_edit.shop_tags_edit = 3
      } else if (row.shop_tags === '新店') {
        this.shop_edit.shop_tags_edit = 4
      } else {
        this.shop_edit.shop_tags_edit = 0
      }
      this.get_shop_edit(row.shop_id)
      this.get_shop_add_form(row.shop_id)
      this.shop_edit.shop_kp_name_edit = row.shop_kp_name
      this.shop_edit.shop_telephonenumber_edit = row.shop_telephonenumber
      this.shop_edit.shop_kp_position_edit = row.shop_kp_position
      this.shop_edit.shop_kp_city_edit = row.shop_kp_city
      this.shop_edit.shop_kp_category_edit = row.shop_kp_category
      this.shop_edit.shop_business_district_edit = row.shop_business_district
      this.shop_edit.shop_category_edit = row.shop_category
      this.shop_edit.shop_region_edit = row.shop_region
      this.shop_edit.shop_kp_wechat_id_edit = row.shop_kp_wechat_id
      this.shop_edit.shop_address_edit = row.shop_address
      this.shop_edit.user_edit = global.state['first_name']
      this.shop_edit.shop_add_form_edit = row.shop_add_form
      this.shop_edit.shop_effect_edit = row.shop_effect
      this.shop_edit.shop_service_edit = row.shop_service
      this.shop_edit.shop_surroundings_edit = row.shop_surroundings
    },
    current_change: function(currentPage) {
      this.currentPage = currentPage
    },
    // 跳转到大众点评商户页面
    jump_href(href, row) {
      console.log(row)
      window.open('https://www.dianping.com/shop/' + row.shop_id)
    },
    // 分页
    // 每页显示的条数
    handleSizeChange(val) {
      // 改变每页显示的条数
      this.pagesize = val
      this.loading = true

      // 点击每页显示的条数时，显示第一页
      this.addUser()
      this.qryTableDate()
      // 注意：在改变每页显示的条数时，要将页码显示到第一页
    },
    // 显示第几页
    handleCurrentChange(val) {
      console.log('第几页', val)
      this.loading = true
      // 改变默认的页数
      this.currentPage = val
      // 切换页码时，要获取每页显示的条数
      this.addUser()
      this.qryTableDate()
    }
  },
  computed: {
    region: {
      get () {
        return this.$data._selected
      },
    }
  },
}

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
