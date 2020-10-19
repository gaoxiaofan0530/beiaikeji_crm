<template>
  <div @click="noclick">
    <el-form
      ref="ruleForm"
      :model="ruleForm"
      :rules="rules"
      label-width="100px"
      class="demo-ruleForm"

      style="margin-left:15px;margin-top:30px;margin-right:50px;"
    >
      <el-form-item label="合同编号" prop="contract_id" placeholder="请输入合同编号">
        <el-input v-model="ruleForm.contract_id"/>
      </el-form-item>
      <el-form-item label="下单日期" prop="order_date">
        <el-date-picker v-model="ruleForm.order_date" ref="datePicker" @focus="datePicker_click" type="date" placeholder="请选择下单日期(到账日期)" @change="get_data" />
      </el-form-item>
      <el-form-item label="开始日期" prop="order_start_date">
        <el-date-picker
          ref="datePicker2" 
          @focus="datePicker_click2"
          v-model="ruleForm.order_start_date"
          type="date"
          placeholder="请选择开始日期"
          @change="change_order_date"
        />
      </el-form-item>
      <el-form-item label="签约商户" prop="sign_contract_shop">
        <el-select
          ref="chooseKpi4"
          v-model="ruleForm.sign_contract_shop"
          filterable
          placeholder="请选择签约商户"
          @blur="chooseKpi4"
          @change="get_shop_date"
        >
          <el-option v-for="item in options" :key="item.label" :label="item.label" :value="item.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="签约店数" prop="order_numbers">
        <el-input v-model="ruleForm.order_numbers" placeholder="请输入签约门店数" />
      </el-form-item>
      <el-form-item label="合作时长" prop="shop_cooperation_duration" placeholder="请输入合作时长">
        <el-select
          v-model="ruleForm.shop_cooperation_duration"
          filterable
          ref="chooseKpi5"
          class="filter-item"
          value-key="id"
          placeholder="请选合作时长"
          @blur="chooseKpi5"
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
      <el-form-item label="结束日期" prop="order_end_date">
        <el-date-picker v-model="ruleForm.order_end_date" type="date" :disabled="true" placeholder="请选择结束日期" />
      </el-form-item>
      <el-form-item label="收款金额" prop="order_amount">
        <el-input v-model="ruleForm.order_amount" placeholder="请输入收款金额" />
      </el-form-item>
      <el-form-item label="成本费" prop="cost_fees">
        <el-input v-model="ruleForm.cost_fees" placeholder="请输入成本费" />
      </el-form-item>
      <el-form-item label="签约销售" prop="order_contract_sales" placeholder="请输入客户所在行业">
        <el-select
          v-model="ruleForm.order_contract_sales"
          filterable
          :disabled="true"
          class="filter-item"
          value-key="id"
          placeholder="请选择签约销售"
        >
          <el-option v-for="item in user_data" :key="item.id" :label="item.label" :value="item" />
        </el-select>
      </el-form-item>
      <el-form-item label="签约/续约" prop="qianyue_xuyue" placeholder="请输入客户所在行业">
        <el-select  
          v-model="ruleForm.qianyue_xuyue"
          ref="chooseKpi55"
          @blur="chooseKpi55"
          filterable
          class="filter-item"
          value-key="id"
          placeholder="请选择签约状态"
        >           
          <el-option v-for="item in q_x" :key="item.id" :label="item.label" :value="item" />
        </el-select>
      </el-form-item>
      <el-divider />
      <el-form-item v-for="(domain, index) in shop_add_form" :key="domain.key" :label="domain.label">
        <span v-if="domain.type === '文本类型'">
          <el-input v-model="domain.value" filterable  @blur="edit_shop_add_form(index,domain.value)" />
        </span>
        <span v-if="domain.type === '日期类型'">
          <el-date-picker
            v-model="domain.value"
            type="date"
            placeholder="选择日期"
            filterable
            @change="edit_shop_add_form(index,domain.value)"
          />
        </span>
        <span v-if="domain.type === '选择下拉框'">
          <el-select
            v-model="domain.value"
            ref="chooseKpi6"
            type="date"
            placeholder="选择内容"
            filterable
            @blur="chooseKpi6(index)"
            @change="edit_shop_add_form(index,domain.value)"
          >
            <el-option
              v-for="item in domain.select"
              :key="item.label"
              :label="item.label"
              :value="item.value"
              filterable
            />
          </el-select>
        </span>
        <span v-if="domain.type === '大文本框'">
          <el-input
            v-model="domain.value"
            type="textarea"
            filterable
            @blur="edit_shop_add_form(index,domain.value)"
          />
        </span>
      </el-form-item>
      <el-form-item label="付款截图">
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
      <el-form-item label="备注">
        <el-input v-model.trim="ruleForm.shop_remark" type="textarea" placeholder="备注信息" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
        <el-button @click="resetForm('ruleForm')">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
// import Chart from '@/components/Charts/Keyboard'

import request from '@/utils/request'
import global from '@/store/modules/user'
import city from '@/layout/components/Navbar'
import qs from 'qs';

export default {
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入订单编号'))
      } else {
        this.axios
          .get('http://127.0.0.1:8000/app/contract_id_verification/', {
            params: {
              contract_id: value
            }
          })
          .then(res => {
            if (res.data.state === 1) {
              callback(new Error('订单编号已存在，请重新输入'))
            } else {
              callback()
            }
          })
          .catch(function(error) {
            this.$notify({
              title: '创建失败',
              message: '创建失败',
              type: 'error'
            })
          })
      }
    }
    return {
      options: '',
      formLabelWidth: '80px',
      shop_add_form: '',
      shop_add_form_edit_edit:'',
      shop_add_form_edit: '',
      ruleForm: {
        order_date: '',
        contract_id: '',
        sign_contract_shop: [],
        customer_source: '',
        order_start_date: '',
        payment_method: '',
        order_end_date: '',
        contract_status: '',
        order_numbers: '',
        order_contract_sales: '',
        order: '',
        cost_fees:'',
        shop_remark: '',
        contracted_projects: '',
        shop_cooperation_duration: '',
        shop_telephonenumber: '',
        shop_industry: '',
        shop_kp_name: '',
        shop_add_form: '',
        qianyue_xuyue:'',
        region: '',
        date1: '',
        date2: '',
        delivery: false,
        type: [],
        resource: '',
        update:'',
        desc: '',
        dialogImageUrl:''
      },
      user_data: [],
      id: [],
      q_x:[{
        id:'新签',
        label:'新签'
      },{
        id:'续约',
        label:'续约'
      }],
      count: 0,
      year: 0,
      month: 0,
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
      shop_name: '',
      qianyue_xuyue:'',
      rules: {
        order_date: [
          {
            type: 'date',
            required: true,
            message: '请选择下单日期',
            trigger: 'change'
          }
        ],
        contract_id: [{ validator: validatePass, trigger: 'blur' }],
        shop_kp_name: [
          { required: true, message: '请输入KP姓名', trigger: 'change' }
        ],
        qianyue_xuyue: [
          { required: true, message: '请选择签约状态', trigger: 'change' }
        ],
        shop_telephonenumber: [
          { required: true, message: '请输入KP电话', trigger: 'change' }
        ],
        order_contract_sales: [
          { required: true, message: '请选择签约销售', trigger: 'change' }
        ],
        order_amount: [
          { required: true, message: '请输入收款金额', trigger: 'change' }
        ],
        cost_fees: [
          { required: true, message: '请输入成本费', trigger: 'change' }
        ],
        order_start_date: [
          { required: true, message: '请输入开始日期', trigger: 'change' }
        ],
        payment_method: [
          { required: true, message: '请输入支付方式', trigger: 'change' }
        ],
        order_end_date: [
          { required: true, message: '请选择结束日期', trigger: 'change' }
        ],
        order_numbers: [
          { required: true, message: '请输入签约门店数', trigger: 'change' }
        ],
        shop_industry: [
          { required: true, message: '请选择客户所在行业', trigger: 'change' }
        ],
        shop_cooperation_duration: [
          { required: true, message: '请选择合作时长', trigger: 'change' }
        ],
        sign_contract_shop: [
          {
            required: true,
            message: '请选择签约商户',
            trigger: 'change'
          }
        ],
        update: [
          {
            required: true,
            message: '请上传图片',
            trigger: 'change'
          }
        ],
        customer_source: [
          {
            required: true,
            message: '请选择客户来源',
            trigger: 'change'
          }
        ],
        contract_status: [
          {
            required: true,
            message: '请选择签约状态',
            trigger: 'change'
          }
        ],
        contracted_projects: [
          {
            required: true,
            message: '请选择签约项目-',
            trigger: 'change'
          }
        ],
        date2: [
          {
            type: 'date',
            required: true,
            message: '请选择时间',
            trigger: 'change'
          }
        ],
        type: [
          {
            type: 'array',
            required: true,
            message: '请至少选择一个活动性质',
            trigger: 'change'
          }
        ],
        resource: [
          { required: true, message: '请选择活动资源', trigger: 'change' }
        ],
        desc: [{ required: true, message: '请填写活动形式', trigger: 'blur' }],
      },
      dialogImageUrl: '',
      dialogVisible: false,
      url:'',
      update:'',
      create_count:1
    }
  },
  created: function() {
    var now = new Date()
    this.year = now.getFullYear().toString() // 得到年份
    this.month = now.getMonth() + 1
    this.get_shop_add_form()
    this.user_data_xiaoshou()
    this.get_user_shop()
    this.order_select()
    this.ruleForm.order_contract_sales = global.state['first_name']
  },
  methods: {
    noclick(){
      console.log(this.create_count)
      if (this.create_count == 1){
        this.create_count = 3
      }else if (this.create_count == 3){
        this.$refs.datePicker.hidePicker();
        this.$refs.datePicker2.hidePicker();
        this.create_count = 1
      }
    },
    datePicker_click(){
      this.create_count = 1
    },
    datePicker_click2(){
      this.create_count = 1
    },
    handleRemove(file, fileList) {
        this.$message({
          message: '已删除',
          type: 'warning'
        });
    },
    handlePictureCardPreview(file) {
        console.log(file.name)
        this.dialogImageUrl = 'http://127.0.0.1:8000/media/'+file.name;
        console.log('this.dialogImageUrl',this.dialogImageUrl)
        // this.url = this.dialogImageUrl
        this.dialogVisible = true;
    },
    handlechange(file){
      if (file.status == 'success'){
        console.log(file)
        this.$message({
          message: '上传成功',
          type: 'success'
        });
        this.dialogImageUrl = 'http://127.0.0.1:8000/media/'+file.name;
        console.log('this.dialogImageUrl',this.dialogImageUrl)
      }
    },
    chooseKpi4(){
      this.$refs.chooseKpi4.blur();
    },
    chooseKpi5(){
      this.$refs.chooseKpi5.blur();
    },
    chooseKpi55(){
      this.$refs.chooseKpi55.blur();
    },
    chooseKpi6(){
      this.$refs.chooseKpi6.blur();
    },
    order_select() {
      this.count = 0
      if (this.month.toString().length === 1) {
        console.log('0' + this.month)
        this.month = '0' + this.month
      }
      this.axios
        .get('http://127.0.0.1:8000/app/order_select_data/', {
          params: {
            username: global.state['first_name'],
            month: this.year + '-' + this.month
          }
        })
        .then(res => {
          if (this.month.toString().length === 1) {
            console.log('0' + this.month)
            this.month = '0' + this.month
          }
          if (res.data.count.length === 1) {
            this.count = '00' + res.data.count
          } else if (res.data.count.length === 2) {
            this.count = '0' + res.data.count
          }
          this.ruleForm.contract_id = this.year.toString() + this.month.toString() + 'D' + global.state['username'] + this.count
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    get_data(val) {
      this.year = val.getFullYear()
      this.month = val.getMonth() + 1
      this.order_select()
    },
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          for (var s = 0; s < this.shop_add_form.length; s++) {
            delete this.shop_add_form[s].select
          }
          console.log(this.shop_add_form)
          console.log('下单日期',this.ruleForm.order_date)
          console.log('开始日期',this.ruleForm.order_start_date)
          console.log('开始日期',this.dialogImageUrl)
          this.resetForm.shop_add_form = this.shop_add_form
          if (this.dialogImageUrl != ''){
            this.axios
            .get('http://127.0.0.1:8000/app/shenhe_order/', {
              params: {
                contract_id: this.ruleForm.contract_id,
                order_date: this.ruleForm.order_date,
                order_start_date: this.ruleForm.order_start_date,
                sign_contract_shop: this.shop_name,
                customer_source: this.ruleForm.customer_source,
                contract_status: this.ruleForm.contract_status,
                contracted_projects: this.ruleForm.contracted_projects,
                shop_industry: this.ruleForm.shop_industry.id,
                shop_kp_name: this.ruleForm.shop_kp_name,
                shop_telephonenumber: this.ruleForm.shop_telephonenumber,
                order_numbers: this.ruleForm.order_numbers,
                cost_fees:this.ruleForm.cost_fees,
                shop_cooperation_duration: this.ruleForm.shop_cooperation_duration.id,
                order_end_date: this.ruleForm.order_end_date,
                order_amount: this.ruleForm.order_amount,
                payment_method: this.ruleForm.payment_method,
                order_contract_sales: this.ruleForm.order_contract_sales,
                shop_remark: this.ruleForm.shop_remark,
                shop_add_form_data: JSON.stringify(this.resetForm.shop_add_form),
                shop_id: this.ruleForm.sign_contract_shop,
                tags:this.ruleForm.qianyue_xuyue.id,
                dialogImageUrl:this.dialogImageUrl
              }
            })
            .then(res => {
              if (res.data.state == 0) {
                this.$notify({                                                                              
                  title: '创建成功',
                  message: '创建成功，表单将重置',
                  type: 'success'
                })
                this.resetForm('ruleForm')
                this.order_select()
                this.axios
                .get('http://127.0.0.1:8000/app/contract_id_verification/', {
                  params: {
                    contract_id: value
                  }
                })
                .then(res => {
                  if (res.data.state === 1) {
                    callback(new Error('订单编号已存在，请重新输入'))
                  } else {
                    callback()
                  }
                })
              } else if (res.data.state == 1) {
                this.$notify({
                  title: '创建失败',
                  message: '该商户订单已提交审核',
                  type: 'error'
                })
              } else {
                this.$notify({
                  title: '创建失败',
                  message: '原因:' + res.data.msg + ',请联系管理员',
                  type: 'error'
                })
              }
            })
            .catch(function(error) {
              this.$notify({
                title: '创建失败',
                message: '创建失败',
                type: 'error'
              })
            })
          }else{
            this.$notify({
              title: '请上传图片',
              message: '注意：图片名称不能包含中文',
              type: 'error'
            })
          }
          
        } else {
          console.log('error submit!!')
          this.$notify({
            title: '创建失败',
            message: '检查是否填写完毕',
            type: 'error'
          })
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    change_order_date(data) {
      if (this.ruleForm.shop_cooperation_duration.id == '') {
        console.log('为空')
      } else {
        this.ruleForm.order_end_date = this.computeYmd(
          this.ruleForm.order_start_date.getFullYear() +
            '-' +
            (this.ruleForm.order_start_date.getMonth() + 1) +
            '-' +
            (this.ruleForm.order_start_date.getDate() + 1),
          this.ruleForm.shop_cooperation_duration.id
        )
      }
    },
    change_shop_cooperation_duration(data) {
      console.log(data.id)
      this.ruleForm.order_end_date = this.computeYmd(
        this.ruleForm.order_start_date.getFullYear() +
          '-' +
          (this.ruleForm.order_start_date.getMonth() + 1) +
          '-' +
          (this.ruleForm.order_start_date.getDate() + 1),
        data.id
      )
      this.$forceUpdate();
    },
    computeYmd(val, data) {
      const str = val.split('-')
      // let d = new Date(str[0], str[1], str[2]);
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
    user_data_xiaoshou() {
      this.axios
        .get('http://127.0.0.1:8000/app/get_user_data/', {})
        .then(res => {
          // this.user_data = res.data.data
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    edit_shop_add_form(index, value) {
      for (var i = 0, len = this.shop_add_form.length; i < len; i++) {
        if (this.shop_add_form[i].label == value) {
          this.shop_add_form[i].label == value
        }
      }
    },
    get_user_shop() {
      // console.log('123')
      this.axios
        .get('http://127.0.0.1:8000/app/get_user_shop/', {
          params: {
            // 每页显示的条数
            username: global.state['first_name']
          }
        })
        .then(res => {
          this.options = res.data.data
          // this.ruleForm.shop_kp_name = res.data.shop_kp_name;
          // this.ruleForm.shop_telephonenumber = res.data.shop_telephonenumber;
          // this.ruleForm.shop_industry = res.data.shop_industry;
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    get_shop_date(data) {
      console.log(data)
      this.axios
        .get('http://127.0.0.1:8000/app/get_shop_date/', {
          params: {
            // 每页显示的条数
            shop_id: data
          }
        })
        .then(res => {
          console.log(res)
          this.ruleForm.shop_kp_name = res.data.shop_kp_name
          this.ruleForm.shop_telephonenumber = res.data.shop_telephonenumber
          this.ruleForm.shop_industry = res.data.shop_region
          this.shop_name = res.data.shop_name
          console.log(this.shop_name)
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
      this.$forceUpdate();
    },
    get_shop_add_form(shop_id) {
      this.axios
        .get('http://127.0.0.1:8000/app/table_simple_get_order_form/', {})
        .then(res => {
          this.shop_add_form = res.data.data
          for (var i = 0, len = this.this.shop_add_form.length; i < len; i++) {
            this.shop_edit[i] = undefined
          }     
          console.log('详情', this.shop_add_form)
          console.log(this.shop_edit)
        })      
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })      
    }           
  }
}
</script>
<style>
.demo-ruleForm {
  width: 30%;
}
@media only screen and (max-width: 500px) {
  .demo-ruleForm {
    width: 80%;
  }
}
</style>
