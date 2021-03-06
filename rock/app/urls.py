from . import views
from django.urls import path

urlpatterns = [
    path('', views.login, name='login'),
    path('console/', views.console, name='console'),
    path('weixin/', views.weixin, name='weixin'),
    path('weixin', views.weixin, name='weixin'),
    # path('weixincontroll.*', views.weixincontroll, name='weixincontroll'),
    path('table_simple/', views.table_simple, name='table_simple'),
    # 签约商户数据
    path('table_simple_signing/',
         views.table_simple_signing,
         name='table_simple_signing'),
    path('create_tuikuan_order/',
         views.create_tuikuan_order,
         name='create_tuikuan_order'),
    # 跳转修改密码页面
    path('password/', views.password, name='password'),
    path('get_user_data/', views.get_user_data, name='get_user_data'),
    path('shop_business_district_select/',
         views.shop_business_district_select,
         name='shop_business_district_select'),
    path('create_order/', views.create_order, name='create_order'),
    path('get_shop_date/', views.get_shop_date, name='get_shop_date'),
    path('test/', views.test, name='test'),
    path('update_city/', views.update_city, name='update_city'),
    path('select_city/', views.select_city, name='select_city'),
    path('get_top_one/', views.get_top_one, name='get_top_one'),
    path('select_urban_area/',
         views.select_urban_area,
         name='select_urban_area'),
    path('select_business_circle/',
         views.select_business_circle,
         name='select_business_circle'),
    path('get_shop_name/', views.get_shop_name, name='get_shop_name'),
    path('get_cities/', views.get_cities, name='get_cities'),
    path('get_number_orders/', views.get_number_orders, name='get_number_orders'),
    path('select_urban_area_user/',
         views.select_urban_area_user,
         name='select_urban_area_user'),
    path('jump_xindian/', views.jump_xindian, name='jump_xindian'),
    path('transfer_update/', views.transfer_update, name='transfer_update'),
    path('get_jump_href/', views.get_jump_href, name='get_jump_href'),
    path('update_jump_href/', views.update_jump_href, name='update_jump_href'),
    path('create_user_data/', views.create_user_data, name='create_user_data'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('get_todo_form/', views.get_todo_form, name='get_todo_form'),
    path('img_test/', views.img_test, name='img_test'),
    path('delete_visit/', views.delete_visit, name='delete_visit'),
    path('edit_shop_add_form_data_edit_baifang/',views.edit_shop_add_form_data_edit_baifang,name='edit_shop_add_form_data_edit_baifang'),
    path('table_simple_to_do/',
         views.table_simple_to_do,
         name='table_simple_to_do'),
    path('order_count/', views.order_count, name='order_count'),
    path('table_simple_visit/',
         views.table_simple_visit,
         name='table_simple_visit'),
    path('edit_shop_add_form_data_baifang/',
         views.edit_shop_add_form_data_baifang,
         name='edit_shop_add_form_data_baifang'),
    path('edit_order_form_data/',
         views.edit_order_form_data,
         name='edit_order_form_data'),
    path('contract_id_verification/',
         views.contract_id_verification,
         name='contract_id_verification'),
    path('table_simple_order_data/',
         views.table_simple_order_data,
         name='table_simple_order_data'),
    path('table_simple_order_data_all/',
         views.table_simple_order_data_all,
         name='table_simple_order_data_all'),
    path('select_shop_data/', views.select_shop_data, name='select_shop_data'),
    path('order_select/', views.order_select, name='order_select'),
    path('get_to_do/', views.get_to_do, name='get_to_do'),
    path('edit_todo_form/', views.edit_todo_form, name='edit_todo_form'),
    path('edit_commission_form/',
         views.edit_commission_form,
         name='edit_commission_form'),
    path('get_commission_form/',
         views.get_commission_form,
         name='get_commission_form'),
    # 跳转修改密码页面1
    path('edit_form/', views.edit_form, name='edit_form'),
    path('edit_order_form/', views.edit_order_form, name='edit_order_form'),
    path('get_order_form/', views.get_order_form, name='get_order_form'),
    path('table_simple_get_order_form/',
         views.table_simple_get_order_form,
         name='table_simple_get_order_form'),
    path('get_user_shop/', views.get_user_shop, name='get_user_shop'),
    # 显示用户数据
    path('create_user/', views.create_user, name='create_user'),
    path('shop_business_district_select_create/', views.shop_business_district_select_create, name='shop_business_district_select_create'),
    path('table_simple_user_data/',
         views.table_simple_user_data,
         name='table_simple_user_data'),
    # 添加签约商户
    path('search_business_circle/',
         views.search_business_circle,
         name='search_business_circle'),
    # 添加商户
    path('table_simple_data_add/',
         views.table_simple_data_add,
         name='table_simple_data_add'),
    # 添加新店
    path('table_simple_new_data_add/',
         views.table_simple_new_data_add,
         name='table_simple_new_data_add'),
    # 查询编辑信息
    path('table_simple_get_edit/',
         views.table_simple_get_edit,
         name='table_simple_get_edit'),
    # 修改商户信息
    path('table_simple_get_tags_new/',
         views.table_simple_get_tags_new,
         name='table_simple_get_tags_new'),
    # 跳转用户页面
    # path('user/', views.user, name='user'),# 跳转用户页面
    # 查找商圈
    # path('email/', views.email, name='email'),# 跳转用户页面
    # path('table_simple_data_bar_plus/', views.table_simple_data_bar_plus, name='table_simple_data_bar_plus'),# 跳转用户页面
    # 新店页面
    path('table_simple_new/', views.table_simple_new, name='table_simple_new'),
    path('table_simple_pending_review/',
         views.table_simple_pending_review,
         name='table_simple_pending_review'),
    # 签约商户信息
    path('table_simple_data_signing/',
         views.table_simple_data_signing,
         name='table_simple_data_signing'),
    # 显示用户数据
    path('user_data/', views.user_data, name='user_data'),  # 显示用户数据
    path('table_simple_data_edit/',
         views.table_simple_data_edit,
         name='table_simple_data_edit'),  # 显示用户数据
    path('table_simple_new_get_edit/',
         views.table_simple_new_get_edit,
         name='table_simple_new_get_edit'),
    # 添加用户
    path('select_user/', views.select_user, name='select_user'),
    path('post_completed/', views.post_completed, name='post_completed'),
    path('delete_order/', views.delete_order, name='delete_order'),
    path('get_completed/', views.get_completed, name='get_completed'),
    path('audit_failure/', views.audit_failure, name='audit_failure'),
    path('get_private_sea/', views.get_private_sea, name='get_private_sea'),
    path('private_sea_edit/', views.private_sea_edit, name='private_sea_edit'),
    # 获取表单数据
    path('get_form/', views.get_form, name='get_form'),
    path('get_shouye_data/', views.get_shouye_data, name='get_shouye_data'),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('select_citydata/', views.select_citydata, name='select_citydata'),
    path('save_shouye_data/', views.save_shouye_data, name='save_shouye_data'),
    path('create_group/', views.create_group, name='create_group'),
    path('get_group_data/', views.get_group_data, name='get_group_data'),
    path('update_user_data_yes/', views.update_user_data_yes, name='update_user_data_yes'),
    
    path('get_pending_review/',
         views.get_pending_review,
         name='get_pending_review'),
    #　全部商户表单获取
    path('table_simple_get_form/',
         views.table_simple_get_form,
         name='table_simple_get_form'),
    #　全部商户表单修改
    path('edit_shop_add_form_data/',
         views.edit_shop_add_form_data,
         name='edit_shop_add_form_data'),
    # 用户权限
    # 加载个人信息
    path('order_select_data/',
         views.order_select_data,
         name='order_select_data'),
    path('get_xiaoshou_data/',
         views.get_xiaoshou_data,
         name='get_xiaoshou_data'),
    path('create_table/', views.create_table, name='create_table'),
    # 修改个人信息
    # 画图显示商家信息
    # path('table_simple_data_bar/', views.table_simple_data_bar, name='table_simple_data_bar'),
    # 跳转到数据分析页
    path('transfer_details_page/',
         views.transfer_details_page,
         name='transfer_details_page'),
    # 拉商户
    path('pull_add/', views.pull_add, name='pull_add'),
    path('get_shop_edit_pull/', views.get_shop_edit_pull, name='get_shop_edit_pull'),
    path('table_simple_user_data_edit/', views.table_simple_user_data_edit, name='table_simple_user_data_edit'),
    path('get_benyuejiangjing/', views.get_benyuejiangjing, name='get_benyuejiangjing'),
    path('get_benyuejiangjing_xiayue/', views.get_benyuejiangjing_xiayue, name='get_benyuejiangjing_xiayue'),
    path('get_benyueyeji/', views.get_benyueyeji, name='get_benyueyeji'),
    # 回退数据
    path('pull_back/', views.pull_back, name='pull_back'),
    # 跳转到销售客户
    path('go_private_sea/', views.go_private_sea, name='go_private_sea'),
    # 查看销售客户
    path('table_simple_private_sea_data/',
         views.table_simple_private_sea_data,
         name='table_simple_private_sea_data'),
    path('get_performance_this_month/',
         views.get_performance_this_month,
         name='get_performance_this_month'),
    path('delete_shenhe/',
         views.delete_shenhe,
         name='delete_shenhe'),
    # 查看销售自己的客户
    path('change_private_sea_username/',
         views.change_private_sea_username,
         name='change_private_sea_username'),
    # 获取城区数据
    path('city_statistics/', views.city_statistics, name='city_statistics'),
    # 全部用户
    path('username_data/', views.username_data, name='username_data'),
    # 全部工单
    path('table_work_order_data/',
         views.table_work_order_data,
         name='table_work_order_data'),
    # 全部工单
    path('get_top_group/',
         views.get_top_group,
         name='get_top_group'),
    path('get_performance_this_year/',
         views.get_performance_this_year,
         name='get_performance_this_year'),
    path('get_qiandan_this_year/',
         views.get_qiandan_this_year,
         name='get_qiandan_this_year'),
    path('get_xiaoshou_this_year/',
         views.get_xiaoshou_this_year,
         name='get_xiaoshou_this_year'),
    path('shenhe_order/',
         views.shenhe_order,
         name='shenhe_order'),
    path('update_img/',
         views.update_img,
         name='update_img'),
    path('shenhe_order_select/',
         views.shenhe_order_select,
         name='shenhe_order_select'),
    path('update_order_ok/',
         views.update_order_ok,
         name='update_order_ok'),
    path('get_xiaoshou_group_this_year/',
         views.get_xiaoshou_group_this_year,
         name='get_xiaoshou_group_this_year'),
    path('selelct_xiaoshou/',
         views.selelct_xiaoshou,
         name='selelct_xiaoshou'),
    path('transfer_update_order/',
         views.transfer_update_order,
         name='transfer_update_order'),
    path('append_table/',
         views.append_table,
         name='append_table'),
    path('select_new_date/',
         views.select_new_date,
         name='select_new_date'),
    path('send_data/',
         views.send_data,
         name='send_data'),
    path('select_order/',
         views.select_order,
         name='select_order'),
    # 添加工单
    path('table_work_order_add/',
         views.table_work_order_add,
         name='table_work_order_add'),
    # 修改工单
    path('table_work_order_edit/',
         views.table_work_order_edit,
         name='table_work_order_edit'),
    # 获取销售的数据
    path('work_implementer_xiaoshou/',
         views.work_implementer_xiaoshou,
         name='work_implementer_xiaoshou'),
    # 获取文案的数据
    path('work_implementer_wenan/',
         views.work_implementer_wenan,
         name='work_implementer_wenan'),
    # 获取设计的数据
    path('work_implementer_sheji/',
         views.work_implementer_sheji,
         name='work_implementer_sheji'),
    # 获取修图的数据
    path('work_implementer_xiutu/',
         views.work_implementer_xiutu,
         name='work_implementer_xiutu'),
    # 获取品类数据
    path('category_data/', views.category_data, name='category_data'),
    # 获取全部商户的标签
    path('table_simple_get_tags/',
         views.table_simple_get_tags,
         name='table_simple_get_tags'),
    # 获取新店的标签
    path('table_simple_new_get_tags/',
         views.table_simple_new_get_tags,
         name='table_simple_new_get_tags'),
    # 获取用户商户的标签
    path('table_simple_get_tags_user/',
         views.table_simple_get_tags_user,
         name='table_simple_get_tags_user'),
    # 全部商户数据
    path('table_simple_data/',
         views.table_simple_data,
         name='table_simple_data'),
    # 全部新店数据
    path('table_simple_new_data/',
         views.table_simple_new_data,
         name='table_simple_new_data'),
    # 更改新店备注信息
    path('table_simple_new_data_edit/',
         views.table_simple_new_data_edit,
         name='table_simple_new_data_edit'),
    # 用户管理
    path('required_login/', views.required_login, name='required_login'),
    path('get_xiaoshou_jj/', views.get_xiaoshou_jj, name='get_xiaoshou_jj'),
    path('get_money_jj/', views.get_money_jj, name='get_money_jj'),
    path('table_simple_data_count/',
         views.table_simple_data_count,
         name='table_simple_data_count'),
    # 登陆
    # re_path('login/', views.login, name='login'),
    # 退出登录
]