<template>
  <div>
    <el-drawer
      class="drawer_body"
      title="待审核信息"
      :visible.sync="drawer"
      :direction="direction"
      :before-close="handleClose"
      size="100"
    >
      <div class="demo-drawer__content">
        <el-form :model="form">
          <el-form-item label="订单编号" :label-width="formLabelWidth">
            <el-input
              v-model="pending_review.order_id"
              autocomplete="off"
              style="width:80%"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="商户名称" :label-width="formLabelWidth">
            <el-input
              v-model="pending_review.shop_name"
              autocomplete="off"
              style="width:80%"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="服务项目" :label-width="formLabelWidth">
            <el-input
              v-model="pending_review.project"
              style="width:80%"
              placeholder="请选择活动区域"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="服务奖金" :label-width="formLabelWidth">
            <el-input
              v-model="pending_review.money"
              style="width:80%"
              placeholder="请选择活动区域"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="截止时间" :label-width="formLabelWidth">
            <el-input
              v-model="pending_review.time"
              style="width:80%"
              placeholder="请选择活动区域"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="提交时间" :label-width="formLabelWidth">
            <el-input
              v-model="pending_review.submit_time"
              style="width:80%"
              placeholder="请选择活动区域"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="提交人" :label-width="formLabelWidth">
            <el-input
              v-model="pending_review.submitter"
              style="width:80%"
              placeholder="请选择活动区域"
              :disabled="true"
            />
          </el-form-item>
          <el-divider>付款截图</el-divider>
            <img width="50%" height="50%" :src="pending_review.url" alt="">
          <el-divider>备注</el-divider>
          <el-form-item label="备注内容" :label-width="formLabelWidth">
            <el-input
              v-model="pending_review.edit"
              style="width:80%"
              placeholder="备注内容"
              type="textarea"
              :disabled="true"
            />
          </el-form-item>
        </el-form>
      </div>
    </el-drawer>
    <!-- <span v-if="roles === 'super_admin'">
      <div class="filter-container" style="margin-left:15px;margin-top:25px;">
        <el-select
          v-model="xiaoshou"
          ref="chooseKpi"
          class="filter-item"
          style="width:130px;"
          value-key="id"
          placeholder="类型"
          filterable 
          @blur="type_select"
          @change="type_data"
        >
          <el-option v-for="item in xiaoshou_data" :key="item.id" :label="item.label" :value="item" />
        </el-select>
      </div>
    </span> -->
    <el-table
      ref="multipleTable"
      v-loading="loading"
      :data="tableData"
      border
      fit
      stripe
      highlight-current-row
      style="width: 100%;margin-left:15px;margin-right:30px;margin-top:15px;"
      @row-click="data_update"
    >
      <el-table-column prop="order_id" label="订单编号" show-overflow-tooltip />
      <el-table-column prop="shop_name" label="商户" show-overflow-tooltip />
      <el-table-column label="服务项目" show-overflow-tooltip prop="project" />
      <el-table-column prop="time" label="截止时间" show-overflow-tooltip />
      <el-table-column prop="money" show-overflow-tooltip label="服务奖金" />
      <el-table-column prop="username" show-overflow-tooltip label="销售" />
      <el-table-column prop="submit_time" show-overflow-tooltip label="提交时间" />
      <el-table-column label="操作" width="210" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click.stop="jump_href(scope.$index, scope.row);">
            <i class="el-icon-check" />
          </el-button>
          <el-button size="mini" type="danger" @click.stop="chazhao(scope.row)">
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
    <el-dialog title="驳回备注" :visible.sync="dialogTableVisible">
      <el-form :model="form">
        <el-form-item
        label="驳回备注"
        :label-width="formLabelWidth"
        :rules="[
          { required: true, message: '不能为空'},
        ]"
        >
          <el-input v-model="edit" autocomplete="off"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogTableVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogTableVisible = false;handleEdit();">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import request from '@/utils/request'
import global from '@/store/modules/user'

export default {
  name: 'DataList',
  data() {
    return {
      dialogTableVisible:false,
      row:'',
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
          id: '全部',
          label: '全部'
        }
      ],
      edit:'',
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
          id: '全部',
          label: '全部'
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
      shop_add_form: [],
      shop_add_form_edit: '',
      shop_edit: {
        shop_table_row: undefined,
        shop_id_edit: undefined,
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
      pending_review: {
        project: '',
        shop_name: '',
        time: '',
        money: '',
        schedule: '',
        username: '',
        submitter: '',
        submit_time: '',
        success_time: '',
        order_id:'',
        edit: '',
        url:''
      },
      type: '全部',
      region: '全部',
      category: '全部',
      business_district: '全部',
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
      dynamicData: {},
      lng: '',
      lat: '',
      roles: '',
      xiaoshou:'全部',
      xiaoshou_name:'全部',
      xiaoshou_data:null,
    }
  },
  created: function() {
    this.roles = global.state['avatar']
    this.addUser(
      this.pagesize,
      this.currentPage,
      '全部',
      '全部',
      '全部',
      '全部',
      ''
    )
    this.selelct_xiaoshou()
    if (global.state["avatar"] === "admin" || global.state["avatar"] === "super_admin") {
        console.log()
    }else{
      this.$router.push({path: '/dashboard'});
      this.$message.error('暂无权限访问');
    }
    this.shangquan('全部')
  },
  mounted() {
    this.addUser()
    this.shangquan('全部')
  },

  methods: {
    type_select(){
      this.$refs.chooseKpi.blur()
    },
    type_data(){
      this.xiaoshou_name = this.xiaoshou.id
      this.addUser(this.pagesize,this.currentPage)
    },
    handleClose(done) {
      this.drawer = false
      if (this.shop_edit.text_edit == '') {
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
        this.shop_edit.text_edit
      )
    },
    chazhao(row){
        this.row = row
        this.dialogTableVisible = true;
    },
    selelct_xiaoshou(){
      this.axios
        .get('http://127.0.0.1:8000/app/selelct_xiaoshou/', {
          params: {
            username: global.state['first_name'],
          }
        })
        .then(res => {
          this.xiaoshou_data = res.data.data
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    // 查找商户数据
    addUser(n1, n2) {
      this.axios
        .get('http://127.0.0.1:8000/app/table_simple_pending_review/', {
          params: {
            // 每页显示的条数
            pagesize: n1,
            // 显示第几页
            currentPage: n2,
            username: global.state['first_name'],
            name: this.listQuery.title,
            xiaoshou:this.xiaoshou_name
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
    // shangquan(region) {
    //   this.axios
    //     .get('http://127.0.0.1:8000/app/search_business_circle/', {
    //       params: {
    //         // 每页显示的条数
    //         region: region
    //       }
    //     })
    //     .then(res => {
    //       this.business_districts = res.data.data
    //     })
    //     .catch(function(error) {
    //       this.loading = false
    //       console.log(error)
    //     })
    // },
    // 根据城区查找数据
    regions_data(data) {
      // 如果上面:value赋的是对象，则可以将返回的对象赋予其他变量，这里的data是选中的对象，那么data.label则是reasonTypes中的label值，如果下拉中选中美国，那么this.selectVal 值为“美国”
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
      this.qryTableDate()
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
        .then(res => {})
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    // 根据商圈查找数据
    // 表格单击事件(弹出抽屉修改)
    data_update(row, event, column) {
      this.drawer = true
      this.pending_review.project = row.project
      this.pending_review.shop_name = row.shop_name
      this.pending_review.time = row.time
      this.pending_review.money = row.money
      this.pending_review.schedule = row.schedule
      this.pending_review.username = row.username
      this.pending_review.submitter = row.submitter
      this.pending_review.submit_time = row.submit_time
      this.pending_review.order_id = row.order_id
      this.pending_review.edit = row.edit
      this.pending_review.url = row.url
      console.log(row)
    },
    select_input() {
      this.addUser(
        this.pagesize,
        this.currentPage
      )
    },
    current_change: function(currentPage) {
      this.currentPage = currentPage
    },
    // 跳转到大众点评商户页面
    jump_href(href, row) {
      if(global.state['avatar'] != 'super_admin' && global.state['avatar'] != 'admin' ){
          this.$notify({
            title: '操作失败',
            message: '联系负责人进行审核',
            type: 'error'
          })
      } else if(row.username == global.state['first_name'] && global.state['avatar'] != 'super_admin'){
        this.$notify({
            title: '操作失败',
            message: '联系负责人进行审核',
            type: 'error'
          })
      }else{
          this.axios
            .get('http://127.0.0.1:8000/app/post_completed/', {
              params: {
                // 每页显示的条数
                project: row.project,
                shop_name: row.shop_name,
                time: row.time,
                money: row.money,
                schedule: row.schedule,
                username: row.username,
                submitter: global.state['first_name'],
                submit_time: row.submit_time,
                success_time: row.success_time,
                order_id:row.order_id,
                edit: row.edit,
                lat: row.lat,
                lng: row.lng
              }
            })
            .then(res => {
              this.addUser(this.pagesize, this.currentPage)
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
      }
    },
    handleEdit(row) {
      this.axios
        .get('http://127.0.0.1:8000/app/audit_failure/', {
          params: {
            // 每页显示的条数
            project: this.row.project,
            shop_name: this.row.shop_name,
            time: this.row.time,
            money: this.row.money,
            schedule: this.row.schedule,
            order_id: this.row.order_id,
            username: this.row.username,
            edit: this.edit
          }
        })
        .then(res => {
          this.addUser(this.pagesize, this.currentPage)
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
    // 分页
    // 每页显示的条数
    handleSizeChange(val) {
      // 改变每页显示的条数
      this.pagesize = val
      // 点击每页显示的条数时，显示第一页
      this.addUser(
        val,
        this.currentPage,
      )
      this.qryTableDate()
      // 注意：在改变每页显示的条数时，要将页码显示到第一页
    },
    // 显示第几页
    handleCurrentChange(val) {
      console.log('第几页', val)
      // 改变默认的页数
      this.currentPage = val
      // 切换页码时，要获取每页显示的条数
      this.addUser(
        this.pagesize,
        val,
      )
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
.map {
  width: 80%;
  height: 400px;
}
</style>
