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
          <el-form-item label="ID" :label-width="formLabelWidth">
            <el-input
              v-model="shop_edit.id"
              autocomplete="off"
              style="width:80%"
              :disabled="true"
            />
          </el-form-item>
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
          <el-form-item label="拜访日期" :label-width="formLabelWidth">
            <el-input
              v-model="shop_edit.time"
              style="width:80%"
              placeholder="请选择活动区域"
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
              <el-select v-model="domain.value" type="date" :disabled="true" placeholder="选择内容" @change="edit_shop_add_form(index,domain.value)">
                <el-option
                  v-for="item in domain.select"
                  :key="item.label"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </span>
            <span v-if="domain.type === '大文本框'">
              <el-input v-model="domain.value" type="textarea" :disabled="true" @blur="edit_shop_add_form(index,domain.value)" />
            </span>
          </el-form-item>
        </el-form>
      </div>
    </el-drawer>
    <div class="filter-container" style="margin-left:15px;margin-top:25px;">
      <span v-if="roles === 'admin'">
        <el-select v-model="xiaoshou_value" clearable filterable placeholder="请选择" @change="xiaoshou_change(xiaoshou_value)">
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
      <el-table-column prop="id" label="ID" show-overflow-tooltip />
      <el-table-column prop="visit_id" label="商户ID" show-overflow-tooltip />
      <el-table-column prop="visit_shop_name" label="店名" show-overflow-tooltip width="450" />
      <el-table-column prop="visit_time" label="拜访日期" show-overflow-tooltip />
      <el-table-column label="操作" width="210" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <div v-if="roles === 'admin'">
            <el-tooltip class="item" effect="dark" content="删除" placement="top-start">
              <el-button
                size="mini"
                type="danger"
                content="删除"
                placement="top"
                @click.stop="handleDelete(scope.row)"
              >
                <i class="el-icon-delete" />
              </el-button>
            </el-tooltip>
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
  name: 'DataList',
  data() {
    return {
      num: '2019',
      roles: '',
      xiaoshou_value: '',
      xiaoshou_options: [],
      regions: [
        {
          id: '西城区',
          label: '西城区'
        },
        {
          id: '海淀区',
          label: '海淀区'
        },
        {
          id: '东城区',
          label: '东城区'
        },
        {
          id: '石景山区',
          label: '石景山区'
        },
        {
          id: '朝阳区',
          label: '朝阳区'
        },
        {
          id: '丰台区',
          label: '丰台区'
        },
        {
          id: '顺义区',
          label: '顺义区'
        },
        {
          id: '房山区',
          label: '房山区'
        },
        {
          id: '大兴区',
          label: '大兴区'
        },
        {
          id: '昌平区',
          label: '昌平区'
        },
        {
          id: '通州区',
          label: '通州区'
        },
        {
          id: '昌平区',
          label: '昌平区'
        },
        {
          id: '密云区',
          label: '密云区'
        },
        {
          id: '怀柔区',
          label: '怀柔区'
        },
        {
          id: '平谷区',
          label: '平谷区'
        },
        {
          id: '延庆区',
          label: '延庆区'
        },
        {
          id: '门头沟区',
          label: '门头沟区'
        },
        {
          id: '区域',
          label: '区域'
        }
      ],
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
      shop_kp_position: [
        { id: '大老板', label: '大老板' },
        { id: '合伙人', label: '合伙人' },
        { id: '经理', label: '经理' },
        { id: '店长', label: '店长' },
        { id: '前台', label: '前台' },
        { id: '技师', label: '技师' }
      ],
      shop_kp_city: [
        { id: '北京市', label: '北京市' },
        { id: '上海市', label: '上海市' },
        { id: '天津市', label: '天津市' },
        { id: '武汉市', label: '武汉市' },
        { id: '南京市', label: '南京市' },
        { id: '青岛市', label: '青岛市' },
        { id: '成都市', label: '成都市' },
        { id: '厦门市', label: '厦门市' },
        { id: '宁波市', label: '宁波市' },
        { id: '杭州市', label: '杭州市' },
        { id: '西安市', label: '西安市' },
        { id: '武汉市', label: '武汉市' },
        { id: '深圳市', label: '深圳市' }
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
      shop_edit: {
        time: undefined,
        shop_table_row: undefined,
        shop_id_edit: undefined,
        id: undefined,
        shop_name_edit: undefined,
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
        shop_add_form_edit: undefined
      },
      type: '合作状态',
      region: '区域',
      category: '行业',
      business_district: '商圈',
      tableData: [],
      multipleSelection: [],
      total: 0,
      pagesize: 10,
      currentPage: 1,
      loading: true,
      drawer: false,
      direction: 'rtl',
      options: [],
      formLabelWidth: '80px',
      timer: null,
      editData: {},
      remoteFuncs: {},
      dynamicData: {}
    }
  },
  created: function() {
    this.roles = global.state['avatar']
    if (global.state['avatar'] === 'admin') {
      this.get_xiaoshou_data()
    }
    this.addUser(
      this.pagesize,
      this.currentPage,
      this.region,
      this.business_district,
      this.category,
      this.type,
      ''
    )
    this.shangquan('商圈')
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
    this.num = year + seperator1 + month + seperator1 + strDate
  },
  methods: {
    // 查找商户数据
    addUser(n1, n2, region, business_district, category, type, search) {
      if (this.xiaoshou_value === '') {
        this.axios
          .get('http://127.0.0.1:8000/app/table_simple_visit/', {
            params: {
              // 每页显示的条数
              pagesize: n1,
              // 显示第几页
              currentPage: n2,
              username: global.state['first_name']
            }
          })
          .then(res => {
            this.tableData = res.data.data
            this.total = res.data.total
            this.loading = false
            console.log(this.tableData)
          })
          .catch(function(error) {
            this.loading = false
            console.log(error)
          })
      } else {
        this.axios
          .get('http://127.0.0.1:8000/app/table_simple_visit/', {
            params: {
              // 每页显示的条数
              pagesize: n1,
              // 显示第几页
              currentPage: n2,
              username: this.xiaoshou_value
            }
          })
          .then(res => {
            this.tableData = res.data.data
            this.total = res.data.total
            this.loading = false
            console.log(this.tableData)
          })
          .catch(function(error) {
            this.loading = false
            console.log(error)
          })
      }
    },
    xiaoshou_change(item) {
      this.xiaoshou_value = item
      this.addUser(this.pagesize, this.currentPage)
    },
    get_xiaoshou_data() {
      this.axios
        .get('http://127.0.0.1:8000/app/get_xiaoshou_data/')
        .then(body => {
          this.xiaoshou_options = body.data.data
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
      text_edit
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
            shop_edit: text_edit
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
            this.region,
            this.business_district,
            this.category,
            this.type,
            this.listQuery.title
          )
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    pull_get(row) {
      // console.log('用户名',global.state["first_name"]);
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
            shop_edit: row.shop_edit,
            shop_tags: row.shop_tags,
            shop_kp_name: row.shop_kp_name,
            shop_kp_wechat_id: row.shop_kp_wechat_id,
            shop_kp_city: row.shop_kp_city,
            shop_kp_category: row.shop_kp_category,
            shop_kp_position: row.shop_kp_position,
            shop_add_form: row.shop_add_form
          }
        })
        .then(res => {
          if (res.data.state == 3) {
            this.$notify({
              title: '私海商户数量达到允许最大值',
              message: '',
              type: 'error'
            })
          } else {
            this.$notify({
              title: '拉入成功',
              message: '',
              type: 'success'
            })
            this.addUser(
              this.pagesize,
              this.currentPage,
              this.region,
              this.business_district,
              this.category,
              this.type,
              this.listQuery.title
            )
          }
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
            shop_id: shop_id
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
      this.axios
        .get('http://127.0.0.1:8000/app/table_simple_get_form/', {
          params: {
            // 每页显示的条数
            shop_id: shop_id
          }
        })
        .then(res => {
          this.shop_add_form = res.data.data
          this.console.log('编辑信息', this.shop_add_form.length)
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
    // 根据城区查找数据
    regions_data(data) {
      // 如果上面:value赋的是对象，则可以将返回的对象赋予其他变量，这里的data是选中的对象，那么data.label则是reasonTypes中的label值，如果下拉中选中美国，那么this.selectVal 值为“美国”
      console.log('选中值', data.label)
      this.region = data.label
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
      // this.qryTableDate();
    },
    edit_shop_add_form(index, value) {
      console.log('失去焦点', this.shop_edit.id, index, value)
      this.axios
        .get('http://127.0.0.1:8000/app/edit_shop_add_form_data_edit_baifang/', {
          params: {
            // 每页显示的条数
            shop_id: this.shop_edit.shop_id_edit,
            id: this.shop_edit.id,
            index: index,
            value: value
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
    // 根据商圈查找数据
    business_district_data(data) {
      // 如果上面:value赋的是对象，则可以将返回的对象赋予其他变量，这里的data是选中的对象，那么data.label则是reasonTypes中的label值，如果下拉中选中美国，那么this.selectVal 值为“美国”
      this.business_district = data.label
      this.shangquan(this.region)
      this.addUser(
        this.pagesize,
        this.currentPage,
        this.region,
        data.label,
        this.category,
        this.type,
        this.listQuery.title
      )
      this.qryTableDate()
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
      console.log(data)
      this.type = data.label
      this.addUser(
        this.pagesize,
        this.currentPage,
        this.region,
        this.business_district,
        this.category,
        data.label,
        this.listQuery.title
      )
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
      this.drawer = true
      this.shop_edit.shop_table_row = row
      this.shop_edit.shop_id_edit = row.visit_id
      this.shop_edit.id = row.id
      this.shop_edit.shop_name_edit = row.visit_shop_name
      this.shop_edit.time = row.visit_time
      this.shop_add_form = row.visit_data
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
      // 点击每页显示的条数时，显示第一页
      this.addUser(val, this.currentPage)
      this.qryTableDate()
      // 注意：在改变每页显示的条数时，要将页码显示到第一页
    },
    // 显示第几页
    handleCurrentChange(val) {
      console.log('第几页', val)
      // 改变默认的页数
      this.currentPage = val
      // 切换页码时，要获取每页显示的条数
      this.addUser(this.pagesize, val)
      this.qryTableDate()
    },
    handleDelete(row) {
      this.$confirm('确定要删除拜访吗? 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.axios
            .get('http://127.0.0.1:8000/app/delete_visit/', {
              params: {
                // 每页显示的条数
                visit_data: JSON.stringify(row.visit_data),
                id: row.id
              }
            })
            .then(res => {
              if (res.data.state == 1) {
                this.$notify({
                  title: '删除成功',
                  message: '',
                  type: 'success'
                })
              } else {
                this.$notify({
                  title: '删除失败',
                  message: '',
                  type: 'error'
                })
              }
              this.addUser(
                this.pagesize,
                this.currentPage,
                this.region,
                this.business_district,
                this.category,
                this.type,
                ''
              )
            })
            .catch(function(error) {
              this.loading = false
              console.log(error)
            })
        })
        .catch(() => {
          this.$notify({
            title: '已取消删除',
            message: '',
            type: 'info'
          })
        })
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
