from django.db import models

# Create your models here.

# 丽人系列全部商家信息


class Dazhongdianping_liren_all_data(models.Model):
    shop_id = models.CharField(max_length=100)  # 店铺id
    shop_name = models.CharField(max_length=100)  # 店铺名称
    shop_start = models.CharField(max_length=100)  # 店铺星级
    shop_review_count = models.CharField(max_length=100)  # 评论数
    shop_bad_review = models.CharField(max_length=100)  # 差评数
    shop_per_capita_consumption = models.CharField(max_length=100)  # 人均消费
    shop_effect = models.CharField(max_length=100)  # 效果
    shop_service = models.CharField(max_length=100)  # 服务
    shop_surroundings = models.CharField(max_length=100)  # 环境
    shop_region = models.CharField(max_length=100)  # 区域
    shop_business_district = models.CharField(max_length=100)  # 商圈
    shop_category = models.CharField(max_length=100)  # 品类
    shop_address = models.CharField(max_length=100)  # 地址
    shop_telephonenumber = models.CharField(max_length=100)  # 电话
    shop_edit = models.CharField(max_length=100, default='无')
    shop_tags = models.CharField(max_length=100)  # 客户标签
    shop_kp_name = models.CharField(max_length=100)  # KP姓名
    shop_kp_position = models.CharField(max_length=100)  # KP职位
    shop_kp_wechat_id = models.CharField(max_length=100)  # 微信号
    shop_kp_city = models.CharField(max_length=100)  # 北京市
    shop_kp_category = models.CharField(max_length=100)  # 北京市
    shop_add_form = models.CharField(max_length=100)  # 北京市
    shop_city = models.CharField(max_length=100)

    # def __str__(self):
    #     return "<Emp:({shop_id},{shop_name},{shop_start},{shop_review_count}," \
    #            "{shop_bad_review},{shop_per_capita_consumption},{shop_effect}," \
    #            "{shop_service},{shop_surroundings},{shop_region},{shop_business_district}," \
    #            "{shop_category},{shop_address}," \
    #            "{shop_telephonenumber},{shop_edit})>".format(id=self.shop_id,
    #                                              shop_name=self.shop_name,
    #                                              shop_reviewcount=self.shop_start,
    #                                              shop_avgpricetitle=self.shop_review_count ,
    #                                              shop_effect=self.shop_bad_review,
    #                                              shop_service=self.shop_per_capita_consumption,
    #                                              shop_surroundings=self.shop_effect,
    #                                              shop_address=self.shop_service,
    #                                              shop_region = self.shop_region,
    #                                              shop_business_district = self.shop_business_district,
    #                                              shop_category = self.shop_category,
    #                                              shop_edit = self.shop_edit,
    #                                              shop_telephonenumber=self.shop_surroundings,
    #                                              shop_businesshours=self.shop_address,
    #                                              shop_url=self.shop_telephonenumber)

# 丽人系列全部商家信息


class Dazhongdianping_liren_user_data(models.Model):
    username = models.CharField(max_length=100)
    shop_id = models.CharField(max_length=100)  # 店铺id
    shop_name = models.CharField(max_length=100)  # 店铺名称
    shop_start = models.CharField(max_length=100)  # 店铺星级
    shop_review_count = models.CharField(max_length=100)  # 评论数
    shop_bad_review = models.CharField(max_length=100)  # 差评数
    shop_per_capita_consumption = models.CharField(max_length=100)  # 人均消费
    shop_effect = models.CharField(max_length=100)  # 效果
    shop_service = models.CharField(max_length=100)  # 服务
    shop_surroundings = models.CharField(max_length=100)  # 环境
    shop_region = models.CharField(max_length=100)  # 区域
    shop_business_district = models.CharField(max_length=100)  # 商圈
    shop_category = models.CharField(max_length=100)  # 品类
    shop_address = models.CharField(max_length=100)  # 地址
    shop_telephonenumber = models.CharField(max_length=100)  # 电话
    shop_edit = models.CharField(max_length=100, default='无')
    shop_tags = models.CharField(max_length=100, default='无')
    shop_kp_name = models.CharField(max_length=100)  # KP姓名
    shop_kp_position = models.CharField(max_length=100)  # KP职位
    shop_kp_wechat_id = models.CharField(max_length=100)  # 微信号
    shop_kp_city = models.CharField(max_length=100)  # 北京市
    shop_kp_category = models.CharField(max_length=100)  # 北京市
    pull_date = models.CharField(max_length=100, default='无')
    position = models.CharField(max_length=100)
    shop_add_form = models.CharField(max_length=100)
    shop_city = models.CharField(max_length=100)

class Business_district_select(models.Model):
    business_district = models.CharField(max_length=100)
    shop_city = models.CharField(max_length=100)

class Dazhongdianping_liren_signing_data(models.Model):
    # 店铺id
    shop_id = models.CharField(max_length=100)
    # 店铺名称
    shop_name = models.CharField(max_length=100)
    # 店铺用户名
    shop_user = models.CharField(max_length=100)
    # 评论数
    shop_review_count = models.CharField(max_length=100)
    # 星级
    shop_start = models.CharField(max_length=100)
    # 店铺密码
    shop_password = models.CharField(max_length=100)
    # 店铺cookie
    shop_cookie = models.CharField(max_length=100)
    # 店铺storekey
    shop_storekey = models.CharField(max_length=100)
    # 曝光人数
    shop_exposures = models.CharField(max_length=100)
    # 访问人数
    shop_visitors = models.CharField(max_length=100)
    # 下单人数
    shop_orders = models.CharField(max_length=100)
    # 预约人数
    shop_reservations = models.CharField(max_length=100)
    # 到店消费人数
    shop_consumption = models.CharField(max_length=100)
    # 新增评论数
    shop_new_reviews_count = models.CharField(max_length=100)
    # 新增差评数
    shop_new_bad_review = models.CharField(max_length=100)
    # 差评回复率
    shop_bad_review_response = models.CharField(max_length=100)

    shop_csm_amt_tuangou = models.CharField(max_length=100, default=0)
    # 到店消费金额占比_一口价
    shop_csm_amt_yikoujia = models.CharField(max_length=100, default=0)

    shop_csm_amt_cika = models.CharField(
        max_length=100, default=0)  # 到店消费金额占比_团购
    # 到店消费金额笔数占比_团购
    shop_csm_cnt_tuangou = models.CharField(max_length=100, default=0)
    # 到店消费笔数占比_一口价
    shop_csm_cnt_yikoujia = models.CharField(max_length=100, default=0)
    # 到店消费笔数占比_此卡
    shop_csm_cnt_cika = models.CharField(
        max_length=100, default=0)  # 到店消费金额占比_团购
    # 到店消费笔数人次占比_团购
    shop_csm_renci_tuangou = models.CharField(max_length=100, default=0)
    # 到店消费人次占比_一口价
    shop_csm_renci_yikoujia = models.CharField(max_length=100, default=0)
    # 到店消费人次占比_此卡
    shop_csm_renci_cika = models.CharField(max_length=100, default=0)


class User(models.Model):
    # 用户名
    name = models.CharField(max_length=100)
    # 姓名
    username = models.CharField(max_length=100)
    # 密码
    pwd = models.CharField(max_length=100)
    # 加入时间
    last_time = models.DateTimeField()
    # 手机号码
    phone = models.CharField(max_length=100)
    # 邮箱
    email = models.CharField(max_length=100)
    # 性别
    gender = models.CharField(max_length=100)
    # 拥有权限
    have_access = models.CharField(max_length=100)
    # 具体描述
    specific_description = models.CharField(max_length=100)
    # 角色
    role = models.CharField(max_length=100)
    # 拉商户
    pull_01 = models.CharField(max_length=100, default='0')
    pull_02 = models.CharField(max_length=100, default='0')
    pull_03 = models.CharField(max_length=100, default='0')
    pull_04 = models.CharField(max_length=100, default='0')
    pull_05 = models.CharField(max_length=100, default='0')
    pull_06 = models.CharField(max_length=100, default='0')
    pull_07 = models.CharField(max_length=100, default='0')
    pull_08 = models.CharField(max_length=100, default='0')
    pull_09 = models.CharField(max_length=100, default='0')
    pull_10 = models.CharField(max_length=100, default='0')
    pull_11 = models.CharField(max_length=100, default='0')
    pull_12 = models.CharField(max_length=100, default='0')
    pull_13 = models.CharField(max_length=100, default='0')
    pull_14 = models.CharField(max_length=100, default='0')
    pull_15 = models.CharField(max_length=100, default='0')
    pull_16 = models.CharField(max_length=100, default='0')
    pull_17 = models.CharField(max_length=100, default='0')
    pull_18 = models.CharField(max_length=100, default='0')
    pull_19 = models.CharField(max_length=100, default='0')
    pull_20 = models.CharField(max_length=100, default='0')


class Dazhongdianping_liren_new_all_data(models.Model):
    shop_id = models.CharField(max_length=100)  # 店铺id
    shop_name = models.CharField(max_length=100)  # 店铺名称
    shop_start = models.CharField(max_length=100)  # 店铺星级
    shop_review_count = models.CharField(max_length=100)  # 评论数
    shop_per_capita_consumption = models.CharField(max_length=100)  # 人均消费
    shop_effect = models.CharField(max_length=100)  # 效果
    shop_service = models.CharField(max_length=100)  # 服务
    shop_surroundings = models.CharField(max_length=100)  # 环境
    shop_region = models.CharField(max_length=100)  # 区域
    shop_business_district = models.CharField(max_length=100)  # 商圈
    shop_category = models.CharField(max_length=100)  # 品类
    shop_address = models.CharField(max_length=100)  # 地址
    shop_telephonenumber = models.CharField(max_length=100)  # 电话
    shop_edit = models.CharField(max_length=100, default='无')
    shop_tags = models.CharField(max_length=100)

class Citydata(models.Model):
    city = models.CharField(max_length=100, default='20')
    data = models.CharField(max_length=10000, default='20')

class Setting_storage(models.Model):
    private_sea_time = models.CharField(max_length=100, default='20')
    private_sea_length = models.CharField(max_length=100, default='20')
    tags_data = models.CharField(max_length=100, default='20')
    edit_form = models.CharField(max_length=10000, default='20')
    order_form = models.CharField(max_length=10000, default='20')
    todo_form = models.CharField(max_length=10000, default='20')
    commission_form = models.CharField(max_length=10000, default='20')
    shouye_data = models.CharField(max_length=10000, default='20')
    date = models.CharField(max_length=10000, default='20')

class Pending_review(models.Model):
    project = models.CharField(max_length=100, default='20')
    shop_name = models.CharField(max_length=100, default='20')
    order_id = models.CharField(max_length=100, default='20')
    time = models.CharField(max_length=100, default='20')
    money = models.CharField(max_length=100, default='20')
    schedule = models.CharField(max_length=100, default='20')
    username = models.CharField(max_length=100, default='20')
    submitter = models.CharField(max_length=100, default='20')
    submit_time = models.CharField(max_length=100, default='20')
    success_time = models.CharField(max_length=100, default='20')
    edit = models.CharField(max_length=100, default='20')
    lat = models.CharField(max_length=100, default='20')
    lng = models.CharField(max_length=100, default='20')
    status = models.CharField(max_length=100, default='20')
    url = models.CharField(max_length=100, default='20')

class Completed(models.Model):
    project = models.CharField(max_length=100, default='20')
    shop_name = models.CharField(max_length=100, default='20')
    time = models.CharField(max_length=100, default='20')
    money = models.CharField(max_length=100, default='20')
    order_id = models.CharField(max_length=100, default='20')
    schedule = models.CharField(max_length=100, default='20')
    username = models.CharField(max_length=100, default='20')
    submitter = models.CharField(max_length=100, default='20')
    submit_time = models.CharField(max_length=100, default='20')
    status = models.CharField(max_length=100, default='20')
    success_time = models.CharField(max_length=100, default='20')
    url = models.CharField(max_length=100, default='20')
    

class To_do(models.Model):
    project = models.CharField(max_length=100, default='20')
    shop_name = models.CharField(max_length=100, default='20')
    time = models.CharField(max_length=100, default='20')
    money = models.CharField(max_length=100, default='20')
    order_id = models.CharField(max_length=100, default='20')
    schedule = models.CharField(max_length=100, default='20')
    username = models.CharField(max_length=100, default='20')
    status = models.CharField(max_length=100, default='20')
    edit = models.CharField(max_length=100, default='20')

class Setting(models.Model):
    private_sea_time = models.CharField(max_length=100, default='20')
    private_sea_length = models.CharField(max_length=100, default='20')
    tags_data = models.CharField(max_length=100, default='20')
    edit_form = models.CharField(max_length=10000, default='20')
    todo_form = models.CharField(max_length=10000, default='20')
    shouye_data = models.CharField(max_length=10000, default='20')



class Work_order(models.Model):
    work_name = models.CharField(max_length=100, default='20')  # 项目名称
    work_start_time = models.CharField(max_length=100, default='20')  # 项目开始时间
    work_status = models.CharField(max_length=100, default='20')  # 项目状态
    work_deadline = models.CharField(max_length=100, default='20')  # 项目截止时间
    work_implementer_sheji = models.CharField(
        max_length=100, default='20')  # 项目实施人
    work_implementer_wenan = models.CharField(
        max_length=100, default='20')  # 项目实施人
    work_implementer_xiaoshou = models.CharField(
        max_length=100, default='20')  # 项目实施人
    work_implementer_xiutu = models.CharField(
        max_length=100, default='20')  # 项目实施人
    work_publisher = models.CharField(max_length=100, default='20')  # 项目发布人
    work_edit = models.CharField(max_length=100, default='20')  # 项目发布人
    work_implementer_sheji_button = models.CharField(
        max_length=100, default='20')  # 项目实施人
    work_implementer_wenan_button = models.CharField(
        max_length=100, default='20')  # 项目实施人
    work_implementer_xiutu_button = models.CharField(
        max_length=100, default='20')  # 项目实施人

class My_visit(models.Model):
    visit_id = models.CharField(max_length=100, default='20')
    visit_shop_name = models.CharField(max_length=100, default='20')  # 拜访的商户名
    visit_time = models.CharField(max_length=100, default='20')  # 什么时候拜访的
    visit_name = models.CharField(max_length=100, default='20')  # 谁拜访的
    visit_data =  models.CharField(max_length=100, default='20')  # 拜访的内容


class Order(models.Model):
    shop_id =  models.CharField(max_length=100, default='20') 
    contract_id = models.CharField(max_length=100, default='20')  # 订单编号
    order_date = models.CharField(max_length=100, default='20')  # 下单日期
    order_start_date = models.CharField(max_length=100, default='20')  # 开始日期
    sign_contract_shop = models.CharField(max_length=100, default='20')  # 签约商户
    customer_source = models.CharField(max_length=100, default='20')  # 客户来源
    contract_status = models.CharField(max_length=100, default='20')  # 签约状态
    contracted_projects = models.CharField(
        max_length=100, default='20')  # 签约项目
    shop_industry = models.CharField(max_length=100, default='20')  # 所在行业
    shop_kp_name = models.CharField(max_length=100, default='20')  # KP姓名
    cost_fees = models.CharField(max_length=100, default='20')  # KP姓名
    shop_telephonenumber = models.CharField(
        max_length=100, default='20')  # KP电话
    order_numbers = models.CharField(max_length=100, default='20')  # 签约店数
    shop_cooperation_duration = models.CharField(
        max_length=100, default='20')  # 合作时长
    order_end_date = models.CharField(max_length=100, default='20')  # 结束日期
    order_amount = models.CharField(max_length=100, default='20')  # 收款金额
    payment_method = models.CharField(max_length=100, default='20')  # 支付方式
    order_contract_sales = models.CharField(
        max_length=100, default='20')  # 签约销售
    shop_remark = models.CharField(max_length=100, default='20')  # 备注
    order_form = models.CharField(max_length=100, default='20')  # 备注
    order_commission = models.CharField(max_length=100, default='20')  # 备注
    tags = models.CharField(max_length=100, default='20')
    city = models.CharField(max_length=100, default='20')
    date = models.CharField(max_length=100, default='20')


class Shenhe_order(models.Model):
    shop_id =  models.CharField(max_length=100, default='20') 
    contract_id = models.CharField(max_length=100, default='20')  # 订单编号
    order_date = models.CharField(max_length=100, default='20')  # 下单日期
    order_start_date = models.CharField(max_length=100, default='20')  # 开始日期
    sign_contract_shop = models.CharField(max_length=100, default='20')  # 签约商户
    customer_source = models.CharField(max_length=100, default='20')  # 客户来源
    contract_status = models.CharField(max_length=100, default='20')  # 签约状态
    contracted_projects = models.CharField( max_length=100, default='20')  # 签约项目
    shop_industry = models.CharField(max_length=100, default='20')  # 所在行业
    shop_kp_name = models.CharField(max_length=100, default='20')  # KP姓名
    cost_fees = models.CharField(max_length=100, default='20')  # KP姓名
    shop_telephonenumber = models.CharField(max_length=100, default='20')  # KP电话
    order_numbers = models.CharField(max_length=100, default='20')  # 签约店数
    shop_cooperation_duration = models.CharField(max_length=100, default='20')  # 合作时长
    order_end_date = models.CharField(max_length=100, default='20')  # 结束日期
    order_amount = models.CharField(max_length=100, default='20')  # 收款金额
    payment_method = models.CharField(max_length=100, default='20')  # 支付方式
    order_contract_sales = models.CharField(max_length=100, default='20')  # 签约销售
    shop_remark = models.CharField(max_length=100, default='20')  # 备注
    order_form = models.CharField(max_length=100, default='20')  # 备注
    order_commission = models.CharField(max_length=100, default='20')  # 备注
    tags = models.CharField(max_length=100, default='20')
    city = models.CharField(max_length=100, default='20')
    dialogImageUrl = models.CharField(max_length=100, default='20')

class Group(models.Model):
    group_name = models.CharField(max_length=100,default='20')

class user_profile(models.Model):
    password = models.CharField(max_length=100, default='20')  # 项目名称
    last_login = models.CharField(max_length=100, default='20')  # 项目名称
    is_superuser = models.CharField(max_length=100, default='20')  # 项目名称
    username = models.CharField(max_length=100, default='20')  # 项目名称
    first_name = models.CharField(max_length=100, default='20')  # 项目名称
    last_name = models.CharField(max_length=100, default='20')  # 项目名称
    email = models.CharField(max_length=100, default='20')  # 项目名称
    is_staff = models.CharField(max_length=100, default='20')  # 项目名称
    is_active = models.CharField(max_length=100, default='20')  # 项目名称
    date_joined = models.CharField(max_length=100, default='20')  # 项目名称
    avatar = models.CharField(max_length=100, default='20')  # 项目名称
    role = models.CharField(max_length=100, default='20')  # 项目名称
    introduction = models.CharField(max_length=100, default='20')  # 项目名称
    group_name = models.CharField(max_length=100, default='20')  # 项目名称m

class Tuikuan_Order(models.Model):
    order_id = models.CharField(max_length=100, default='20')  # 项目名称
    order_date_before = models.CharField(max_length=100, default='20')  # 项目名称
    order_date_after = models.CharField(max_length=100, default='20')  # 项目名称
    order_start_date_before = models.CharField(max_length=100, default='20')  # 项目名称
    order_start_date_after = models.CharField(max_length=100, default='20')  # 项目名称
    shop_cooperation_duration_before = models.CharField(max_length=100, default='20')  # 项目名称
    shop_cooperation_duration_after = models.CharField(max_length=100, default='20')  # 项目名称
    order_amount_before = models.CharField(max_length=100, default='20')  # 项目名称
    order_amount_after = models.CharField(max_length=100, default='20')  # 项目名称
    cost_fees_before = models.CharField(max_length=100, default='20')  # 项目名称
    cost_fees_after = models.CharField(max_length=100, default='20')  # 项目名称
    order_contract_sales = models.CharField(max_length=100, default='20')  # 项目名称
    order_end_date = models.CharField(max_length=100, default='20')  # 项目名称
    sign_contract_shop = models.CharField(max_length=100, default='20')  # 项目名称m
    tags = models.CharField(max_length=100, default='20')  # 项目名称m