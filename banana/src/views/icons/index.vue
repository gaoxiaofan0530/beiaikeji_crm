
<template>
  <div>
    <el-drawer
      class="drawer_body"
      title="任务信息"
      :visible.sync="drawer"
      :direction="direction"
      :before-close="handleClose"
      size="100"
    >
      <div class="demo-drawer__content">
        <span v-if="suatus_name === '已完成'">
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
            <el-form-item label="状态" :label-width="formLabelWidth">
              <el-tag type="success" effect="dark">{{ pending_review.suatus }}</el-tag>
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
            <el-form-item label="完成时间" :label-width="formLabelWidth">
              <el-input
                v-model="pending_review.success_time"
                style="width:80%"
                placeholder="请选择活动区域"
                :disabled="true"
              />
            </el-form-item>
            <el-form-item label="审核人" :label-width="formLabelWidth">
              <el-input
                v-model="pending_review.submitter"
                style="width:80%"
                placeholder="请选择活动区域"
                :disabled="true"
              />
            </el-form-item>
            <el-form-item label="销售" :label-width="formLabelWidth">
              <el-input
                v-model="pending_review.username"
                style="width:80%"
                placeholder="请选择活动区域"
                :disabled="true"
              />
            </el-form-item>
            <el-divider>任务截图</el-divider>
              <img width="50%" height="50%" :src="pending_review.url" alt="">
            <el-form-item label="进度" :label-width="formLabelWidth">
              <el-progress
                :text-inside="true"
                :stroke-width="26"
                :percentage="pending_review.schedule"
              />
            </el-form-item>
          </el-form>
        </span>
        <span v-else-if="suatus_name === '未完成'">
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
            <el-form-item label="状态" :label-width="formLabelWidth">
              <el-tag type="danger" effect="dark">{{ pending_review.suatus }}</el-tag>
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
            <el-form-item label="销售" :label-width="formLabelWidth">
              <el-input
                v-model="pending_review.username"
                style="width:80%"
                placeholder="请选择活动区域"
                :disabled="true"
              />
            </el-form-item>
            <el-form-item label="进度" :label-width="formLabelWidth">
              <el-progress
                :text-inside="true"
                :stroke-width="26"
                :percentage="pending_review.schedule"
              />
            </el-form-item>
          </el-form>
        </span>
        <span v-else>
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
            <el-form-item label="状态" :label-width="formLabelWidth">
              <el-tag type="warning" effect="dark">{{ pending_review.suatus }}</el-tag>
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
            <el-form-item label="审核人" :label-width="formLabelWidth">
              <el-input
                v-model="pending_review.submitter"
                style="width:80%"
                placeholder="请选择活动区域"
                :disabled="true"
              />
            </el-form-item>
            <el-form-item label="销售" :label-width="formLabelWidth">
              <el-input
                v-model="pending_review.username"
                style="width:80%"
                placeholder="请选择活动区域"
                :disabled="true"
              />
            </el-form-item>
            <el-form-item label="进度" :label-width="formLabelWidth">
              <el-progress
                :text-inside="true"
                :stroke-width="26"
                :percentage="pending_review.schedule"
              />
            </el-form-item>
          </el-form>
        </span>
      </div>
    </el-drawer>
    <div class="filter-container" style="margin-left:15px;margin-top:25px;">
      <el-select
        v-model="type"
        ref="chooseKpi3"
        filterable
        style="width:130px;"
        value-key="id"
        placeholder="类型"
        @blur="city_select3"
        @change="suatus"
      >
        <el-option v-for="item in types" :key="item.id" :label="item.label" :value="item" />
      </el-select>
      <span v-if="roles === 'admin' || roles === 'super_admin'">
        <el-select
          ref="chooseKpi4"
          v-model="xiaoshou_value"
          clearable
          filterable
          placeholder="请选择"
          @blur="city_select"
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
      <el-table-column label="订单编号" show-overflow-tooltip prop="order_id" width="300" />
      <el-table-column prop="shop_name" label="商户" width="450" show-overflow-tooltip>
        <template slot-scope="{row}">
          <div v-if="row.suatus === '已完成'">
            <span
              class="link-type"
              style="color:#606266"
              @click="data_update(row);drawer = true"
            >{{ row.shop_name }}</span>
            <el-tag type="success" effect="dark">{{ row.suatus }}</el-tag>
          </div>
          <div v-else-if="row.suatus === '未完成'">
            <span
              class="link-type"
              style="color:#606266"
              @click="data_update(row);drawer = true"
            >{{ row.shop_name }}</span>
            <el-tag type="danger" effect="dark">{{ row.suatus }}</el-tag>
          </div>
          <div v-else-if="row.suatus === '待审核'">
            <span
              class="link-type"
              style="color:#606266"
              @click="data_update(row);drawer = true"
            >{{ row.shop_name }}</span>
            <el-tag type="warning" effect="dark">{{ row.suatus }}</el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="服务项目" show-overflow-tooltip prop="project" />
      <el-table-column prop="time" label="截止时间" show-overflow-tooltip />
      <el-table-column prop="money" show-overflow-tooltip label="服务奖金" />
      <el-table-column prop="username" show-overflow-tooltip label="实施人" />
      <el-table-column label="操作" width="210" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <div v-if="roles === 'admin' || roles === 'super_admin'">
            <el-tooltip class="item" effect="dark" content="转移" placement="top-start">
              <el-button
                size="mini"
                type="primary"
                content="转移"
                placement="top"
                @click.stop="transfer_order(scope.row)"
              >
                <i class="el-icon-refresh" />
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
          <el-select v-model="form.xiaoshou_value_transfer" clearable filterable placeholder="请选择要转给谁">
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
  name: 'DataList',
  data() {
    return {
      business_districts: '',
      roles: '',
      now_admin: '',
      form: {
        xiaoshou_value_transfer: ''
      },
      row: '',
      dialogFormVisible: false,
      types: [
        {
          id: '已完成',
          label: '已完成'
        },
        {
          id: '未完成',
          label: '未完成'
        },
        {
          id: '待审核',
          label: '待审核'
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
      shop_add_form: [],
      shop_add_form_edit: '',
      pending_review: {
        project: '',
        shop_name: '',
        time: '',
        money: '',
        schedule: '',
        username: '',
        submitter: '',
        submit_time: '',
        username: '',
        suatus: '',
        order_id: '',
        url:''
      },
      type: '已完成',
      region: '全部',
      suatus_name: '已完成',
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
      name:'',
      roles: '',
      formLabelWidth: '80px',
      timer: null,
      editData: {},
      remoteFuncs: {},
      dynamicData: {},
      xiaoshou_value: '',
      data:'',
      xiaoshou_options: [],
      rules: {
        xiaoshou_value_transfer: [
          { required: true, message: '请选择要转移到的销售', trigger: 'blur' }
        ]
      }
    }
  },
  created: function() {
    this.roles = global.state['avatar']
    if (global.state['avatar'] === 'admin' || global.state['avatar'] === 'super_admin') {
      this.get_xiaoshou_data()
      this.name = global.state['avatar']
    } else {
      this.xiaoshou_value = global.state['first_name']
    }
    this.addUser(
      this.pagesize,
      this.currentPage,
      this.suatus_name,
      this.xiaoshou_value
    )
    this.shangquan('全部')
  },
  mounted() {
    this.addUser()
    this.shangquan('全部')
  },

  methods: {
    // 查找商户数据
    city_select() {
      this.$refs.chooseKpi4.blur();
    },
    city_select3() {
      this.$refs.chooseKpi3.blur();
    },
    addUser(n1, n2, n3, n4) {
      console.log('this.data',this.data)
      this.axios
        .get('http://127.0.0.1:8000/app/table_simple_to_do/', {
          params: {
            // 每页显示的条数
            pagesize: n1,
            currentPage: n2,
            suatus: n3,
            username: n4,
            name: global.state['first_name']
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
    // 根据商圈查找数据
    // 表格单击事件(弹出抽屉修改)
    data_update(row, event, column) {
      this.drawer = true
      this.pending_review.project = row.project
      this.pending_review.order_id = row.order_id
      this.pending_review.shop_name = row.shop_name
      this.pending_review.time = row.time
      this.pending_review.money = row.money
      this.pending_review.suatus = row.suatus
      this.pending_review.schedule = row.schedule
      this.pending_review.username = row.username
      this.pending_review.submitter = row.submitter
      this.pending_review.submit_time = row.submit_time
      this.pending_review.edit = row.edit
      this.pending_review.url = row.url
      this.pending_review.submit_time = row.submit_time
      this.pending_review.success_time = row.success_time
      this.getLocation(row.lng, row.lat)
      console.log(row)
    },
    transfer_order(row) {
      console.log(row)
      this.row = row
      this.now_admin = row.username
      this.$confirm('确定要转移任务吗? 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.dialogFormVisible = true
      })
    },
    transfer_update(formName) {
      this.$confirm('确定要转移任务吗? 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.axios
              .get('http://127.0.0.1:8000/app/transfer_update/', {
                params: {
                  order_id: this.row.order_id,
                  username: this.form.xiaoshou_value_transfer,
                  type: this.type,
                  project: this.row.project
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
                  this.addUser(this.pagesize, this.currentPage, this.suatus_name, this.xiaoshou_value)
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
    get_xiaoshou_data() {
      this.axios
        .get('http://127.0.0.1:8000/app/get_xiaoshou_data/', {
            params: {
              username: global.state['first_name']
            }
          })
        .then(body => {
          this.xiaoshou_options = body.data.data
        })
    },
    current_change: function(currentPage) {
      this.currentPage = currentPage
    },
    handleEdit(row) {
      console.log('编辑', row)
      this.axios
        .get('http://127.0.0.1:8000/app/audit_failure/', {
          params: {
            // 每页显示的条数
            project: row.project,
            shop_name: row.shop_name,
            time: row.time,
            money: row.money,
            schedule: row.schedule,
            username: row.username
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
    xiaoshou_change(username) {
      this.addUser(
        this.pagesize,
        this.currentPage,
        this.suatus_name,
        this.xiaoshou_value
      )
    },
    suatus() {
      this.suatus_name = this.type.label
      this.addUser(
        this.pagesize,
        this.currentPage,
        this.suatus_name,
        this.xiaoshou_value
      )
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
        this.suatus_name,
        this.xiaoshou_value
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
      this.addUser(this.pagesize, val, this.suatus_name, this.xiaoshou_value)
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
