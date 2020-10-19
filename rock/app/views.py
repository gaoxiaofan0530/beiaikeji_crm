# coding:utf-8
import base64
import operator
import os
import re
import uuid
import requests
import math
import xmltodict
from django.db.models import Q
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse, redirect, reverse
from app import models
from django.db import connection
import json
import datetime
import math
import sys
import pymysql
import time
from django.http.response import HttpResponse
from wechatpy.exceptions import InvalidSignatureException
import xml.etree.ElementTree as ET
from app.WXBizMsgCrypt import WXBizMsgCrypt
from django.utils.deprecation import MiddlewareMixin
from rest_framework.views import APIView
import oss2
from bottle import request, route, run, http_date
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from lxml import etree

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class WeChat:
    '''
    企业微信发送应用普通消息
    '''

    def __init__(self):
        self.CORPID = 'wwaa5e1adc141fc4e4'  # 企业ID，在管理后台获取
        # 自建应用的Secret，每个自建应用里都有单独的secret
        self.CORPSECRET = 'bUGrb2L48lJ-41COkWg9HKLVM0jNFvWEb1VnLiMBz5w'
        self.AGENTID = '1000040'  # 应用ID，在后台应用中获取

    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def get_access_token(self):
        try:
            with open('./access_token.conf', 'r') as f:
                t, access_token = f.read().split()
        except:
            with open('./access_token.conf', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7260:
                return access_token
            else:
                with open('./access_token.conf', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    # 发送消息
    def send_data(self, message, name):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + \
                   self.get_access_token()
        send_values = {
            "touser": name,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
            },
            "safe": "0"
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        return respone["errmsg"]


select__date = ''


class Wx_Shenpi:
    '''
    企业微信审批
    '''

    def __init__(self):
        self.CORPID = 'wwaa5e1adc141fc4e4'  # 企业ID，在管理后台获取
        # 自建应用的Secret，每个自建应用里都有单独的secret
        self.CORPSECRET = 'bUGrb2L48lJ-41COkWg9HKLVM0jNFvWEb1VnLiMBz5w'
        self.AGENTID = '1000040'  # 应用ID，在后台应用中获取

    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def get_access_token(self):
        try:
            with open('./access_token.conf', 'r') as f:
                t, access_token = f.read().split()
        except:
            with open('./access_token.conf', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7260:
                return access_token
            else:
                with open('./access_token.conf', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    def send_data_renwu(self, shop_name, project, username, submit_time, time, edit, admin_username, to_do_id):
        '''
        销售任务审核
        '''
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + \
                   self.get_access_token()
        send_values = {
            "touser": admin_username,
            "msgtype": "taskcard",
            "agentid": self.AGENTID,
            "taskcard": {
                "title": "" + username + "的任务审核",
                "description":
                    '<div class=\"gray\">' + str(datetime.date.today()) + '</div> '
                    '<div class=\"highlight\">店名：' + shop_name + '</div>'
                    '<div class=\"highlight\">任务：' + project + '</div>'
                    '<div class=\"highlight\">销售：' + username + '</div>'
                    '<div class=\"highlight\">提交时间：' + submit_time + '</div>'
                    '<div class=\"highlight\">最晚完成时间：' + str(time) + '</div>'
                    '<div class=\"highlight\">备注：' + str(edit) + '</div>',
                "task_id": "" + str(to_do_id) + "",  # 更换为订单号
                "btn": [
                    {
                        "key": "yipizhun_todo",
                        "name": "批准",
                        "replace_name": "已批准",
                        "color": "green",
                        "is_bold": True
                    },
                    {
                        "key": "yibohui_todo",
                        "name": "驳回",
                        "color": "red",
                        "replace_name": "已驳回"
                    }
                ]
            },
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        return respone["errmsg"]

    # 订单审核
    def send_data(self, username, order_contract_sales, tags, sign_contract_shop, city, order_numbers,
                  shop_cooperation_duration, order_amount, fangshi, contract_id, dialogImageUrl):
        '''
        销售订单审核
        '''
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + \
                   self.get_access_token()
        send_values = {
            "touser": username,
            "msgtype": "taskcard",
            "agentid": self.AGENTID,
            "taskcard": {
                "title": "" + order_contract_sales + "的订单审核",
                "description":
                    '<div class=\"gray\">' + str(datetime.date.today()) + '</div> '
                    '<div class=\"highlight\">销售：' + order_contract_sales + '</div>'
                    '<div class=\"highlight\">新签 / 续约：' + tags + '</div>'
                                                                                                                                                                                 '<div class=\"highlight\">店名：' + sign_contract_shop + '</div>'
                                                                                                                                                                                                                                     '<div class=\"highlight\">城市：' + city + '</div>'
                                                                                                                                                                                                                                                                             '<div class=\"highlight\">店数：' + str(
                        order_numbers) + '</div>'
                                         '<div class=\"highlight\">时长：' + str(shop_cooperation_duration) + '个月</div>'
                   '<div class=\"highlight\">金额：' + str(
                        order_amount) + '</div>'
                                        '<div class=\"highlight\">支付方式：' + fangshi + '</div>',
                "task_id": "" + str(contract_id) + "",  # 更换为订单号
                "btn": [
                    {
                        "key": "yipizhun",
                        "name": "批准",
                        "replace_name": "已批准",
                        "color": "green",
                        "is_bold": True
                    },
                    {
                        "key": "yibohui",
                        "name": "驳回",
                        "color": "red",
                        "replace_name": "已驳回"
                    }
                ]
            },
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        # 获取发送地址
        send_url_img = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=' + self.get_access_token() + '&type=file'
        # 拿到文件名
        dialogImageUrl = re.findall("http://152.32.135.62/media/(.*)", dialogImageUrl)[0]
        # 获取文件
        wx = WeChat()
        data_img = {'meida': open('/home/beiaikeji_admin/rock/media/' + dialogImageUrl, 'rb')}
        # 发送请求
        r_img = requests.post(url=send_url_img, files=data_img)
        wx.send_data(r_img.text, 'gaoxiaofan')
        dict_data = r_img.json()
        # 拿到图片id
        img_id = dict_data['media_id']
        '''
            发送图片
        '''
        img_data = {
            "touser": username,
            "msgtype": "image",
            "agentid": self.AGENTID,
            "image": {
                "media_id": img_id
            },
            "safe": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        send_msges_img = (bytes(json.dumps(img_data), 'utf-8'))
        respone_img = requests.post(send_url, send_msges_img)
        return respone["errmsg"]

    # 发送图片
    def send_img(self, dialogImageUrl, username):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + \
                   self.get_access_token()
        send_url_img = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=' + self.get_access_token() + '&type=file'
        # 拿到文件名
        dialogImageUrl = re.findall("http://152.32.135.62/media/(.*)", dialogImageUrl)[0]
        # 获取文件
        wx = WeChat()
        # /home/beiaikeji_admin/rock/media/
        data_img = {'meida': open('/home/beiaikeji_admin/rock/media/' + dialogImageUrl, 'rb')}
        # 发送请求
        r_img = requests.post(url=send_url_img, files=data_img)
        # wx.send_data(r_img.text,'gaoxiaofan')
        dict_data = r_img.json()
        # 拿到图片id
        img_id = dict_data['media_id']
        '''
            发送图片
        '''
        img_data = {
            "touser": username,
            "msgtype": "image",
            "agentid": self.AGENTID,
            "image": {
                "media_id": img_id
            },
            "safe": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        send_msges_img = (bytes(json.dumps(img_data), 'utf-8'))
        respone_img = requests.post(send_url, send_msges_img)
        return 1

    def send_data_tuikuan(self, order_date_before, order_date_after, order_start_date_before, order_start_date_after,
                          shop_cooperation_duration_before, shop_cooperation_duration_after, order_amount_before,
                          order_amount_after, cost_fees_before, cost_fees_after, id, order_contract_sales,
                          order_end_date, sign_contract_shop, tags, username, shop_name, order_id, admin_username):
        '''
        退单申请审核
        '''
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + \
                   self.get_access_token()
        send_values = {
            "touser": admin_username,
            "msgtype": "taskcard",
            "agentid": self.AGENTID,
            "taskcard": {
                "title": "" + shop_name + "订单修改",
                "description":
                    '<div class=\"gray\">' + str(datetime.date.today()) + '</div> '
                                                                          '<div class=\"highlight\">店名：' + shop_name + '</div>'
                                                                                                                       '<div class=\"highlight\">下单日期：' + order_date_before + '日' + '>>>>>' + order_date_after + '日' + '</div>'
                                                                                                                                                                                                                       '<div class=\"highlight\">开始日期：' + order_start_date_before + '日' + '>>>>>' + order_start_date_after + '日' + '</div>'
                                                                                                                                                                                                                                                                                                                                   '<div class=\"highlight\">合作时长：' + str(
                        shop_cooperation_duration_before) + '个月' + '>>>>>' + str(
                        shop_cooperation_duration_after) + '个月' + '</div>'
                                                                  '<div class=\"highlight\">签单金额：' + str(
                        order_amount_before) + '元' + '>>>>>' + str(order_amount_after) + '元' + '</div>'
                                                                                               '<div class=\"highlight\">成本费用：' + str(
                        cost_fees_before) + '元' + '>>>>>' + str(cost_fees_after) + '元' + '</div>',
                "task_id": "" + str(order_id) + 'lll' + str(id) + "",  # 更换为订单号
                "btn": [
                    {
                        "key": "yipizhun_tuikuan",
                        "name": "批准",
                        "replace_name": "已批准",
                        "color": "green",
                        "is_bold": True
                    },
                    {
                        "key": "yibohui_tuikuan",
                        "name": "驳回",
                        "color": "red",
                        "replace_name": "已驳回"
                    }
                ]
            },
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        return respone["errmsg"]


# 订单审核审批通过后触发，创建订单
shop_form = ''


class Order_Order:

    def __init__(self):
        self.a = ''

    def Create_Order(self, contract_id, order_date, sign_contract_shop, order_start_date, customer_source,
                     contract_status, contracted_projects, shop_industry, shop_kp_name, shop_telephonenumber,
                     order_numbers, cost_fees, shop_cooperation_duration, order_end_date, order_amount, payment_method,
                     order_contract_sales, shop_remark, shop_id, city, tags):
        order_start_date = str(order_start_date)
        shop_add_form = shop_form
        shop_id_id = shop_id
        count = models.Order.objects.filter(contract_id=contract_id).count()
        if count == 0:
            try:
                order_start_date_year = int(order_start_date[0:4])
                order_start_date_month = int(order_start_date[5:7])
                if '0' == order_start_date[5:6]:
                    order_start_date_month = int(order_start_date[6:7])
                order_start_date_day = int(order_start_date[8:10])
                order_start_date = datetime.date(order_start_date_year,
                                                 order_start_date_month,
                                                 order_start_date_day)

                order_date_year = int(order_date[0:4])
                order_date_month = int(order_date[5:7])
                if '0' == order_date[5:6]:
                    order_date_month = int(order_date[6:7])
                order_date_day = int(order_date[8:10])
                if '0' == order_date[8:9]:
                    order_date_day = int(order_date[9:10])
                order_date = datetime.date(order_date_year, order_date_month,
                                           order_date_day)

                shop_add = models.Order.objects.create(
                    shop_id=shop_id,
                    contract_id=contract_id,
                    order_date=str(order_date + datetime.timedelta(days=1))[0:10],
                    date=str(order_date + datetime.timedelta(days=1))[0:7],
                    order_start_date=str(order_start_date + datetime.timedelta(days=1))[0:10],
                    customer_source=customer_source,
                    sign_contract_shop=sign_contract_shop,
                    contract_status=contract_status,
                    contracted_projects=contracted_projects,
                    shop_industry=shop_industry,
                    shop_kp_name=shop_kp_name,
                    cost_fees=cost_fees,
                    order_numbers=order_numbers,
                    shop_telephonenumber=shop_telephonenumber,
                    shop_cooperation_duration=shop_cooperation_duration,
                    order_end_date=str(order_end_date)[0:10],
                    order_amount=order_amount,
                    payment_method=payment_method,
                    order_contract_sales=order_contract_sales,
                    shop_remark=shop_remark,
                    order_form=[{"value": "收钱吧", "label": "付款方式", "type": "选择下拉框", "index": "付款方式"}, {
                        "value": "点评套餐", "label": "签约项目", "type": "选择下拉框", "index": "签约项目"}],
                    order_commission=int(order_amount) * 0.15,

                    city=city,
                    tags=tags)
                data = datetime.date.today()
                a = models.Dazhongdianping_liren_user_data.objects.filter(
                    shop_id=shop_id)
                edit_data = ''
                for i in a:
                    edit_data = i.shop_edit
                if shop_remark == '' or shop_remark == None:
                    print('')
                else:
                    models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_id=shop_id).update(shop_edit=edit_data + '修改人:' +
                                                          order_contract_sales + '，时间:' + str(data) +
                                                          '，内容:' + shop_remark + '￥')

                if shop_add != '':
                    create = models.Dazhongdianping_liren_user_data.objects.filter(shop_id=shop_id)
                    tag_data = models.Order.objects.filter(shop_id=shop_id)
                    if len(tag_data) > 1:
                        tag = '续约'
                    for c in create:
                        models.Dazhongdianping_liren_all_data.objects.create(
                            shop_id=c.shop_id,
                            shop_name=c.shop_name,
                            shop_start=c.shop_start,
                            shop_review_count=c.shop_review_count,
                            shop_bad_review=c.shop_bad_review,
                            shop_per_capita_consumption=c.shop_per_capita_consumption,
                            shop_effect=c.shop_effect,
                            shop_service=c.shop_service,
                            shop_surroundings=c.shop_surroundings,
                            shop_address=c.shop_address,
                            shop_telephonenumber=c.shop_telephonenumber,
                            shop_business_district=c.shop_business_district,
                            shop_category=c.shop_category,
                            shop_region=c.shop_region,
                            shop_tags=tags,
                            shop_edit=c.shop_edit,
                            shop_kp_name=c.shop_kp_name,
                            shop_kp_position=c.shop_kp_position,
                            shop_kp_wechat_id=c.shop_kp_wechat_id,
                            shop_kp_city=c.shop_kp_city,
                            shop_city=c.shop_city,
                            shop_kp_category='',
                            shop_add_form=c.shop_add_form)
                        models.Dazhongdianping_liren_user_data.objects.filter(
                            shop_id=c.shop_id).delete()
                    problems = models.Setting_storage.objects.all()
                    now_date = datetime.date.today()
                    first = now_date.replace(day=1)
                    last_month = str(now_date)
                    performance = 0
                    commission_point = 0
                    performance_data = models.Order.objects.filter(
                        order_contract_sales=order_contract_sales)
                    for i in performance_data:
                        if str(last_month)[0:7] == i.order_date[0:7]:
                            performance += int(i.order_amount)
                    commission_point_data = models.Setting_storage.objects.all()
                    commission_point_json = ''
                    for c in commission_point_data:
                        commission_point_json = c.commission_form
                    count = []
                    for o in eval(commission_point_json):
                        count.append(int(o['commission_performance']))
                    for a in sorted(count):
                        if performance >= a:
                            for o in eval(commission_point_json):
                                if a == int(o['commission_performance']):
                                    commission_point = int(
                                        o['commission_commission_point'])
                        else:
                            performance = 0
                    date_time = str(order_start_date)
                    year = int(date_time[0:4])
                    month = int(date_time[5:7])
                    if '0' == date_time[5:6]:
                        month = int(str(date_time[6:7]))
                    day = int(date_time[8:10])
                    if '0' == date_time[8:9]:
                        day = int(date_time[9:10])
                    js = 0
                    date = datetime.date(year, month, day)
                    data = ''
                    for i in problems:
                        data = i.todo_form
                    total_number_of_tasks = 0  # 任务总数
                    # 计算任务总数
                    for at in range(0, len(eval(data))):
                        if eval(data)[at]['select'] == '单次任务':
                            total_number_of_tasks = total_number_of_tasks + 1
                        elif eval(data)[at]['select'] == '重复任务':
                            frequency = eval(data)[at]['time']  # 获取重复任务的频率
                            start_date = order_start_date
                            end_date = order_end_date
                            # 开始的时间
                            date_time = str(order_start_date)
                            year = int(date_time[0:4])
                            month = int(date_time[5:7])
                            if '0' == str(date_time[5:6]):
                                month = int(str(date_time[6:7]))
                            day = int(date_time[8:10])
                            if '0' == str(date_time[8:9]):
                                day = int(str(date_time[9:10]))
                            cur_day = datetime.date(
                                int(year), int(month), int(day))
                            # 结束的时间
                            date_time_end = order_end_date
                            year_end = int(date_time_end[0:4])
                            month_end = int(date_time_end[5:7])
                            if '0' == str(date_time_end[5:6]):
                                month_end = int(str(date_time_end[6:7]))
                            day_end = int(date_time_end[8:10])
                            if '0' == str(date_time_end[8:9]):
                                day_end = int(str(date_time_end[9:10]))
                            # 订单开始的时间
                            cur_day = datetime.date(
                                int(year), int(month), int(day))
                            # 订单结束的时间
                            next_day = datetime.date(int(year_end), int(month_end),
                                                     int(day_end))
                            # 　两个日期之间的差值
                            difference = int((next_day - cur_day).days)
                            count = int(difference) / int(frequency)
                            count = round(count)
                            total_number_of_tasks = total_number_of_tasks + count
                    money = int(order_amount) * \
                            (int(commission_point) / 100) * (1 / 3)
                    money = money * 2

                    data = ''
                    for i in problems:
                        data = i.todo_form
                    # 分配任务以及金额
                    for a in range(0, len(eval(data))):
                        if eval(data)[a]['select'] == '单次任务':
                            models.To_do.objects.create(
                                project=eval(data)[a]['name'],
                                shop_name=sign_contract_shop,
                                order_id=contract_id,
                                # 开始日期加上任务的时间
                                time=date + \
                                     datetime.timedelta(
                                         days=int(eval(data)[a]['time'])),
                                money=round(money / total_number_of_tasks),
                                schedule=0,
                                username=order_contract_sales,
                                status='未审核')
                        elif eval(data)[a]['select'] == '重复任务':
                            # 重复频率
                            frequency = eval(data)[a]['time']  # 获取重复任务的频率
                            start_date = order_start_date
                            end_date = order_end_date
                            # 开始的时间
                            date_time = str(order_start_date)
                            year = int(date_time[0:4])
                            month = int(date_time[5:7])
                            if '0' == str(date_time[5:6]):
                                month = int(str(date_time[6:7]))
                            day = int(date_time[8:10])
                            if '0' == str(date_time[8:9]):
                                day = int(str(date_time[9:10]))
                            cur_day = datetime.date(year, month, day)
                            # 结束的时间
                            date_time_end = order_end_date
                            year_end = int(date_time_end[0:4])
                            month_end = int(date_time_end[5:7])
                            if '0' == str(date_time_end[5:6]):
                                month_end = int(str(date_time_end[6:7]))
                            day_end = int(date_time_end[8:10])
                            if '0' == str(date_time_end[8:9]):
                                day_end = int(str(date_time_end[9:10]))
                            # 订单开始的时间
                            cur_day = datetime.date(year, month, day)
                            # 订单结束的时间
                            next_day = datetime.date(
                                int(year_end), int(month_end), int(day_end))
                            # 　两个日期之间的差值
                            difference = int((next_day - cur_day).days)
                            count = int(difference) / int(frequency)
                            count = round(count)
                            original_time = cur_day
                            for b in range(0, count):
                                models.To_do.objects.create(
                                    project='第' + str(b + 1) + '次' +
                                            eval(data)[a]['name'],
                                    shop_name=sign_contract_shop,
                                    order_id=contract_id,
                                    time=original_time + datetime.timedelta(days=int(
                                        eval(data)[a]['time'])),  # 开始日期加上任务的时间
                                    money=round(money / total_number_of_tasks),
                                    schedule=0,
                                    username=order_contract_sales,
                                    status='未审核')
                                original_time = original_time + \
                                                datetime.timedelta(
                                                    days=int(eval(data)[a]['time']))

                    db = pymysql.connect(
                        "localhost", "root", "bakj123456", "rock")
                    cursor = db.cursor()
                    cursor.execute(
                        "SELECT * FROM user_userprofile where first_name = '" + order_contract_sales + "'")
                    data = cursor.fetchall()
                    group = data[0][14]  # 销售组
                    name = data[0][4]  # 签约人
                    cursor2 = db.cursor()
                    cursor2.execute(
                        "SELECT * FROM user_userprofile where group_name = '" + group + "' and avatar='admin'")
                    data2 = cursor2.fetchall()
                    wx = WeChat()
                    wx.send_data(
                        '订单审核通过\n'
                        '小组：' + group + '\n'
                                        '销售：' + order_contract_sales + '\n'
                                                                       '新签/续约：' + tags + '\n'
                                                                                         '店名：' + sign_contract_shop + '\n'
                                                                                                                      '城市：' + city + '\n'
                                                                                                                                     '店数：' + str(
                            order_numbers) + '\n'
                                             '时长：' + str(shop_cooperation_duration) + '个月\n'
                                                                                      '金额：' + str(order_amount) + '\n',
                        name)
                    headers = {'Content-Type': 'text/plain'}
                    print(type(order_start_date))
                    order_start_date2 = str(order_start_date)
                    print(type(order_start_date2))
                    data = {
                        "msgtype": "markdown",
                        "markdown": {
                            "content":
                                "💫北爱“" + order_contract_sales + "”战报来袭 💫\n"
                                "小组：<font color=\"red\">" + group + "</font>\n"
                                "销售：<font color=\"red\">" + order_contract_sales + "</font>\n"
                                "新签/续约：<font color=\"red\">" + tags + "</font>\n"
                                "店名：<font color=\"red\">" + sign_contract_shop + "</font>\n"
                                "城市：<font color=\"red\">" + city + "</font>\n"
                                "店数：<font color=\"red\">" +str(order_numbers) + "</font>\n"
                                "时长：<font color=\"red\">" +str(shop_cooperation_duration) + "个月</font>\n"
                                "金额：<font color=\"red\">" +str(order_amount) + "元</font>\n"
                                # "支付方式：<font color=\"blue\">" + fangshi + "</font>\n"
                                "签约时间：<font color=\"red\">" + str(order_date) + "</font>\n"
                                "开始时间：<font color=\"red\">" + str(order_start_date2) + "</font>\n"
                                "厉害牛牛牛！！加油加油加👍🏻👍🏻🌹🌹以上签收同步赞赞赞👍👍👍使命必达🎉🎉🎉\n"
                        }
                    }
                    requests.post(
                        url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=91ce23c7-be03-47d3-a5e8-def2937fdc30',
                        json=data, headers=headers)
                    models.Shenhe_order.objects.filter(shop_id=shop_id_id).delete()
            except Exception as e:
                models.Order.objects.filter(contract_id=contract_id).delete()
                resultdict = {}
                resultdict['code'] = 0
                resultdict['msg'] = e
                resultdict['state'] = 1
                return JsonResponse(resultdict, safe=False)


def getMonthRangList(start_month, end_month):
    """
    从开始日期到结束日期查询存在的月份列表，除去本月的数据
    """
    print()
    start_time = datetime.datetime.strptime(start_month, "%Y-%m")
    end_time = datetime.datetime.strptime(end_month, "%Y-%m")
    month_count = rrule.rrule(rrule.MONTHLY, dtstart=start_time, until=end_time).count()
    now_month = datetime.datetime.strptime(str(datetime.datetime.now())[:7], "%Y-%m")
    if start_time == now_month == end_time:
        return []
    else:
        month_list = []
        for x in range(month_count):
            year, month = [int(y) for y in str(start_time)[:7].split("-")]
            month = month + x
            if month > 12:
                year += 1
                month -= 12
            elif month < 1:
                year -= 1
                month += 12
            year, month = str(year), str(month)
            if len(month) == 1:
                month = "0" + month
            month_list.append(year + "-" + month)
        return month_list


@csrf_exempt
def weixin(request):
    """
    企业微信卡片任务审核之后触发
    """
    wx = WeChat()
    sCorpID = "wwaa5e1adc141fc4e4"
    sToken = 'u8zsAacLJanxVM'
    sEncodingAESKey = "y0v5tRTEPCXRUnFLt8meewyHz8IOFdvntYmvxKd09XC"
    wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
    if request.method == "POST":
        sReqMsgSig = request.GET.get('msg_signature')
        sReqTimeStamp = request.GET.get('timestamp')
        sReqNonce = request.GET.get('nonce')
        sReqData = request.body
        wx.send_data(sReqData.decode(), 'gaoxiaofan')
        ret, sMsg = wxcpt.DecryptMsg(
            sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
        if (ret != 0):
            sys.exit(1)
        a = str(sMsg)
        b = str(sMsg)
        shenpi_str = re.findall("<EventKey><!(.*?)></EventKey>", a)[0]
        shenpi_data = shenpi_str.strip('[CDATA[]]')
        order_str = re.findall("<TaskId><!(.*?)></TaskId>", b)[0]
        order_data = order_str.strip('[CDATA[]]')
        wx_wx_wx_wx = WeChat()
        wx_wx_wx_wx.send_data(shenpi_data, 'gaoxiaofan')
        wx_wx_wx_wx.send_data(order_data, 'gaoxiaofan')
        if shenpi_data == 'yibohui':
            order = models.Shenhe_order.objects.filter(contract_id=order_data)
            for p in order:
                db = pymysql.connect("localhost", "root", "bakj123456", "rock")
                cursor = db.cursor()
                cursor.execute(
                    "SELECT * FROM user_userprofile where first_name = '" + p.order_contract_sales + "'")
                data = cursor.fetchall()
                name = data[0][4]
                group = data[0][14]
                fangshi = ''
                for i in eval(p.order_form):
                    if i['label'] == '付款方式':
                        fangshi = i['value']
                wx_wx = WeChat()
                wx_wx.send_data('订单审核失败\n'
                                '失败原因：''\n'
                                '--------------------\n'
                                '小组：' + group + '\n'
                                '销售：' + p.order_contract_sales + '\n'
                                '新签/续约：' + p.tags + '\n'
                                '店名：' + p.sign_contract_shop + '\n'
                                '城市：' + p.city + '\n'
                                '店数：' + str(p.order_numbers) + '\n'
                                '时长：' +str(p.shop_cooperation_duration) + '个月\n'
                                '金额：' + str(p.order_amount) + '\n'
                                '支付方式：' + fangshi + '\n',
                                name)
                models.Shenhe_order.objects.filter(contract_id=order_data).delete()
        if shenpi_data == 'yipizhun':
            order = models.Shenhe_order.objects.filter(contract_id=order_data)
            for p in order:
                contract_id = p.contract_id
                order_date = p.order_date
                sign_contract_shop = p.sign_contract_shop
                order_start_date = p.order_start_date
                customer_source = p.customer_source
                contract_status = p.contract_status
                contracted_projects = p.contracted_projects
                shop_industry = p.shop_industry
                shop_kp_name = p.shop_kp_name
                shop_telephonenumber = p.shop_telephonenumber
                order_numbers = p.order_numbers
                cost_fees = p.cost_fees
                shop_cooperation_duration = p.shop_cooperation_duration
                order_end_date = p.order_end_date
                order_amount = p.order_amount
                payment_method = p.payment_method
                order_contract_sales = p.order_contract_sales
                shop_remark = p.shop_remark
                shop_id = p.shop_id
                tags = p.tags
                city = p.city
                global shop_form
                shop_form = p.order_form,
                wx_wx = WeChat()
                wx_wx.send_data(contract_id, 'gaoxiaofan')
                oo = Order_Order()
                oo.Create_Order(contract_id, order_date, sign_contract_shop, order_start_date, customer_source,
                                contract_status, contracted_projects, shop_industry, shop_kp_name,
                                shop_telephonenumber, order_numbers, cost_fees, shop_cooperation_duration,
                                order_end_date, order_amount, payment_method, order_contract_sales, shop_remark,
                                shop_id, city, tags)
        if shenpi_data == 'yibohui_todo':
            str_todo = 'SELECT * FROM app_pending_review where id=' + str(order_data) + ''
            db2 = pymysql.connect("localhost", "root", "bakj123456", "rock")
            cursor2 = db2.cursor()
            cursor2.execute(str_todo)
            data2 = cursor2.fetchall()
            project = data2[0][1]  # 销售组
            shop_name = data2[0][2]
            time = data2[0][3]
            money = data2[0][4]
            schedule = data2[0][5]
            username = data2[0][6]
            order_id = data2[0][15]
            # edit = data2[0][10]
            success_time = datetime.date.today()
            problems = models.To_do.objects.create(project=project,
                                                   shop_name=shop_name,
                                                   time=time,
                                                   money=money,
                                                   schedule=schedule,
                                                   username=username,
                                                   order_id=order_id,
                                                   edit='',
                                                   status='审核未通过')
            if problems != None:
                models.Pending_review.objects.filter(project=project,
                                                     shop_name=shop_name,
                                                     time=time).delete()
                db = pymysql.connect("localhost", "root", "bakj123456", "rock")
                cursor = db.cursor()
                cursor.execute(
                    "SELECT * FROM user_userprofile where first_name = '" + username + "'")
                data = cursor.fetchall()
                username = data[0][4]
                wx = WeChat()
                wx.send_data('任务审核失败通知\n'
                             '店名：' + shop_name + '\n'
                             '任务名：' + project + '\n'
                             '审核时间：' + str(success_time) + '\n', username)
                resultdict = {}
                resultdict['code'] = 0
                resultdict['msg'] = ""
                resultdict['state'] = 1
                return JsonResponse(resultdict, safe=False)
        if shenpi_data == 'yipizhun_todo':
            db_todo = pymysql.connect("localhost", "root", "bakj123456", "rock")
            cursor_todo = db_todo.cursor()
            str_todo = 'SELECT * FROM app_pending_review where id = ' + str(order_data) + ''
            cursor_todo.execute(str_todo)
            data_todo = cursor_todo.fetchall()
            project = data_todo[0][1]  # 销售组
            shop_name = data_todo[0][2]
            time = data_todo[0][3]
            money = data_todo[0][4]
            schedule = data_todo[0][5]
            username = data_todo[0][6]
            submitter = data_todo[0][7]
            order_id = data_todo[0][15]
            url = data_todo[0][16]
            submit_time = data_todo[0][9]
            success_time = datetime.date.today()
            completed = models.Completed.objects.filter(shop_name=shop_name)
            tp_do = models.To_do.objects.filter(shop_name=shop_name)
            pending_review = models.Pending_review.objects.filter(
                shop_name=shop_name)
            count = len(completed) + len(tp_do) + len(pending_review)
            schedule = int(float(schedule)) + (100 / count)
            problems = models.Completed.objects.create(project=project,
                                                       shop_name=shop_name,
                                                       time=time,
                                                       money=money,
                                                       schedule=int(schedule),
                                                       order_id=order_id,
                                                       username=username,
                                                       submitter=submitter,
                                                       status='已完成',
                                                       submit_time=submit_time,
                                                       url=url,
                                                       success_time=success_time)
            if problems != None:
                print('进入')
                models.Pending_review.objects.filter(project=project,
                                                     shop_name=shop_name,
                                                     time=time).delete()
                models.Completed.objects.filter(shop_name=shop_name).update(
                    schedule=schedule)
                models.To_do.objects.filter(shop_name=shop_name).update(
                    schedule=schedule)
                models.Pending_review.objects.filter(shop_name=shop_name).update(
                    schedule=schedule)
                db = pymysql.connect("localhost", "root", "bakj123456", "rock")
                cursor = db.cursor()
                cursor.execute(
                    "SELECT * FROM user_userprofile where first_name = '" + username + "'")
                data = cursor.fetchall()
                username = data[0][4]
                wx = WeChat()
                wx.send_data('任务审核成功通知\n'
                             '店名：' + shop_name + '\n'
                                                 '任务名：' + project + '\n'
                                                                    '审核通过时间：' + str(success_time) + '\n', username)
                resultdict = {}
                resultdict['code'] = 0
                resultdict['msg'] = ""
                resultdict['state'] = 1
                return JsonResponse(resultdict, safe=False)
        if shenpi_data == 'yipizhun_tuikuan':
            order_data = order_data[:order_data.find("lll")]
            wx = WeChat()
            wx.send_data(order_data, 'gaoxiaofan')
            db_todo = pymysql.connect("localhost", "root", "bakj123456", "rock")
            cursor_todo = db_todo.cursor()
            str_todo = 'SELECT * FROM app_tuikuan_order where order_id = "' + str(order_data) + '"'
            cursor_todo.execute(str_todo)
            data_todo = cursor_todo.fetchall()
            order_id = data_todo[0][1]
            order_date_before = data_todo[0][2]
            order_date_after = data_todo[0][3]
            order_start_date_before = data_todo[0][4]
            order_start_date_after = data_todo[0][5]
            shop_cooperation_duration_before = data_todo[0][6]
            shop_cooperation_duration_after = data_todo[0][7]
            order_amount_before = data_todo[0][8]
            order_amount_after = data_todo[0][9]
            cost_fees_before = data_todo[0][10]
            cost_fees_after = data_todo[0][11]
            order_contract_sales = data_todo[0][12]
            order_end_date = data_todo[0][13]
            sign_contract_shop = data_todo[0][14]
            tags = data_todo[0][15]
            db = pymysql.connect("localhost", "root", "bakj123456", "rock")
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM user_userprofile where first_name = '" + order_contract_sales + "'")
            data = cursor.fetchall()
            username_yinwen = data[0][4]
            if order_amount_before == order_amount_after and cost_fees_before == cost_fees_after and order_date_before == order_date_after and order_start_date_before == order_start_date_after and shop_cooperation_duration_before == shop_cooperation_duration_after:
                pass
            elif order_amount_before != order_amount_after:
                models.Order.objects.filter(contract_id=order_id).update(order_amount=order_amount_after)
            elif cost_fees_before != cost_fees_after:
                models.Order.objects.filter(contract_id=order_id).update(cost_fees=cost_fees_after)
            elif order_date_before != order_date_after:
                order_start_date_year = int(order_date_after[0:4])
                order_start_date_month = int(order_date_after[5:7])
                if '0' == order_date_after[5:6]:
                    order_start_date_month = int(order_date_after[6:7])
                order_start_date_day = int(order_date_after[8:10])
                if '0' == order_date_after[8:9]:
                    order_start_date_day = int(order_date_after[9:10])
                order_date = datetime.date(order_start_date_year,
                                           order_start_date_month,
                                           order_start_date_day)
                models.Order.objects.filter(contract_id=order_id).update(
                    order_date=order_date + datetime.timedelta(days=1))
            elif order_start_date_before != order_start_date_after:
                problems = models.Setting_storage.objects.all()
                now_date = datetime.date.today()
                first = now_date.replace(day=1)
                last_month = str(now_date)
                performance = 0
                commission_point = 0
                performance_data = models.Order.objects.filter(
                    order_contract_sales=order_contract_sales)
                for i in performance_data:
                    if str(last_month)[0:7] == i.order_date[0:7]:
                        performance += int(i.order_amount)
                commission_point_data = models.Setting_storage.objects.all()
                commission_point_json = ''
                for c in commission_point_data:
                    commission_point_json = c.commission_form
                count = []
                for o in eval(commission_point_json):
                    count.append(int(o['commission_performance']))
                for a in sorted(count):
                    if performance >= a:
                        for o in eval(commission_point_json):
                            if a == int(o['commission_performance']):
                                commission_point = int(
                                    o['commission_commission_point'])
                    else:
                        performance = 0
                date_time = str(order_start_date_after)
                year = int(date_time[0:4])
                month = int(date_time[5:7])
                if '0' == date_time[5:6]:
                    month = int(str(date_time[6:7]))
                day = int(date_time[8:10])
                if '0' == date_time[8:9]:
                    day = int(date_time[9:10])
                js = 0
                date = datetime.date(year, month, day)
                data = ''
                for i in problems:
                    data = i.todo_form
                total_number_of_tasks = 0  # 任务总数
                # 计算任务总数
                for at in range(0, len(eval(data))):
                    if eval(data)[at]['select'] == '单次任务':
                        total_number_of_tasks = total_number_of_tasks + 1
                    elif eval(data)[at]['select'] == '重复任务':
                        frequency = eval(data)[at]['time']  # 获取重复任务的频率
                        start_date = order_start_date_after
                        end_date = order_end_date
                        # 开始的时间
                        date_time = str(order_start_date_after)
                        year = int(date_time[0:4])
                        month = int(date_time[5:7])
                        if '0' == str(date_time[5:6]):
                            month = int(str(date_time[6:7]))
                        day = int(date_time[8:10])
                        if '0' == str(date_time[8:9]):
                            day = int(str(date_time[9:10]))
                        cur_day = datetime.date(
                            int(year), int(month), int(day))
                        # 结束的时间
                        date_time_end = order_end_date
                        year_end = int(date_time_end[0:4])
                        month_end = int(date_time_end[5:7])
                        if '0' == str(date_time_end[5:6]):
                            month_end = int(str(date_time_end[6:7]))
                        day_end = int(date_time_end[8:10])
                        if '0' == str(date_time_end[8:9]):
                            day_end = int(str(date_time_end[9:10]))
                        # 订单开始的时间
                        cur_day = datetime.date(
                            int(year), int(month), int(day))
                        # 订单结束的时间
                        next_day = datetime.date(int(year_end), int(month_end),
                                                 int(day_end))
                        # 　两个日期之间的差值
                        difference = int((next_day - cur_day).days)
                        count = int(difference) / int(frequency)
                        count = round(count)
                        total_number_of_tasks = total_number_of_tasks + count
                money = int(order_amount_after) * \
                        (int(commission_point) / 100) * (1 / 3)
                money = money * 2
                data = ''
                for i in problems:
                    data = i.todo_form
                # 删除任务，重新分配
                models.To_do.objects.filter(order_id=order_id).delete()
                models.Completed.objects.filter(order_id=order_id).delete()
                models.Pending_review.objects.filter(order_id=order_id).delete()
                # 重新分配任务
                for a in range(0, len(eval(data))):
                    if eval(data)[a]['select'] == '单次任务':
                        models.To_do.objects.create(
                            project=eval(data)[a]['name'],
                            shop_name=sign_contract_shop,
                            order_id=order_id,
                            # 开始日期加上任务的时间
                            time=date + \
                                 datetime.timedelta(
                                     days=int(eval(data)[a]['time'])),
                            money=round(money / total_number_of_tasks),
                            schedule=0,
                            username=order_contract_sales,
                            status='未审核')
                    elif eval(data)[a]['select'] == '重复任务':
                        # 重复频率
                        frequency = eval(data)[a]['time']  # 获取重复任务的频率
                        start_date = order_start_date_after
                        end_date = order_end_date
                        # 开始的时间
                        date_time = str(order_start_date_after)
                        year = int(date_time[0:4])
                        month = int(date_time[5:7])
                        if '0' == str(date_time[5:6]):
                            month = int(str(date_time[6:7]))
                        day = int(date_time[8:10])
                        if '0' == str(date_time[8:9]):
                            day = int(str(date_time[9:10]))
                        cur_day = datetime.date(year, month, day)
                        # 结束的时间
                        date_time_end = order_end_date
                        year_end = int(date_time_end[0:4])
                        month_end = int(date_time_end[5:7])
                        if '0' == str(date_time_end[5:6]):
                            month_end = int(str(date_time_end[6:7]))
                        day_end = int(date_time_end[8:10])
                        if '0' == str(date_time_end[8:9]):
                            day_end = int(str(date_time_end[9:10]))
                        # 订单开始的时间
                        cur_day = datetime.date(year, month, day)
                        # 订单结束的时间
                        print('day_end', day_end)
                        next_day = datetime.date(
                            int(year_end), int(month_end), int(day_end))
                        # 　两个日期之间的差值
                        difference = int((next_day - cur_day).days)
                        count = int(difference) / int(frequency)
                        count = round(count)
                        original_time = cur_day
                        for b in range(0, count):
                            print('创建')
                            models.To_do.objects.create(
                                project='第' + str(b + 1) + '次' +
                                        eval(data)[a]['name'],
                                shop_name=sign_contract_shop,
                                order_id=order_id,
                                time=original_time + datetime.timedelta(days=int(
                                    eval(data)[a]['time'])),  # 开始日期加上任务的时间
                                money=round(money / total_number_of_tasks),
                                schedule=0,
                                username=order_contract_sales,
                                status='未审核')
                            original_time = original_time + \
                                            datetime.timedelta(
                                                days=int(eval(data)[a]['time']))
                order_start_date_year = int(order_start_date_after[0:4])
                order_start_date_month = int(order_start_date_after[5:7])
                if '0' == order_start_date_after[5:6]:
                    order_start_date_month = int(order_start_date_after[6:7])
                order_start_date_day = int(order_start_date_after[8:10])
                if '0' == order_start_date_after[8:9]:
                    order_start_date_day = int(order_start_date_after[9:10])
                order_start_date = datetime.date(order_start_date_year,
                                                 order_start_date_month,
                                                 order_start_date_day)
                models.Order.objects.filter(contract_id=order_id).update(
                    order_start_date=order_start_date + datetime.timedelta(days=1), order_end_date=order_end_date, )
            elif shop_cooperation_duration_before != shop_cooperation_duration_after:
                problems = models.Setting_storage.objects.all()
                now_date = datetime.date.today()
                first = now_date.replace(day=1)
                last_month = str(now_date)
                performance = 0
                commission_point = 0
                performance_data = models.Order.objects.filter(
                    order_contract_sales=order_contract_sales)
                for i in performance_data:
                    if str(last_month)[0:7] == i.order_date[0:7]:
                        performance += int(i.order_amount)
                commission_point_data = models.Setting_storage.objects.all()
                commission_point_json = ''
                for c in commission_point_data:
                    commission_point_json = c.commission_form
                count = []
                for o in eval(commission_point_json):
                    count.append(int(o['commission_performance']))
                for a in sorted(count):
                    if performance >= a:
                        for o in eval(commission_point_json):
                            if a == int(o['commission_performance']):
                                commission_point = int(
                                    o['commission_commission_point'])
                    else:
                        performance = 0
                date_time = str(order_start_date_after)
                year = int(date_time[0:4])
                month = int(date_time[5:7])
                if '0' == date_time[5:6]:
                    month = int(str(date_time[6:7]))
                day = int(date_time[8:10])
                if '0' == date_time[8:9]:
                    day = int(date_time[9:10])
                js = 0
                date = datetime.date(year, month, day)
                data = ''
                for i in problems:
                    data = i.todo_form
                total_number_of_tasks = 0  # 任务总数
                # 计算任务总数
                for at in range(0, len(eval(data))):
                    if eval(data)[at]['select'] == '单次任务':
                        total_number_of_tasks = total_number_of_tasks + 1
                    elif eval(data)[at]['select'] == '重复任务':
                        frequency = eval(data)[at]['time']  # 获取重复任务的频率
                        start_date = order_start_date_after
                        end_date = order_end_date
                        # 开始的时间
                        date_time = str(order_start_date_after)
                        year = int(date_time[0:4])
                        month = int(date_time[5:7])
                        if '0' == str(date_time[5:6]):
                            month = int(str(date_time[6:7]))
                        day = int(date_time[8:10])
                        if '0' == str(date_time[8:9]):
                            day = int(str(date_time[9:10]))
                        cur_day = datetime.date(
                            int(year), int(month), int(day))
                        # 结束的时间
                        date_time_end = order_end_date
                        year_end = int(date_time_end[0:4])
                        month_end = int(date_time_end[5:7])
                        if '0' == str(date_time_end[5:6]):
                            month_end = int(str(date_time_end[6:7]))
                        day_end = int(date_time_end[8:10])
                        if '0' == str(date_time_end[8:9]):
                            day_end = int(str(date_time_end[9:10]))
                        # 订单开始的时间
                        cur_day = datetime.date(
                            int(year), int(month), int(day))
                        # 订单结束的时间
                        next_day = datetime.date(int(year_end), int(month_end),
                                                 int(day_end))
                        # 　两个日期之间的差值
                        difference = int((next_day - cur_day).days)
                        count = int(difference) / int(frequency)
                        count = round(count)
                        total_number_of_tasks = total_number_of_tasks + count
                money = int(order_amount_after) * \
                        (int(commission_point) / 100) * (1 / 3)
                money = money * 2
                print('提成点', money)
                wx.send_data(total_number_of_tasks, 'gaoxiaofan')
                print('任务总数', total_number_of_tasks)
                data = ''
                # 获得任务
                for i in problems:
                    data = i.todo_form
                # 分配任务以及金额
                models.To_do.objects.filter(order_id=order_id).delete()
                models.Completed.objects.filter(order_id=order_id).delete()
                models.Pending_review.objects.filter(order_id=order_id).delete()
                for a in range(0, len(eval(data))):
                    if eval(data)[a]['select'] == '单次任务':
                        models.To_do.objects.create(
                            project=eval(data)[a]['name'],
                            shop_name=sign_contract_shop,
                            order_id=order_id,
                            # 开始日期加上任务的时间
                            time=date + \
                                 datetime.timedelta(
                                     days=int(eval(data)[a]['time'])),
                            money=round(money / total_number_of_tasks),
                            schedule=0,
                            username=order_contract_sales,
                            status='未审核')
                    elif eval(data)[a]['select'] == '重复任务':
                        # 重复频率
                        frequency = eval(data)[a]['time']  # 获取重复任务的频率
                        start_date = order_start_date_after
                        end_date = order_end_date
                        # 开始的时间
                        date_time = str(order_start_date_after)
                        year = int(date_time[0:4])
                        month = int(date_time[5:7])
                        if '0' == str(date_time[5:6]):
                            month = int(str(date_time[6:7]))
                        day = int(date_time[8:10])
                        if '0' == str(date_time[8:9]):
                            day = int(str(date_time[9:10]))
                        cur_day = datetime.date(year, month, day)
                        # 结束的时间
                        date_time_end = order_end_date
                        year_end = int(date_time_end[0:4])
                        month_end = int(date_time_end[5:7])
                        if '0' == str(date_time_end[5:6]):
                            month_end = int(str(date_time_end[6:7]))
                        day_end = int(date_time_end[8:10])
                        if '0' == str(date_time_end[8:9]):
                            day_end = int(str(date_time_end[9:10]))
                        # 订单开始的时间
                        cur_day = datetime.date(year, month, day)
                        # 订单结束的时间
                        next_day = datetime.date(
                            int(year_end), int(month_end), int(day_end))
                        # 　两个日期之间的差值
                        difference = int((next_day - cur_day).days)
                        count = int(difference) / int(frequency)
                        count = round(count)
                        original_time = cur_day
                        for b in range(0, count):
                            models.To_do.objects.create(
                                project='第' + str(b + 1) + '次' +
                                        eval(data)[a]['name'],
                                shop_name=sign_contract_shop,
                                order_id=order_id,
                                time=original_time + datetime.timedelta(days=int(
                                    eval(data)[a]['time'])),  # 开始日期加上任务的时间
                                money=round(money / total_number_of_tasks),
                                schedule=0,
                                username=order_contract_sales,
                                status='未审核')
                            original_time = original_time + datetime.timedelta(days=int(eval(data)[a]['time']))
                wx.send_data('时间' + str(shop_cooperation_duration_after), 'gaoxiaofan')
                models.Tuikuan_Order.objects.filter(order_id=order_id).delete()
                models.Order.objects.filter(contract_id=order_id).update(
                    shop_cooperation_duration=shop_cooperation_duration_after, order_end_date=order_end_date, tags=tags)
                order_start_date_year = int(order_start_date_after[0:4])

                order_start_date_month = int(order_start_date_after[5:7])

                if '0' == order_start_date_after[5:6]:
                    order_start_date_month = int(order_start_date_after[6:7])
                order_start_date_day = int(order_start_date_after[8:10])

                if '0' == order_start_date_after[8:9]:
                    order_start_date_day = int(order_start_date_after[9:10])
                # 更新时间
                order_start_date = datetime.date(order_start_date_year, order_start_date_month, order_start_date_day)
                # 更新订单
            models.Tuikuan_Order.objects.filter(order_id=order_data).delete()
            wx.send_data('订单修改审核成功通知\n'
                         '店名：' + sign_contract_shop + '\n', username_yinwen)
            order = models.Order.objects.filter(contract_id=order_data)
            data = datetime.date.today()
            for i in order:
                models.Dazhongdianping_liren_user_data.objects.filter(
                    shop_id=i.shop_id).update(shop_edit='修改人:' +
                                                        i.order_contract_sales + '，时间:' + str(data) +
                                                        '，内容:' + '修改了订单' + '￥')

        if shenpi_data == 'yibohui_tuikuan':
            order_data = order_data[:order_data.find("lll")]
            db_todo = pymysql.connect("localhost", "root", "bakj123456", "rock")
            cursor_todo = db_todo.cursor()
            str_todo = 'SELECT * FROM app_tuikuan_order where order_id = "' + str(order_data) + '"'
            cursor_todo.execute(str_todo)
            data_todo = cursor_todo.fetchall()
            order_id = data_todo[0][1]
            models.Tuikuan_Order.objects.filter(order_id=order_data).delete()
            wx.send_data('订单修改审核失败通知\n'
                         '店名：' + sign_contract_shop + '\n', username_yinwen)
    else:
        signature = request.GET.get('msg_signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')
        try:
            ret, sEchoStr = wxcpt.VerifyURL(
                signature, timestamp, nonce, echo_str)
            if (ret != 0):
                print("ERR: VerifyURL ret: " + str(ret))
        except InvalidSignatureException:
            return HttpResponse("Weixin-NO")
        response = HttpResponse(sEchoStr, content_type="text/plain")
        return response


def test(request):
    wx = WeChat()
    wx.send_data('123', 'gaoxiaofan')
    resultdict = {}
    resultdict['code'] = 0
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def img_test(request):
    if request.method == "POST":
        fileDict = request.FILES.items()
        pic = request.FILES['image']
        pic_name = pic.name  # 上传文件名
        save_path = os.path.join(BASE_DIR, 'media', pic_name)
        with open(save_path, 'wb') as f:
            for content in pic.chunks():
                f.write(content)
        return HttpResponse(pic_name)


@csrf_exempt
def last_day_of_month(any_day):
    """
    获取获得一个月中的最后一天
    :param any_day: 任意日期
    :return: string
    """
    next_month = any_day.replace(day=28) + datetime.timedelta(
        days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)


def save_shouye_data(request):
    data = request.GET.get('shouye_data')
    models.Setting_storage.objects.filter(id=1).update(shouye_data=data)
    resultdict = {}
    resultdict['code'] = 0
    return JsonResponse(resultdict, safe=False)


def get_shouye_data(request):
    data = models.Setting_storage.objects.filter(id=1)[0].shouye_data
    resultdict = {}
    resultdict['data'] = data
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def required_login(func):
    def inner(*args, **kwargs):
        request = args[0]
        if request.session.get('is_login'):
            return func(*args, **kwargs)
        else:
            if request.is_ajax():
                return HttpResponse(json.dumps({'status': 0}))
            return redirect(reverse('login'))

    return inner


@csrf_exempt
def go_private_sea(request):
    return render(request, 'lyear_pages_data_table_private_sea.html')


@csrf_exempt
def console(request):
    table_simple_data = len(
        models.Dazhongdianping_liren_all_data.objects.all())
    table_simple_data_signing = len(
        models.Dazhongdianping_liren_signing_data.objects.all())
    user = len(models.User.objects.all())
    dazhongdianping_liren_new_all_data = len(
        models.Dazhongdianping_liren_all_data.objects.filter(
            shop_tags__contains='新店'))
    return render(
        request, "lyear_main.html", {
            "table_simple_data": table_simple_data,
            "table_simple_data_signing": table_simple_data_signing,
            "dazhongdianping_liren_new_all_data":
                dazhongdianping_liren_new_all_data,
            "user": user
        })


@csrf_exempt
def table_simple_data_count(request):
    city = request.GET.get('city')
    table_simple_data = models.Dazhongdianping_liren_all_data.objects.filter(
        shop_city=city).count()
    table_simple_data_signing = models.Order.objects.all().count()
    db = pymysql.connect("localhost", "root", "bakj123456", "rock")
    cursor = db.cursor()
    cursor.execute("select count(*) from user_userprofile")
    user = cursor.fetchall()
    cursor.close()
    # 关闭数据库连接
    db.close()
    table_simple_new_all_data = models.Dazhongdianping_liren_all_data.objects.filter(
        shop_tags__contains='新店', shop_city=city).count()
    user = re.sub("\D", "", str(user))
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['table_simple_data'] = table_simple_data
    resultdict['table_simple_data_signing'] = table_simple_data_signing
    resultdict['user'] = str(user)
    resultdict['table_simple_new_all_data'] = table_simple_new_all_data
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def shop_business_district_select(request):
    shop_category_create = request.GET.get('shop_category_create')
    business_data = models.Business_district_select.objects.filter(
        shop_city__in=eval(shop_category_create))
    dict_data = []
    for b in business_data:
        dict_data.append({
            'id': b.business_district,
            'label': b.business_district
        })
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['data'] = dict_data
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def shop_business_district_select_create(request):
    shop_category_create = request.GET.get('shop_category_create')
    business_data = models.Business_district_select.objects.filter(
        shop_city=shop_category_create)
    dict_data = []
    for b in business_data:
        dict_data.append({
            'id': b.business_district,
            'label': b.business_district
        })
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['data'] = dict_data
    return JsonResponse(resultdict, safe=False)


def select_business_circle(request):
    business_circle = request.GET.get('business_circle')
    city = request.GET.get('city')
    problems = models.Dazhongdianping_liren_all_data.objects.filter(
        shop_city=city, shop_business_district__in=eval(business_circle))
    print('business_circle', business_circle)
    dist = []
    for i in problems:
        dist.append(i.shop_category)
    urban_area_data = list(set(dist))
    urban_area = []
    for u in urban_area_data:
        urban_area.append({'label': u, 'id': u})
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['data'] = urban_area
    return JsonResponse(resultdict, safe=False)


def select_urban_area(request):
    city = request.GET.get('city')
    problems = models.Dazhongdianping_liren_all_data.objects.filter(
        shop_city=city)
    dist = []
    for i in problems:
        dist.append(i.shop_business_district)
    urban_area_data = list(set(dist))
    i = 0
    while i < len(urban_area_data):
        if '区' not in urban_area_data[i]:
            urban_area_data.pop(i)
            i -= 1
        else:
            pass
        i += 1
    urban_area = []
    for u in urban_area_data:
        urban_area.append({'label': u, 'id': u})
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['data'] = urban_area
    return JsonResponse(resultdict, safe=False)


def select_urban_area_user(request):
    city = request.GET.get('city')
    problems = models.Dazhongdianping_liren_user_data.objects.filter(
        shop_city__in=eval(city))
    print(problems)
    dist = []
    for i in problems:
        dist.append(i.shop_business_district)
    urban_area_data = list(set(dist))
    i = 0
    while i < len(urban_area_data):
        if '区' not in urban_area_data[i]:
            urban_area_data.pop(i)
            i -= 1
        else:
            pass
        i += 1
    urban_area = []
    for u in urban_area_data:
        urban_area.append({'label': u, 'id': u})
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['data'] = urban_area
    return JsonResponse(resultdict, safe=False)


# 显示商圈
@csrf_exempt
def search_business_circle(request):
    region = request.GET.get('region')
    city = request.GET.get('city')
    problems = models.Dazhongdianping_liren_user_data.objects.filter(
        shop_city__in=eval(city), shop_business_district__in=eval(region))
    dist = []
    for i in problems:
        dist.append(i.shop_category)
    urban_area_data = list(set(dist))
    urban_area = []
    for u in urban_area_data:
        urban_area.append({'label': u, 'id': u})
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['data'] = urban_area
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def jump_xindian(request):
    problems = models.Setting_storage.objects.all().update(tags_data='新店')
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['count'] = 20
    resultdict['curr'] = 1
    resultdict['limit'] = 11
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def get_jump_href(request):
    problems = models.Setting_storage.objects.all()
    dic = ''
    for p in problems:
        dic = p.tags_data
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['count'] = 20
    resultdict['dic'] = dic
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def update_jump_href(request):
    problems = models.Setting_storage.objects.all().update(tags_data='')
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['count'] = 20
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def username_data(request):
    problems = models.User.objects.all()
    dict = []
    for p in problems:
        dic = {}
        dic['name'] = p.name
        dict.append(dic)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['count'] = 20
    resultdict['curr'] = 1
    resultdict['limit'] = 1
    resultdict['data'] = dict
    print(resultdict)
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def get_user_data(request):
    problems = models.User.objects.filter(role='销售')
    dict = []
    for p in problems:
        dic = {}
        dict.append({'label': p.username, 'id': p.username})
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


# 显示用户数据
@csrf_exempt
def user_data(request):
    page = request.POST.get('pageSize')
    rows = request.POST.get('curr')
    name = request.POST.get("search")
    # i = (int(page) - 1) * int(rows)
    # j = (int(page) - 1) * int(rows) + int(rows)
    problems = models.User.objects.all()
    total = problems.count()
    # problems = problems[i:j]
    dict = []
    data = {"rows": dict, "total": total}
    for p in problems:
        dic = {}
        dic['id'] = p.id
        dic['name'] = p.name
        dic['username'] = p.username
        dic['phone'] = p.phone
        dic['last_time'] = str(p.last_time)
        dic['email'] = p.email
        dic['gender'] = p.gender
        dic['have_access'] = p.have_access
        dic['role'] = p.role
        dic['specific_description'] = p.specific_description
        dict.append(dic)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['total'] = total
    resultdict['count'] = 20
    resultdict['curr'] = 1
    resultdict['limit'] = 1
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def submit_review(request):
    project = request.GET.get('project')  # 项目名
    shop_name = request.GET.get('shop_name')  # 店名
    time = request.GET.get('time')  # 该完成时间
    money = request.GET.get('money')  # 钱
    schedule = request.GET.get('schedule')  # 进度
    username = request.GET.get('username')  # 任务分配人
    submitter = request.GET.get('username')  # 提交人
    order_id = request.GET.get('order_id')  # 提交人
    lat = request.GET.get('lat')  # 提交人
    lng = request.GET.get('lng')  # 提交人
    edit = request.GET.get('edit')  # 提交人
    url = request.GET.get('url')
    submit_time = datetime.date.today()  # 提交时间
    count = models.Pending_review.objects.filter(project=project, shop_name=shop_name, order_id=order_id).count()
    if count != 0:
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 2
        return JsonResponse(resultdict, safe=False)
    else:
        db = pymysql.connect("localhost", "root", "bakj123456", "rock")
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM user_userprofile where first_name = '" + username + "'")
        data = cursor.fetchall()
        group_name = data[0][14]
        cursor2 = db.cursor()
        cursor2.execute(
            "SELECT * FROM user_userprofile where group_name = '" + group_name + "'")
        data = cursor2.fetchall()
        admin_username = ''
        tesr_username = ''
        for a in data:
            if a[11] == 'admin':
                tesr_username = a[4]
                admin_username = a[5]
        if tesr_username == 'admin' or tesr_username == 'super_admin':
            admin_username = '超级管理员'
        shop_add = models.Pending_review.objects.create(project=project,
                                                        shop_name=shop_name,
                                                        time=time,
                                                        money=money,
                                                        schedule=schedule,
                                                        username=username,
                                                        submitter=admin_username,
                                                        submit_time=submit_time,
                                                        order_id=order_id,
                                                        lat=lat,
                                                        status='待审核',
                                                        lng=lng,
                                                        url=url,
                                                        edit=edit, )
    if shop_add != None:
        db = pymysql.connect("localhost", "root", "bakj123456", "rock")
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM user_userprofile where first_name = '" + username + "'")
        data = cursor.fetchall()
        group_name = data[0][14]
        cursor2 = db.cursor()
        cursor2.execute(
            "SELECT * FROM user_userprofile where group_name = '" + group_name + "'")
        data = cursor2.fetchall()
        admin_username = ''
        for a in data:
            if a[11] == 'admin':
                admin_username = a[4]
        cursor3 = db.cursor()
        cursor3.execute("SELECT * FROM app_to_do where project='" + project + "' and shop_name='" + shop_name + "'")
        data = cursor3.fetchall()
        to_do_id = data[0][0]
        str_todo = 'UPDATE app_pending_review SET id=' + str(
            to_do_id) + ' where project="' + project + '" and shop_name="' + shop_name + '"'
        cursor4 = db.cursor()
        cursor4.execute(str_todo)
        db.commit()
        wx = Wx_Shenpi()
        str_todo = 'SELECT * FROM app_pending_review where id = ' + str(to_do_id) + ''
        cursor5 = db.cursor()
        cursor5.execute(str_todo)
        data3 = cursor5.fetchall()
        if admin_username == 'admin' or admin_username == '超级管理员':
            admin_username = 'pengyan'
            if url == '':
                wx.send_data_renwu(shop_name, project, username, str(submit_time), str(time), str(edit), admin_username,
                                   to_do_id)
                models.To_do.objects.filter(project=project,
                                            username=username,
                                            shop_name=shop_name).delete()
            else:
                wx.send_img(url, admin_username)
                wx.send_data_renwu(shop_name, project, username, str(submit_time), str(time), str(edit), admin_username,
                                   to_do_id)
                models.To_do.objects.filter(project=project,
                                            username=username,
                                            shop_name=shop_name).delete()
        else:
            if url == '':
                wx.send_data_renwu(shop_name, project, username, str(submit_time), str(time), str(edit), admin_username,
                                   to_do_id)
                models.To_do.objects.filter(project=project,
                                            username=username,
                                            shop_name=shop_name).delete()
            else:
                wx.send_img(url, admin_username)
                wx.send_data_renwu(shop_name, project, username, str(submit_time), str(time), str(edit), admin_username,
                                   to_do_id)
                models.To_do.objects.filter(project=project,
                                            username=username,
                                            shop_name=shop_name).delete()

        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)


@csrf_exempt
def order_count(request):
    username = request.GET.get('username')
    date = request.GET.get('month_data')
    print('日期', date)
    print('username', username)
    today = date
    print('当前的时间', today)
    now_date = datetime.datetime.strptime(date + '-01', '%Y-%m-%d')
    first = now_date.replace(day=1)
    print('first', first)
    last_month = first - datetime.timedelta(days=1)
    # 上个月年月份
    last_month = str(last_month)[0:7]
    numbers = 0
    numbers2 = 0
    performance = 0
    commission_point = 0
    res = last_day_of_month(now_date)
    print('res', res)
    next_month = str(res + datetime.timedelta(days=1))[0:7]  # 下月日期
    print('下个月的日期', next_month)
    shop_add = models.Order.objects.filter(order_contract_sales=username,
                                           order_date__startswith=today)
    performance_data = models.Order.objects.filter(
        order_contract_sales=username)
    # 上下月的服务奖金
    last_month_service_bonus_data_todo = models.To_do.objects.filter(
        time__contains=today, username=username)
    last_month_service_bonus_data_completed = models.Completed.objects.filter(
        time__contains=today, username=username)
    last_month_service_bonus_data_pending_review = models.Pending_review.objects.filter(
        time__contains=today, username=username)
    next_month_service_bonus_data_todo = models.To_do.objects.filter(
        time__contains=next_month, username=username)
    next_month_service_bonus_data_completed = models.Completed.objects.filter(
        time__contains=next_month, username=username)
    next_month_service_bonus_data_pending_review = models.Pending_review.objects.filter(
        time__contains=next_month, username=username)
    last_month_service_bonus = 0
    next_month_service_bonus = 0
    for lt in last_month_service_bonus_data_todo:
        last_month_service_bonus = last_month_service_bonus + \
                                   int(float(lt.money))
    for ll in last_month_service_bonus_data_completed:
        last_month_service_bonus = last_month_service_bonus + \
                                   int(float(ll.money))
    for lp in last_month_service_bonus_data_pending_review:
        last_month_service_bonus = last_month_service_bonus + \
                                   int(float(lp.money))
    for lt2 in next_month_service_bonus_data_todo:
        next_month_service_bonus = next_month_service_bonus + \
                                   int(float(lt2.money))
    for ll2 in next_month_service_bonus_data_completed:
        next_month_service_bonus = next_month_service_bonus + \
                                   int(float(ll2.money))
    for lp2 in next_month_service_bonus_data_pending_review:
        next_month_service_bonus = next_month_service_bonus + \
                                   int(float(lp2.money))
    #  本月已获得的服务奖金
    month_service_bonus = 0
    month_service_bonus_data = models.Completed.objects.filter(
        time__contains=today, username=username)
    for m in month_service_bonus_data:
        month_service_bonus = month_service_bonus + int(float(m.money))
    # 下月已获得的服务奖金
    next_get_month_service_bonus = 0
    next_get_month_service_bonus_data = models.Completed.objects.filter(
        time__contains=next_month, username=username)
    for n in next_get_month_service_bonus_data:
        next_get_month_service_bonus = next_get_month_service_bonus + int(
            float(n.money))
    for p in shop_add:
        numbers += int(p.order_amount)
        numbers2 += int(p.order_amount) - int(p.cost_fees)
        # 判断日期是否匹配订单
    for i in performance_data:
        if str(today)[0:7] == i.order_date[0:7]:
            performance += int(i.order_amount)
    commission_point_data = models.Setting_storage.objects.all()
    commission_point_json = ''
    for c in commission_point_data:
        commission_point_json = c.commission_form
    count = []
    for o in eval(commission_point_json):
        count.append(int(o['commission_performance']))
    for a in sorted(count):
        if performance >= a:
            for o in eval(commission_point_json):
                if a == int(o['commission_performance']):
                    commission_point = int(o['commission_commission_point'])
        else:
            performance = 0
    table_simple_data = numbers
    table_simple_data_signing = (numbers2 *
                                 (int(commission_point) / 100)) * 2 / 3
    user = len(shop_add)
    table_simple_new_all_data = len(
        models.Dazhongdianping_liren_user_data.objects.filter(
            username=username))  # 意向客户
    order = models.Order.objects.filter(order_contract_sales=username)
    money = 0  # 订单金额
    cost_fees = 0
    for p in order:
        if str(today)[0:7] in p.order_date:
            cost_fees += int(p.cost_fees)
            money += int(p.order_amount)
    # 计算提成点
    commission_point = 0
    commission_point_data = models.Setting_storage.objects.all()
    todo_count = 0
    todo_count_number = 0
    commission_point_json = ''
    for c in commission_point_data:
        commission_point_json = c.commission_form
    count = []
    for o in eval(commission_point_json):
        count.append(int(o['commission_performance']))
    for a in sorted(count):
        if money >= a:
            for o in eval(commission_point_json):
                if a == int(o['commission_performance']):
                    commission_point = int(o['commission_commission_point'])
        else:
            performance = 0
    Order = models.Order.objects.filter(tags__in=('续约', '新签'))
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['table_simple_data'] = int(table_simple_data)
    resultdict['table_simple_data_signing'] = int(table_simple_data_signing)
    resultdict['commission_point'] = int(commission_point)
    resultdict['last_month_service_bonus'] = int(last_month_service_bonus)
    resultdict['month_service_bonus'] = int(month_service_bonus)
    resultdict['cost_fees'] = int(cost_fees)
    resultdict['next_month_service_bonus'] = int(next_month_service_bonus)
    resultdict['next_get_month_service_bonus'] = int(next_get_month_service_bonus)
    resultdict['user'] = user
    resultdict['table_simple_new_all_data'] = table_simple_new_all_data
    return JsonResponse(resultdict, safe=False)


def transfer_update(request):
    order_id = request.GET.get('order_id')
    type2 = request.GET.get('type')
    username = request.GET.get('username')
    project = request.GET.get('project')
    if eval(type2)['id'] == '未完成':
        models.To_do.objects.filter(
            order_id=order_id, project=project).update(username=username)
    elif eval(type2)['id'] == '待审核':
        models.Pending_review.objects.filter(
            order_id=order_id, project=project).update(username=username)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def contract_id_verification(request):
    contract_id = request.GET.get('contract_id')
    form = models.Order.objects.filter(contract_id=contract_id).count()
    if form != 0:
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 1
    elif form == 0:
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 2
    return JsonResponse(resultdict, safe=False)


def shenhe_order_select(request):
    username = request.GET.get('username')
    page = request.GET.get('currentPage')
    rows = request.GET.get('pagesize')
    search = request.GET.get('search')
    db = pymysql.connect("localhost", "root", "bakj123456", "rock")
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM user_userprofile where first_name = '" + username + "'")
    data = cursor.fetchall()
    group_name = data[0][14]
    cursor2 = db.cursor()
    if group_name == '所有组':
        cursor2.execute("SELECT * FROM user_userprofile")
    else:
        cursor2.execute(
            "SELECT * FROM user_userprofile where group_name = '" + group_name + "'")
    cursor22 = cursor2.fetchall()
    username_list = []
    for i in cursor22:
        if group_name == '所有组':
            if i[11] != 'admin':
                pass
            else:
                username_list.append(i[5])
        else:
            if i[11] == 'admin' or i[11] == 'super_admin':
                pass
            else:
                username_list.append(i[5])
    username_list.append('超级管理员')
    username_list.append(username)
    if search == None or search == '':
        order_data = models.Shenhe_order.objects.filter(
            order_contract_sales__in=username_list)
    else:
        order_data = models.Shenhe_order.objects.filter(order_contract_sales__in=username_list,
                                                        sign_contract_shop__contains=search)
    print('order_data', order_data.count())
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    total = order_data.count()
    order_data = order_data[i:j]
    dict = []
    for p in order_data:
        dic = {}
        dic['contract_id'] = p.contract_id
        dic['order_date'] = p.order_date[0:10]
        dic['order_start_date'] = p.order_start_date[0:10]
        dic['sign_contract_shop'] = p.sign_contract_shop
        dic['customer_source'] = p.customer_source
        dic['contract_status'] = p.contract_status
        dic['contracted_projects'] = p.contracted_projects
        dic['shop_industry'] = p.shop_industry
        dic['shop_kp_name'] = p.shop_kp_name
        dic['shop_telephonenumber'] = p.shop_telephonenumber
        dic['order_numbers'] = p.order_numbers
        dic['shop_cooperation_duration'] = p.shop_cooperation_duration
        dic['order_end_date'] = p.order_end_date
        dic['order_amount'] = p.order_amount
        dic['payment_method'] = p.payment_method
        dic['shop_id'] = p.shop_id
        dic['order_contract_sales'] = p.order_contract_sales
        dic['shop_remark'] = p.shop_remark
        dic['cost_fees'] = p.cost_fees
        dic['order_form'] = eval(p.order_form)
        dic['order_commission'] = p.order_commission
        dic['tags'] = p.tags
        dic['city'] = p.city
        dic['dialogImageUrl'] = p.dialogImageUrl
        dict.append(dic)
    print(dict)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    resultdict['total'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


def shenhe_order(request):
    contract_id = request.GET.get('contract_id')
    order_date = request.GET.get('order_date')
    sign_contract_shop = request.GET.get('sign_contract_shop')
    order_start_date = request.GET.get('order_start_date')
    customer_source = request.GET.get('customer_source')
    contract_status = request.GET.get('contract_status')
    contracted_projects = request.GET.get('contracted_projects')
    shop_industry = request.GET.get('shop_industry')
    shop_kp_name = request.GET.get('shop_kp_name')
    shop_telephonenumber = request.GET.get('shop_telephonenumber')
    order_numbers = request.GET.get('order_numbers')
    cost_fees = request.GET.get('cost_fees')
    shop_cooperation_duration = request.GET.get('shop_cooperation_duration')
    order_end_date = request.GET.get('order_end_date')
    order_amount = request.GET.get('order_amount')
    payment_method = request.GET.get('payment_method')
    order_contract_sales = request.GET.get('order_contract_sales')
    shop_remark = request.GET.get('shop_remark')
    shop_add_form = request.GET.get('shop_add_form_data')
    shop_id = request.GET.get('shop_id')
    tags = request.GET.get('tags')
    dialogImageUrl = request.GET.get('dialogImageUrl')
    order_date = datetime.datetime.strptime(
        order_date[0:10], '%Y-%m-%d').date()
    order_start_date = datetime.datetime.strptime(
        order_start_date[0:10], '%Y-%m-%d').date()
    order_date = order_date + datetime.timedelta(days=1)
    order_start_date = order_start_date + datetime.timedelta(days=1)
    count = models.Shenhe_order.objects.filter(shop_id=shop_id).count()
    count2 = models.Shenhe_order.objects.filter(
        contract_id=contract_id).count()
    if count == 0 and count2 == 0:
        db = pymysql.connect("localhost", "root", "bakj123456", "rock")
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM user_userprofile where first_name = '" + order_contract_sales + "'")
        data = cursor.fetchall()
        group_name = data[0][14]
        admin = data[0][11]
        cursor2 = db.cursor()
        cursor2.execute(
            "SELECT * FROM user_userprofile where group_name = '" + group_name + "'")
        data = cursor2.fetchall()
        username = ''
        for a in data:
            if a[11] == 'admin':
                username = a[4]
        city = models.Dazhongdianping_liren_user_data.objects.filter(
            shop_id=shop_id)
        city = city[0].shop_city
        tag = '新签'
        tag_data = models.Order.objects.filter(shop_id=shop_id)
        if len(tag_data) > 1:
            tag = '续约'
        fangshi = ''
        for i in eval(shop_add_form):
            if i['label'] == '付款方式':
                print(i)
                fangshi = i['value']

        models.Shenhe_order.objects.create(
            shop_id=shop_id,
            contract_id=contract_id,
            order_date=order_date,
            order_start_date=order_start_date,
            customer_source=customer_source,
            sign_contract_shop=sign_contract_shop,
            contract_status=contract_status,
            contracted_projects=contracted_projects,
            shop_industry=shop_industry,
            shop_kp_name=shop_kp_name,
            cost_fees=cost_fees,
            order_numbers=order_numbers,
            shop_telephonenumber=shop_telephonenumber,
            shop_cooperation_duration=shop_cooperation_duration,
            order_end_date=str(order_end_date)[0:10],
            order_amount=order_amount,
            payment_method=payment_method,
            order_contract_sales=order_contract_sales,
            shop_remark=shop_remark,
            order_form=eval(shop_add_form),
            order_commission=0,
            tags=tags,
            city=city,
            dialogImageUrl=dialogImageUrl
        )
        a = models.Shenhe_order.objects.filter(contract_id=contract_id)
        id = ''
        for p in a:
            global shop_form
            shop_form = p.order_form
            id = p.id
            b = models.Shenhe_order.objects.filter(contract_id=contract_id).update(order_form=[
                {"value": "收钱吧", "label": "付款方式", "type": "选择下拉框", "index": "付款方式"},
                {"value": "点评套餐", "label": "签约项目", "type": "选择下拉框", "index": "签约项目"}])
            print(b)
        if admin == 'admin' or order_contract_sales == '超级管理员':
            username = 'pengyan'
            wx = Wx_Shenpi()
            wx.send_data(username, order_contract_sales, tags, sign_contract_shop, city,
                         order_numbers, shop_cooperation_duration, order_amount, fangshi, contract_id, dialogImageUrl)
        else:
            wx = Wx_Shenpi()
            wx.send_data(username, order_contract_sales, tags, sign_contract_shop, city,
                         order_numbers, shop_cooperation_duration, order_amount, fangshi, contract_id, dialogImageUrl)
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 0
        return JsonResponse(resultdict, safe=False)
    else:
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)


# 开启任务的提成点要更改
# 是否要开启频率？
def create_order(request):
    contract_id = request.GET.get('contract_id')
    order_date = request.GET.get('order_date')
    sign_contract_shop = request.GET.get('sign_contract_shop')
    order_start_date = request.GET.get('order_start_date')
    customer_source = request.GET.get('customer_source')
    contract_status = request.GET.get('contract_status')
    contracted_projects = request.GET.get('contracted_projects')
    shop_industry = request.GET.get('shop_industry')
    shop_kp_name = request.GET.get('shop_kp_name')
    shop_telephonenumber = request.GET.get('shop_telephonenumber')
    order_numbers = request.GET.get('order_numbers')
    cost_fees = request.GET.get('cost_fees')
    shop_cooperation_duration = request.GET.get('shop_cooperation_duration')
    order_end_date = request.GET.get('order_end_date')
    order_amount = request.GET.get('order_amount')
    payment_method = request.GET.get('payment_method')
    order_contract_sales = request.GET.get('order_contract_sales')
    shop_remark = request.GET.get('shop_remark')
    shop_add_form = request.GET.get('order_form')
    tags = request.GET.get('tags')
    shop_id = request.GET.get('shop_id')
    city = request.GET.get('city')
    shop_id_id = shop_id
    count = models.Order.objects.filter(contract_id=contract_id).count()
    if count == 0:
        # try:
        order_start_date_year = int(order_start_date[0:4])
        order_start_date_month = int(order_start_date[5:7])
        if '0' == order_start_date[5:6]:
            order_start_date_month = int(order_start_date[6:7])
        order_start_date_day = int(order_start_date[8:10])
        if '0' == order_start_date[8:9]:
            order_start_date_day = int(order_start_date[9:10])
        order_start_date = datetime.date(order_start_date_year,
                                         order_start_date_month,
                                         order_start_date_day)
        order_date_year = int(order_date[0:4])
        order_date_month = int(order_date[5:7])
        if '0' == order_date[5:6]:
            order_date_month = int(order_date[6:7])
        order_date_day = int(order_date[8:10])
        if '0' == order_date[8:9]:
            order_date_day = int(order_date[9:10])
        order_date = datetime.date(order_date_year, order_date_month,
                                   order_date_day)
        shop_add = models.Order.objects.create(
            shop_id=shop_id,
            contract_id=contract_id,
            order_date=str(order_date + datetime.timedelta(days=1))[0:10],
            date=str(order_date + datetime.timedelta(days=1))[0:7],
            order_start_date=str(order_start_date +
                                 datetime.timedelta(days=1))[0:10],
            customer_source=customer_source,
            sign_contract_shop=sign_contract_shop,
            contract_status=contract_status,
            contracted_projects=contracted_projects,
            shop_industry=shop_industry,
            shop_kp_name=shop_kp_name,
            cost_fees=cost_fees,
            order_numbers=order_numbers,
            shop_telephonenumber=shop_telephonenumber,
            shop_cooperation_duration=shop_cooperation_duration,
            order_end_date=str(order_end_date)[0:10],
            order_amount=order_amount,
            payment_method=payment_method,
            order_contract_sales=order_contract_sales,
            shop_remark=shop_remark,
            order_form=shop_add_form,
            order_commission=int(order_amount) * 0.15,
            city=city,
            tags=tags)
        data = datetime.date.today()
        a = models.Dazhongdianping_liren_user_data.objects.filter(
            shop_id=shop_id)
        edit_data = ''
        for i in a:
            edit_data = i.shop_edit
        print(edit_data)
        if shop_remark == '' or shop_remark == None:
            print('')
        else:
            models.Dazhongdianping_liren_user_data.objects.filter(
                shop_id=shop_id).update(shop_edit=edit_data + '修改人:' +
                                                  order_contract_sales + '，时间:' + str(data) +
                                                  '，内容:' + shop_remark + '￥')
        order_start_date = request.GET.get('order_start_date')
        order_date = request.GET.get('order_date')

        if shop_add != '':
            create = models.Dazhongdianping_liren_user_data.objects.filter(
                shop_id=shop_id)
            # tags = ''
            # if contract_status == '新签客户':
            #     tags = '新签,'
            # elif contract_status == '老客户续约':
            #     tags = '续约,'
            tag = '新签'
            tag_data = models.Order.objects.filter(shop_id=shop_id)
            if len(tag_data) > 1:
                tag = '续约'
            models.Dazhongdianping_liren_user_data.objects.filter(
                shop_id=shop_id).update(shop_tags=tag)
            for c in create:
                models.Dazhongdianping_liren_all_data.objects.create(
                    shop_id=c.shop_id,
                    shop_name=c.shop_name,
                    shop_start=c.shop_start,
                    shop_review_count=c.shop_review_count,
                    shop_bad_review=c.shop_bad_review,
                    shop_per_capita_consumption=c.shop_per_capita_consumption,
                    shop_effect=c.shop_effect,
                    shop_service=c.shop_service,
                    shop_surroundings=c.shop_surroundings,
                    shop_address=c.shop_address,
                    shop_telephonenumber=c.shop_telephonenumber,
                    shop_business_district=c.shop_business_district,
                    shop_category=c.shop_category,
                    shop_region=c.shop_region,
                    shop_tags=tags,
                    shop_edit=c.shop_edit,
                    shop_kp_name=c.shop_kp_name,
                    shop_kp_position=c.shop_kp_position,
                    shop_kp_wechat_id=c.shop_kp_wechat_id,
                    shop_kp_city=c.shop_kp_city,
                    shop_city=c.shop_city,
                    shop_kp_category='',
                    shop_add_form=c.shop_add_form)
                models.Dazhongdianping_liren_user_data.objects.filter(
                    shop_id=c.shop_id).delete()
            models.Order.objects.filter(
                shop_id=shop_id, contract_id=contract_id).update(tags=tag[0:2])
            # models.Dazhongdianping_liren_user_data.objects.filter(
            #     shop_name=sign_contract_shop).delete()
            problems = models.Setting_storage.objects.all()
            now_date = datetime.date.today()
            first = now_date.replace(day=1)
            last_month = str(now_date)
            performance = 0
            commission_point = 0
            performance_data = models.Order.objects.filter(
                order_contract_sales=order_contract_sales)
            for i in performance_data:
                if str(last_month)[0:7] == i.order_date[0:7]:
                    performance += int(i.order_amount)
            commission_point_data = models.Setting_storage.objects.all()
            commission_point_json = ''
            for c in commission_point_data:
                commission_point_json = c.commission_form
            count = []
            for o in eval(commission_point_json):
                count.append(int(o['commission_performance']))
            for a in sorted(count):
                if performance >= a:
                    for o in eval(commission_point_json):
                        if a == int(o['commission_performance']):
                            commission_point = int(
                                o['commission_commission_point'])
                else:
                    performance = 0
            date_time = order_start_date
            js = 0
            year = int(date_time[0:4])
            month = int(date_time[5:7])
            if '0' == date_time[5:6]:
                month = int(str(date_time[6:7]))
            day = int(date_time[8:10])
            if '0' == date_time[8:9]:
                day = int(date_time[9:10])
            date = datetime.date(year, month, day)
            data = ''
            for i in problems:
                data = i.todo_form
            total_number_of_tasks = 0  # 任务总数
            # 计算任务总数
            for at in range(0, len(eval(data))):
                if eval(data)[at]['select'] == '单次任务':
                    total_number_of_tasks = total_number_of_tasks + 1
                elif eval(data)[at]['select'] == '重复任务':
                    frequency = eval(data)[at]['time']  # 获取重复任务的频率
                    start_date = order_start_date
                    end_date = order_end_date
                    # 开始的时间
                    date_time = order_start_date
                    year = int(date_time[0:4])
                    month = int(date_time[5:7])
                    if '0' == date_time[5:6]:
                        month = int(date_time[6:7])
                    day = int(date_time[8:10])
                    if '0' == date_time[8:9]:
                        day = int(date_time[9:10])
                    cur_day = datetime.date(int(year), int(month), int(day))
                    # 结束的时间
                    date_time_end = order_end_date
                    year_end = int(date_time_end[0:4])
                    month_end = int(date_time_end[5:7])
                    if '0' == date_time_end[5:6]:
                        month_end = int(date_time_end[6:7])
                    day_end = int(date_time_end[8:10])
                    if '0' == date_time_end[8:9]:
                        day_end = int(date_time_end[9:10])
                    # 订单开始的时间
                    cur_day = datetime.date(
                        int(year), int(month), int(day))
                    # 订单结束的时间
                    next_day = datetime.date(int(year_end), int(month_end),
                                             int(day_end))
                    # 　两个日期之间的差值
                    difference = int((next_day - cur_day).days)
                    count = int(difference) / int(frequency)
                    count = round(count)
                    print(count)
                    total_number_of_tasks = total_number_of_tasks + count
            money = int(order_amount) * \
                    (int(commission_point) / 100) * (1 / 3)
            money = money * 2
            print('提成点', money)
            # 分配任务以及金额
            for a in range(0, len(eval(data))):
                if eval(data)[a]['select'] == '单次任务':
                    models.To_do.objects.create(
                        project=eval(data)[a]['name'],
                        shop_name=sign_contract_shop,
                        order_id=contract_id,
                        # 开始日期加上任务的时间
                        time=date + \
                             datetime.timedelta(
                                 days=int(eval(data)[a]['time'])),
                        money=round(money / total_number_of_tasks),
                        schedule=0,
                        username=order_contract_sales,
                        status='未审核')
                elif eval(data)[a]['select'] == '重复任务':
                    # 重复频率
                    frequency = eval(data)[a]['time']  # 获取重复任务的频率
                    start_date = order_start_date
                    end_date = order_end_date
                    # 开始的时间
                    date_time = order_start_date
                    year = int(date_time[0:4])
                    month = int(date_time[5:7])
                    if '0' == date_time[5:6]:
                        month = int(date_time[6:7])
                    day = int(date_time[8:10])
                    if '0' == date_time[8:9]:
                        day = int(date_time[9:10])
                    cur_day = datetime.date(year, month, day)
                    # 结束的时间
                    date_time_end = order_end_date
                    year_end = int(date_time_end[0:4])
                    month_end = int(date_time_end[5:7])
                    if '0' == date_time_end[5:6]:
                        month_end = int(date_time_end[6:7])
                    day_end = int(date_time_end[8:10])
                    if '0' == date_time_end[8:9]:
                        day_end = int(date_time_end[9:10])
                    # 订单开始的时间
                    cur_day = datetime.date(year, month, day)
                    # 订单结束的时间
                    next_day = datetime.date(
                        int(year_end), int(month_end), int(day_end))
                    # 　两个日期之间的差值
                    difference = int((next_day - cur_day).days)
                    count = int(difference) / int(frequency)
                    count = round(count)
                    original_time = cur_day
                    for b in range(0, count):
                        models.To_do.objects.create(
                            project='第' + str(b + 1) + '次' +
                                    eval(data)[a]['name'],
                            shop_name=sign_contract_shop,
                            order_id=contract_id,
                            time=original_time + datetime.timedelta(days=int(
                                eval(data)[a]['time'])),  # 开始日期加上任务的时间
                            money=round(money / total_number_of_tasks),
                            schedule=0,
                            username=order_contract_sales,
                            status='未审核')
                        original_time = original_time + \
                                        datetime.timedelta(
                                            days=int(eval(data)[a]['time']))
            models.Shenhe_order.objects.filter(shop_id=shop_id_id).delete()
            db = pymysql.connect("localhost", "root", "bakj123456", "rock")
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM user_userprofile where first_name = '" + order_contract_sales + "'")
            data = cursor.fetchall()
            group = data[0][14]  # 销售组
            name = data[0][4]  # 签约人
            cursor2 = db.cursor()
            cursor2.execute(
                "SELECT * FROM user_userprofile where group_name = '" + group + "' and avatar='admin'")
            data2 = cursor2.fetchall()
            fangshi = ''
            for i in eval(shop_add_form):
                if i['label'] == '付款方式':
                    print(i)
                    fangshi = i['value']
            wx = WeChat()
            wx.send_data(
                '订单审核通过\n'
                '小组：' + group + '\n'
                                '销售：' + order_contract_sales + '\n'
                                                               '新签/续约：' + tags + '\n'
                                                                                 '店名：' + sign_contract_shop + '\n'
                                                                                                              '城市：' + city + '\n'
                                                                                                                             '店数：' + str(
                    order_numbers) + '\n'
                                     '时长：' + str(shop_cooperation_duration) + '个月\n'
                                                                              '金额：' + str(order_amount) + '\n'
                                                                                                          '支付方式：' + fangshi + '\n',
                name)
            headers = {'Content-Type': 'text/plain'}
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "content":
                        "💫北爱“" + order_contract_sales + "”战报来袭 💫\n"
                        "小组：<font color=\"red\">" + group + "</font>\n"
                        "销售：<font color=\"red\">" + order_contract_sales + "</font>\n"
                        "新签/续约：<font color=\"red\">" + tag + "</font>\n"
                        "店名：<font color=\"red\">" + sign_contract_shop + "</font>\n"
                        "城市：<font color=\"red\">" + city + "</font>\n"
                        "店数：<font color=\"red\">" +str(order_numbers) + "</font>\n"
                        "时长：<font color=\"red\">" +str(shop_cooperation_duration) + "个月</font>\n"
                        "金额：<font color=\"red\">" +str(order_amount) + "元</font>\n"
                        "支付方式：<font color=\"red\">" + fangshi + "</font>\n"
                        "签约时间：<font color=\"red\">" + order_date + "</font>\n"
                        "开始时间：<font color=\"red\">" + order_start_date + "</font>\n"
                        "厉害牛牛牛！！加油加油👍🏻👍🏻 🌹🌹以上签收同步赞赞赞👍👍👍使命必达🎉🎉🎉\n"
                }
            }
            requests.post(
                url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=91ce23c7-be03-47d3-a5e8-def2937fdc30',
                json=data, headers=headers)
            resultdict = {}
            resultdict['code'] = 0
            resultdict['msg'] = ""
            resultdict['state'] = 0
            return JsonResponse(resultdict, safe=False)
    else:
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = '创建出错'
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)


def delete_shenhe(request):
    username = request.GET.get('username')
    order_id = request.GET.get('order_id')
    tags = request.GET.get('tags')
    sign_contract_shop = request.GET.get('sign_contract_shop')
    city = request.GET.get('city')
    order_numbers = request.GET.get('order_numbers')
    shop_cooperation_duration = request.GET.get('shop_cooperation_duration')
    order_amount = request.GET.get('order_amount')
    order_form = request.GET.get('order_form')
    value = request.GET.get('value')
    db = pymysql.connect("localhost", "root", "bakj123456", "rock")
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM user_userprofile where first_name = '" + username + "'")
    data = cursor.fetchall()
    name = data[0][4]
    group = data[0][14]
    fangshi = ''
    for i in eval(order_form):
        if i['label'] == '付款方式':
            print(i)
            fangshi = i['value']
    wx = WeChat()
    wx.send_data(
        '订单审核失败\n'
        '失败原因：' + value + '\n'
                          '--------------------\n'
                          '小组：' + group + '\n'
                                          '销售：' + username + '\n'
                                                             '新签/续约：' + tags + '\n'
                                                                               '店名：' + sign_contract_shop + '\n'
                                                                                                            '城市：' + city + '\n'
                                                                                                                           '店数：' + str(
            order_numbers) + '\n'
                             '时长：' + str(shop_cooperation_duration) + '个月\n'
                                                                      '金额：' + str(order_amount) + '\n'
                                                                                                  '支付方式：' + fangshi + '\n',
        name)
    models.Shenhe_order.objects.filter(contract_id=order_id).delete()
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def order_select_data(request):
    username = request.GET.get('username')
    month = request.GET.get('month')
    count = models.Order.objects.filter(order_contract_sales=username,
                                        order_date__contains=month).count()
    count2 = models.Shenhe_order.objects.filter(order_contract_sales=username,
                                                order_date__contains=month).count()
    resultdict = {}
    resultdict['code'] = 0
    resultdict['count'] = str(count + count2 + 1)
    resultdict['state'] = 1
    return JsonResponse(resultdict, safe=False)


# 跳转到修改密码
def password(request):
    return render(request, "user_set_password.html")


# 跳转全部商户
def table_simple(request):
    return render(request, "lyear_pages_data_table.html")


# 跳转全部商户
def table_simple_new(request):
    return render(request, "lyear_pages_data_table_new.html")


# 跳转签约商户
def table_simple_signing(request):
    return render(request, "lyear_pages_data_table_signing.html")


# 添加商户数据
@csrf_exempt
@required_login
def table_simple_data_add(request):
    resultdict = {}
    try:
        shop_id = request.POST.get('shop_id')
        shop_name = request.POST.get('shop_name')
        shop_start = request.POST.get("shop_start")
        shop_review_count = request.POST.get("shop_review_count")
        shop_bad_review = request.POST.get("shop_bad_review")
        shop_per_capita_consumption = request.POST.get(
            "shop_per_capita_consumption")
        shop_effect = request.POST.get("shop_effect")
        shop_service = request.POST.get("shop_service")
        shop_surroundings = request.POST.get("shop_surroundings")
        shop_region = request.POST.get("shop_region")
        shop_business_district = request.POST.get("shop_business_district")
        shop_category = request.POST.get("shop_category")
        shop_address = request.POST.get("shop_address")
        shop_telephonenumber = request.POST.get("shop_telephonenumber")
        shop_edit = request.POST.get("shop_edit")
    except:
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 0
        return JsonResponse(resultdict, safe=False)
    # print('后台数据显示:' , shop_id,shop_name)
    shop_add = models.Dazhongdianping_liren_all_data.objects.create(
        shop_id=shop_id,
        shop_name=shop_name,
        shop_per_capita_consumption=shop_per_capita_consumption,
        shop_bad_review=shop_bad_review,
        shop_review_count=shop_review_count,
        shop_effect=shop_effect,
        shop_start=shop_start,
        shop_service=shop_service,
        shop_surroundings=shop_surroundings,
        shop_region=shop_region,
        shop_business_district=shop_business_district,
        shop_category=shop_category,
        shop_telephonenumber=shop_telephonenumber,
        shop_address=shop_address,
        shop_edit=shop_edit)
    if shop_add != None:
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)


@csrf_exempt
@required_login
def work_implementer_xiutu(request):
    problems = models.User.objects.filter(role="修图")
    dict = []
    for p in problems:
        dic = {}
        dic['name'] = p.username
        dict.append(dic)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
@required_login
def work_implementer_sheji(request):
    problems = models.User.objects.filter(role="设计")
    dict = []
    for p in problems:
        dic = {}
        dic['name'] = p.username
        dict.append(dic)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
@required_login
def work_implementer_xiaoshou(request):
    problems = models.User.objects.filter(role="销售")
    dict = []
    for p in problems:
        dic = {}
        dic['name'] = p.username
        dict.append(dic)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
@required_login
def work_implementer_wenan(request):
    problems = models.User.objects.filter(role="文案")
    dict = []
    for p in problems:
        dic = {}
        dic['name'] = p.username
        dict.append(dic)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
@required_login
def table_work_order_data(request):
    page = request.GET.get('page')
    rows = request.GET.get('limit')
    name = request.GET.get("search")
    shop_business_district = request.GET.get(
        'search_shop_business_district')  # 区域
    shop_category = request.GET.get('search_shop_category')  # 商圈
    shop_region = request.GET.get('search_shop_region')  # 品类
    username = request.GET.get('username')  # 品类
    sort = request.GET.get('sort')
    sortOrder = request.GET.get('sortOrder')
    username_problems = models.User.objects.filter(username=username)
    if username != None:
        username_dict = []
        for p in username_problems:
            dic = {}
            dic['role'] = p.role
            username_dict.append(dic)
        print(username_dict)
        username_role = username_dict[0]['role']
        print(username_role)
        problems = ''
        if sort != None:
            if sortOrder == 'asc':
                sortOrder = '-'
            else:
                sortOrder = ''
            if username_role == '设计':
                if name != None:
                    problems = models.Work_order.objects.filter(
                        work_implementer_sheji=username).filter(
                        Q(work_name__contains=name)
                        | Q(work_start_time=name)
                        | Q(work_deadline=name)
                        | Q(work_implementer_xiaoshou=name)
                        | Q(work_implementer_wenan=name)
                        | Q(work_implementer_sheji=name)
                        | Q(work_implementer_xiutu=name)
                        | Q(work_publisher=name)).order_by(sortOrder +
                                                           sort)
                else:
                    problems = models.Work_order.objects.filter(
                        work_implementer_sheji=username).order_by(sortOrder +
                                                                  sort)
                i = (int(page) - 1) * int(rows)
                j = (int(page) - 1) * int(rows) + int(rows)
                total = problems.count()
                problems = problems[i:j]
                # resultdict = {}
                # resultdict['total'] = total
                dict = []
                data = {"rows": dict, "total": total}
                for p in problems:
                    dic = {}
                    dic['id'] = p.id
                    dic['work_name'] = p.work_name
                    dic['work_start_time'] = p.work_start_time
                    dic['work_status'] = p.work_implementer_sheji_button
                    dic['work_publisher'] = p.work_publisher
                    dic['work_role'] = '设计'
                    dic['work_edit'] = p.work_edit
                    dict.append(dic)
                return HttpResponse(json.dumps(data),
                                    content_type="application/json")
            elif username_role == '修图':
                if name != None:
                    problems = models.Work_order.objects.filter(
                        work_implementer_xiutu=username).filter(
                        Q(work_name__contains=name)
                        | Q(work_start_time=name)
                        | Q(work_deadline=name)
                        | Q(work_implementer_xiaoshou=name)
                        | Q(work_implementer_wenan=name)
                        | Q(work_implementer_sheji=name)
                        | Q(work_implementer_xiutu=name)
                        | Q(work_publisher=name)).order_by(sortOrder +
                                                           sort)
                else:
                    problems = models.Work_order.objects.filter(
                        work_implementer_xiutu=username).order_by(sortOrder +
                                                                  sort)
                i = (int(page) - 1) * int(rows)
                j = (int(page) - 1) * int(rows) + int(rows)
                total = problems.count()
                problems = problems[i:j]
                # resultdict = {}
                # resultdict['total'] = total
                dict = []
                data = {"rows": dict, "total": total}
                for p in problems:
                    dic = {}
                    dic['id'] = p.id
                    dic['work_name'] = p.work_name
                    dic['work_start_time'] = p.work_start_time
                    dic['work_status'] = p.work_implementer_xiutu_button
                    dic['work_publisher'] = p.work_publisher
                    dic['work_role'] = '修图'
                    dic['work_edit'] = p.work_edit
                    dict.append(dic)
                return HttpResponse(json.dumps(data),
                                    content_type="application/json")
            elif username_role == '文案':
                if name != None:
                    problems = models.Work_order.objects.filter(
                        work_implementer_wenan=username).filter(
                        Q(work_name__contains=name)
                        | Q(work_start_time=name)
                        | Q(work_deadline=name)
                        | Q(work_implementer_xiaoshou=name)
                        | Q(work_implementer_wenan=name)
                        | Q(work_implementer_sheji=name)
                        | Q(work_implementer_xiutu=name)
                        | Q(work_publisher=name)).order_by(sortOrder +
                                                           sort)
                else:
                    problems = models.Work_order.objects.filter(
                        work_implementer_wenan=username).order_by(sortOrder +
                                                                  sort)
                i = (int(page) - 1) * int(rows)
                j = (int(page) - 1) * int(rows) + int(rows)
                total = problems.count()
                problems = problems[i:j]
                dict = []
                data = {"rows": dict, "total": total}
                for p in problems:
                    dic = {}
                    dic['id'] = p.id
                    dic['work_name'] = p.work_name
                    dic['work_start_time'] = p.work_start_time
                    dic['work_status'] = p.work_implementer_wenan_button
                    dic['work_publisher'] = p.work_publisher
                    dic['work_role'] = '文案'
                    dic['work_edit'] = p.work_edit
                    dict.append(dic)
                return HttpResponse(json.dumps(data),
                                    content_type="application/json")
        else:
            if username_role == '设计':
                if name != None:
                    problems = models.Work_order.objects.filter(
                        work_implementer_sheji=username).filter(
                        Q(work_name__contains=name)
                        | Q(work_start_time=name)
                        | Q(work_deadline=name)
                        | Q(work_implementer_xiaoshou=name)
                        | Q(work_implementer_wenan=name)
                        | Q(work_implementer_sheji=name)
                        | Q(work_implementer_xiutu=name)
                        | Q(work_publisher=name))
                else:
                    problems = models.Work_order.objects.filter(
                        work_implementer_sheji=username)
                i = (int(page) - 1) * int(rows)
                j = (int(page) - 1) * int(rows) + int(rows)
                total = problems.count()
                problems = problems[i:j]
                # resultdict = {}
                # resultdict['total'] = total
                dict = []
                data = {"rows": dict, "total": total}
                for p in problems:
                    dic = {}
                    dic['id'] = p.id
                    dic['work_name'] = p.work_name
                    dic['work_start_time'] = p.work_start_time
                    dic['work_status'] = p.work_implementer_sheji_button
                    dic['work_publisher'] = p.work_publisher
                    dic['work_role'] = '设计'
                    dic['work_edit'] = p.work_edit
                    dict.append(dic)
                return HttpResponse(json.dumps(data),
                                    content_type="application/json")
            elif username_role == '修图':
                if name != None:
                    problems = models.Work_order.objects.filter(
                        work_implementer_xiutu=username).filter(
                        Q(work_name__contains=name)
                        | Q(work_start_time=name)
                        | Q(work_deadline=name)
                        | Q(work_implementer_xiaoshou=name)
                        | Q(work_implementer_wenan=name)
                        | Q(work_implementer_sheji=name)
                        | Q(work_implementer_xiutu=name)
                        | Q(work_publisher=name))
                else:
                    problems = models.Work_order.objects.filter(
                        work_implementer_xiutu=username)
                i = (int(page) - 1) * int(rows)
                j = (int(page) - 1) * int(rows) + int(rows)
                total = problems.count()
                problems = problems[i:j]
                # resultdict = {}
                # resultdict['total'] = total
                dict = []
                data = {"rows": dict, "total": total}
                for p in problems:
                    dic = {}
                    dic['id'] = p.id
                    dic['work_name'] = p.work_name
                    dic['work_start_time'] = p.work_start_time
                    dic['work_status'] = p.work_implementer_xiutu_button
                    dic['work_publisher'] = p.work_publisher
                    dic['work_role'] = '修图'
                    dic['work_edit'] = p.work_edit
                    dict.append(dic)
                return HttpResponse(json.dumps(data),
                                    content_type="application/json")
            elif username_role == '文案':
                if name != None:
                    problems = models.Work_order.objects.filter(
                        work_implementer_wenan=username).filter(
                        Q(work_name__contains=name)
                        | Q(work_start_time=name)
                        | Q(work_deadline=name)
                        | Q(work_implementer_xiaoshou=name)
                        | Q(work_implementer_wenan=name)
                        | Q(work_implementer_sheji=name)
                        | Q(work_implementer_xiutu=name)
                        | Q(work_publisher=name))
                else:
                    problems = models.Work_order.objects.filter(
                        work_implementer_wenan=username)
                i = (int(page) - 1) * int(rows)
                j = (int(page) - 1) * int(rows) + int(rows)
                total = problems.count()
                problems = problems[i:j]
                dict = []
                data = {"rows": dict, "total": total}
                for p in problems:
                    dic = {}
                    dic['id'] = p.id
                    dic['work_name'] = p.work_name
                    dic['work_start_time'] = p.work_start_time
                    dic['work_status'] = p.work_implementer_wenan_button
                    dic['work_publisher'] = p.work_publisher
                    dic['work_role'] = '文案'
                    dic['work_edit'] = p.work_edit
                    dict.append(dic)
                return HttpResponse(json.dumps(data),
                                    content_type="application/json")
    else:
        if sort != None:
            if sortOrder == 'asc':
                sortOrder = '-'
            else:
                sortOrder = ''
            print('排序')
            if name == None:
                problems = models.Work_order.objects.order_by(sortOrder + sort)
            else:
                problems = models.Work_order.objects.filter(
                    Q(work_name__contains=name) | Q(work_start_time=name)
                    | Q(work_deadline=name)
                    | Q(work_implementer_xiaoshou=name)
                    | Q(work_implementer_wenan=name)
                    | Q(work_implementer_sheji=name)
                    | Q(work_implementer_xiutu=name)
                    | Q(work_publisher=name)).order_by(sortOrder + sort)
        else:
            if name == None:
                problems = models.Work_order.objects.all()
            else:
                problems = models.Work_order.objects.filter(
                    Q(work_name__contains=name) | Q(work_start_time=name)
                    | Q(work_deadline=name)
                    | Q(work_implementer_xiaoshou=name)
                    | Q(work_implementer_wenan=name)
                    | Q(work_implementer_sheji=name)
                    | Q(work_implementer_xiutu=name)
                    | Q(work_publisher=name))
        i = (int(page) - 1) * int(rows)
        j = (int(page) - 1) * int(rows) + int(rows)
        total = problems.count()
        problems = problems[i:j]
        # resultdict = {}
        # resultdict['total'] = total
        dict = []
        data = {"rows": dict, "total": total}
        for p in problems:
            dic = {}
            dic['id'] = p.id
            dic['work_name'] = p.work_name
            dic['work_start_time'] = p.work_start_time
            dic['work_deadline'] = p.work_deadline
            dic['work_implementer_sheji'] = p.work_implementer_sheji
            dic['work_implementer_wenan'] = p.work_implementer_wenan
            dic['work_implementer_xiutu'] = p.work_implementer_xiutu
            dic['work_implementer_sheji_button'] = p.work_implementer_sheji_button
            dic['work_implementer_wenan_button'] = p.work_implementer_wenan_button
            dic['work_implementer_xiutu_button'] = p.work_implementer_xiutu_button
            dic['work_implementer_xiaoshou'] = p.work_implementer_xiaoshou
            dic['work_publisher'] = p.work_publisher
            # dic['work_status'] = p.work_status
            dic['work_edit'] = p.work_edit
            dict.append(dic)
        return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
@required_login
def table_work_order_edit(request):
    resultdict = {}
    # now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # now_time = now_time[0:4] + now_time[5:7] + now_time[8:10]
    try:
        id = request.POST.get('id')
        role = request.POST.get('role')
        work_status = request.POST.get("work_status")
        work_edit = request.POST.get("work_edit")
    except:
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 0
        return JsonResponse(resultdict, safe=False)
    print('work_status', work_status)
    print(role)
    if role == "设计":
        shop_add = models.Work_order.objects.filter(id=id).update(
            work_implementer_sheji_button=work_status, work_edit=work_edit)
        problems = models.Work_order.objects.filter(id=id)
        dict = []
        for p in problems:
            dic = {}
            dic['work_implementer_sheji_button'] = p.work_implementer_sheji_button
            dic['work_implementer_wenan_button'] = p.work_implementer_wenan_button
            dic['work_implementer_xiutu_button'] = p.work_implementer_xiutu_button
            dict.append(dic)
        if dict[0]['work_implementer_sheji_button'] == "banner" and dict[0][
            'work_implementer_wenan_button'] == '套餐更新' and dict[0][
            'work_implementer_xiutu_button'] == "上传更新":
            today = datetime.date.today()
            print(today)
            models.Work_order.objects.filter(id=id).update(work_status="已完成",
                                                           work_deadline=today)
        if shop_add != None:
            resultdict['code'] = 0
            resultdict['msg'] = ""
            resultdict['state'] = 1
            return JsonResponse(resultdict, safe=False)
    elif role == "文案":
        shop_add = models.Work_order.objects.filter(id=id).update(
            work_implementer_wenan_button=work_status, work_edit=work_edit)
        problems = models.Work_order.objects.filter(id=id)
        dict = []
        for p in problems:
            dic = {}
            dic['work_implementer_sheji_button'] = p.work_implementer_sheji_button
            dic['work_implementer_wenan_button'] = p.work_implementer_wenan_button
            dic['work_implementer_xiutu_button'] = p.work_implementer_xiutu_button
            dict.append(dic)
        if dict[0]['work_implementer_sheji_button'] == "banner" and dict[0][
            'work_implementer_wenan_button'] == '套餐更新' and dict[0][
            'work_implementer_xiutu_button'] == "上传更新":
            today = datetime.date.today()
            print(today)
            models.Work_order.objects.filter(id=id).update(work_status="已完成",
                                                           work_deadline=today)
        if shop_add != None:
            resultdict['code'] = 0
            resultdict['msg'] = ""
            resultdict['state'] = 1
            return JsonResponse(resultdict, safe=False)
    elif role == "修图":
        shop_add = models.Work_order.objects.filter(id=id).update(
            work_implementer_xiutu_button=work_status, work_edit=work_edit)
        problems = models.Work_order.objects.filter(id=id)
        dict = []
        for p in problems:
            dic = {}
            dic['work_implementer_sheji_button'] = p.work_implementer_sheji_button
            dic['work_implementer_wenan_button'] = p.work_implementer_wenan_button
            dic['work_implementer_xiutu_button'] = p.work_implementer_xiutu_button
            dict.append(dic)
        if dict[0]['work_implementer_sheji_button'] == "banner" and dict[0][
            'work_implementer_wenan_button'] == '套餐更新' and dict[0][
            'work_implementer_xiutu_button'] == "上传更新":
            today = datetime.date.today()
            print(today)
            models.Work_order.objects.filter(id=id).update(work_status="已完成",
                                                           work_deadline=today)
        if shop_add != None:
            resultdict['code'] = 0
            resultdict['msg'] = ""
            resultdict['state'] = 1
            return JsonResponse(resultdict, safe=False)


@csrf_exempt
def category_data(request):
    administrative_district = request.POST.get('administrative_district')
    print(administrative_district)
    if administrative_district == None:
        meifa = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_region='美发')
        meirong = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_region='美容/SPA')
        meijiameijie = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_region='美甲美睫')
        yixuemeirong = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_region='医学美容')
        yujia = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_region='瑜伽')
        wudao = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_region='舞蹈')
        wenxiu = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_region='纹绣')
        shoushenqianti = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_region='瘦身纤体')
        wenshen = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_region='纹身')
        qudou = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_region='祛痘')
        huazhuangping = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_region='化妆品')
        chanhousuxing = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_region='产后塑形')
        yangfa = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_region='养发')
    else:
        meifa = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_business_district__contains=administrative_district[0:3],
            shop_region='美发')
        meirong = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_business_district__contains=administrative_district[0:3],
            shop_region='美容/SPA')
        meijiameijie = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_business_district__contains=administrative_district[0:3],
            shop_region='美甲美睫')
        yixuemeirong = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_business_district__contains=administrative_district[0:3],
            shop_region='医学美容')
        yujia = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_business_district__contains=administrative_district[0:3],
            shop_region='瑜伽')
        wudao = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_business_district__contains=administrative_district[0:3],
            shop_region='舞蹈')
        wenxiu = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_business_district__contains=administrative_district[0:3],
            shop_region='纹绣')
        shoushenqianti = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_business_district__contains=administrative_district[0:3],
            shop_region='瘦身纤体')
        wenshen = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_business_district__contains=administrative_district[0:3],
            shop_region='纹身')
        qudou = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_business_district__contains=administrative_district[0:3],
            shop_region='祛痘')
        huazhuangping = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_business_district__contains=administrative_district[0:3],
            shop_region='化妆品')
        chanhousuxing = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_business_district__contains=administrative_district[0:3],
            shop_region='产后塑形')
        yangfa = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_business_district__contains=administrative_district[0:3],
            shop_region='养发')
    dict = []
    dict.append(len(meifa))
    dict.append(len(meirong))
    dict.append(len(meijiameijie))
    dict.append(len(yixuemeirong))
    dict.append(len(yujia))
    dict.append(len(wudao))
    dict.append(len(wenxiu))
    dict.append(len(shoushenqianti))
    dict.append(len(wenshen))
    dict.append(len(qudou))
    dict.append(len(huazhuangping))
    dict.append(len(chanhousuxing))
    dict.append(len(yangfa))
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['data'] = dict
    resultdict['state'] = 1
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
@required_login
def table_work_order_add(request):
    resultdict = {}
    try:
        work_name = request.POST.get('work_name')
        work_start_time = request.POST.get('work_start_time')
        work_status = request.POST.get("work_status")
        work_deadline = request.POST.get("work_deadline")
        work_implementer_wenan = request.POST.get("work_implementer_wenan")
        work_implementer_sheji = request.POST.get("work_implementer_sheji")
        work_implementer_xiutu = request.POST.get("work_implementer_xiutu")
        work_implementer_xiaoshou = request.POST.get(
            "work_implementer_xiaoshou")
        work_publisher = request.POST.get("work_publisher")
        work_edit = request.POST.get("work_edit")
    except:
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 0
        return JsonResponse(resultdict, safe=False)
    shop_add = models.Work_order.objects.create(
        work_name=work_name,
        work_start_time=work_start_time,
        work_status=work_status,
        work_deadline=work_deadline,
        work_implementer_wenan=work_implementer_wenan,
        work_implementer_xiaoshou=work_implementer_xiaoshou,
        work_implementer_sheji=work_implementer_sheji,
        work_implementer_xiutu=work_implementer_xiutu,
        work_implementer_wenan_button='待开始',
        work_implementer_sheji_button='待开始',
        work_implementer_xiutu_button='待开始',
        work_publisher=work_publisher,
        work_edit=work_edit)
    if shop_add != None:
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)


# 添加新店数据
@csrf_exempt
@required_login
def table_simple_new_data_add(request):
    resultdict = {}
    try:
        shop_id = request.POST.get('shop_id')
        shop_name = request.POST.get('shop_name')
        shop_start = request.POST.get("shop_start")
        shop_review_count = request.POST.get("shop_review_count")
        shop_per_capita_consumption = request.POST.get(
            "shop_per_capita_consumption")
        shop_effect = request.POST.get("shop_effect")
        shop_service = request.POST.get("shop_service")
        shop_surroundings = request.POST.get("shop_surroundings")
        shop_region = request.POST.get("shop_region")
        shop_business_district = request.POST.get("shop_business_district")
        shop_category = request.POST.get("shop_category")
        shop_address = request.POST.get("shop_address")
        shop_telephonenumber = request.POST.get("shop_telephonenumber")
        shop_edit = request.POST.get("shop_edit")
    except:
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 0
        return JsonResponse(resultdict, safe=False)
    shop_add = models.Dazhongdianping_liren_new_all_data.objects.create(
        shop_id=shop_id,
        shop_name=shop_name,
        shop_per_capita_consumption=shop_per_capita_consumption,
        shop_review_count=shop_review_count,
        shop_effect=shop_effect,
        shop_start=shop_start,
        shop_service=shop_service,
        shop_surroundings=shop_surroundings,
        shop_region=shop_region,
        shop_business_district=shop_business_district,
        shop_category=shop_category,
        shop_telephonenumber=shop_telephonenumber,
        shop_address=shop_address,
        shop_edit=shop_edit)
    if shop_add != None:
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)


def get_cities(request):
    username = request.GET.get('username')
    cityies = models.Dazhongdianping_liren_user_data.objects.filter(
        username=username)
    dict_city = []
    for c in cityies:
        dict_city.append(c.shop_city)
    dict_city = list(set(dict_city))
    dict = []
    for d in dict_city:
        dict.append({'label': d, 'id': d})
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


# 全部商户数据显示
@csrf_exempt
# @required_login
def table_simple_data(request):
    page = request.GET.get('currentPage')
    rows = request.GET.get('pagesize')
    shop_business_district = request.GET.get('shop_business_district')  # 区域
    shop_category = request.GET.get('shop_category')  # 商圈
    shop_region = request.GET.get('shop_region')  # 品类
    shop_type = request.GET.get('shop_type')  # 类型
    order = request.GET.get('order')
    city = request.GET.get('city')
    name = request.GET.get("search")
    if shop_business_district == None or str(shop_business_district) == 'None' or len(shop_business_district) == 2:
        shop_business_district = '区域'
    else:
        shop_business_district = eval(shop_business_district)
    if shop_category == None or str(shop_category) == 'None' or len(shop_category) == 2:
        shop_category = '商圈'
    else:
        shop_category = eval(shop_category)
    if shop_region == None or str(shop_region) == 'None' or len(shop_region) == 2:
        shop_region = '行业'
    else:
        shop_region = eval(shop_region)
    if '[' in str(shop_region) or '[' in str(shop_category) or '[' in str(shop_business_district):
        if order == 'descending':
            # 搜索逻辑
            # 区域和商圈等于空
            if shop_business_district == None or str(shop_business_district) == 'None':
                shop_business_district = '区域'
            if shop_category == None or str(shop_business_district) == 'None':
                shop_category = '商圈'
            if shop_region == None or str(shop_region) == 'None':
                shop_region == '行业'
            if name != '' and name != None:
                if name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district, shop_category__in=shop_category,
                        shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district, shop_category__in=shop_category,
                        shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district,
                        shop_categoiry__in=shop_category, shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region, shop_category__in=shop_category,
                        shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_category__in=shop_category, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region, shop_category__in=shop_category,
                        shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_category__in=shop_category, shop_tags__contains=shop_type,
                        shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region=shop_region, shop_tags__contains=shop_type,
                        shop_city=city)
            # 搜索逻辑
            # 区域和商圈等于空
            else:
                if shop_business_district == '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 商圈和品类等于空
                elif shop_business_district != '区域' and shop_category == '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    print('进来了')
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 区域和品类等于空
                elif shop_category != '商圈' and shop_region != '行业' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 区域和商圈不等于空
                elif shop_business_district != '区域' and shop_category != '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 商圈和品类不等于空
                elif shop_region != '行业' and shop_category != '商圈' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 区域和品类不等于空
                elif shop_business_district != '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                elif shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                elif shop_category != '商圈' and shop_business_district == '区域' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 类型不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 类型和品类不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 类型和城区不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 类型和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 类型和品类和城区不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 类型和城区和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=shop_category,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 类型和商圈和品类
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('id').order_by('-shop_telephonenumber')
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        shop_category=shop_category,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                elif shop_type != 'None' and shop_region != 'None' and shop_business_district != 'None' and shop_category != 'None':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                    ).order_by('-id').order_by('-shop_telephonenumber')
                elif shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.all(
                    ).order_by('-id').order_by('-shop_telephonenumber')
        elif order == 'ascending':
            # 搜索逻辑
            # 区域和商圈等于空
            if shop_business_district == None or str(shop_business_district) == 'None':
                shop_business_district = '区域'
            if shop_category == None or str(shop_business_district) == 'None':
                shop_category = '商圈'
            if shop_region == None or str(shop_region) == 'None':
                shop_region == '行业'
            if name != '' and name != None:
                if name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    print('数据', name)
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region=shop_region, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region=shop_region,
                        shop_business_district__in=shop_business_district, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region=shop_region,
                        shop_business_district__in=shop_business_district, shop_category__in=shop_category,
                        shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region=shop_region,
                        shop_business_district__in=shop_business_district, shop_category__in=shop_category,
                        shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category, shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region=shop_region, shop_category__in=shop_category,
                        shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_category__in=shop_category, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region=shop_region, shop_category__in=shop_category,
                        shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_category__in=shop_category, shop_tags__contains=shop_type,
                        shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region=shop_region, shop_tags__contains=shop_type,
                        shop_city=city)
            # 搜索逻辑
            # 区域和商圈等于空
            else:
                if shop_business_district == '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 商圈和品类等于空
                elif shop_business_district != '区域' and shop_category == '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 区域和品类等于空
                elif shop_category != '商圈' and shop_region != '行业' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 区域和商圈不等于空
                elif shop_business_district != '区域' and shop_category != '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 商圈和品类不等于空
                elif shop_region != '行业' and shop_category != '商圈' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 区域和品类不等于空
                elif shop_business_district != '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif shop_category != '商圈' and shop_business_district == '区域' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和品类不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和城区不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和品类和城区不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和城区和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=shop_category,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和商圈和品类
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('id').order_by(
                        'shop_telephonenumber')
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        shop_category=shop_category,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif shop_type != 'None' and shop_region != 'None' and shop_business_district != 'None' and shop_category != 'None':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(shop_city=city
                                                                                    ).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(shop_city=city
                                                                                    ).order_by('-id').order_by(
                        'shop_telephonenumber')
        else:
            if shop_business_district == None or str(shop_business_district) == 'None':
                shop_business_district = '区域'
            if shop_category == None or str(shop_business_district) == 'None':
                shop_category = '商圈'
            if shop_region == None or str(shop_region) == 'None':
                shop_region == '行业'
            if name != '' and name != None:
                if name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district, shop_category__in=shop_category,
                        shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district, shop_category__in=shop_category,
                        shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category, shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region, shop_category__in=shop_category,
                        shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_category__in=shop_category, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region, shop_category__in=shop_category,
                        shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_category__in=shop_category, shop_tags__contains=shop_type,
                        shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_tags__contains=shop_type, shop_city=city)
            # 搜索逻辑
            # 区域和商圈等于空
            else:
                # 搜索逻辑
                # 区域和商圈等于空
                if shop_business_district == '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id')
                # 商圈和品类等于空
                elif shop_business_district != '区域' and shop_category == '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id')
                # 区域和品类等于空
                elif shop_category != '商圈' and shop_region != '行业' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_category__id=shop_category,
                        shop_city=city).order_by('-id')
                # 区域和商圈不等于空
                elif shop_business_district != '区域' and shop_category != '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id')
                # 商圈和品类不等于空
                elif shop_region != '行业' and shop_category != '商圈' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id')
                # 区域和品类不等于空
                elif shop_business_district != '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id')
                elif shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id')
                elif shop_category != '商圈' and shop_business_district == '区域' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id')
                # 类型不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_city=city).order_by('-id')
                # 类型和品类不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id')
                # 类型和城区不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id')
                # 类型和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id')
                # 类型和品类和城区不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id')
                # 类型和城区和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=shop_category,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id')
                # 类型和商圈和品类
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_category__contains__in=shop_category,
                        shop_city=city).order_by('id')
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_category__in=shop_category,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id')
                elif shop_type != 'None' and shop_region != 'None' and shop_business_district != 'None' and shop_category != 'None':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(shop_city=city
                                                                                    ).order_by('-id')
                elif shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(shop_city=city
                                                                                    ).order_by('-id')
    else:
        if order == 'descending':
            # 搜索逻辑
            # 区域和商圈等于空
            if shop_business_district == None or str(shop_business_district) == 'None':
                shop_business_district = '区域'
            if shop_category == None or str(shop_business_district) == 'None':
                shop_category = '商圈'
            if shop_region == None or str(shop_region) == 'None':
                shop_region == '行业'
            if name != '' and name != None:
                if name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district, shop_category__in=shop_category,
                        shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district, shop_category__in=shop_category,
                        shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category, shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region, shop_category__in=shop_category,
                        shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_category__in=shop_category, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region, shop_category__in=shop_category,
                        shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_category__in=shop_category, shop_tags__contains=shop_type,
                        shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region=shop_region, shop_tags__contains=shop_type,
                        shop_city=city)
            # 搜索逻辑
            # 区域和商圈等于空
            else:
                if shop_business_district == '区域' and shop_region != '行业' and shop_region != None and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 商圈和品类等于空
                elif shop_business_district != '区域' and shop_category == '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    print('进来了')
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 区域和品类等于空
                elif shop_category != '商圈' and shop_region != '行业' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 区域和商圈不等于空
                elif shop_business_district != '区域' and shop_category != '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 商圈和品类不等于空
                elif shop_region != '行业' and shop_category != '商圈' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 区域和品类不等于空
                elif shop_business_district != '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                elif shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                elif shop_category != '商圈' and shop_business_district == '区域' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 类型不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 类型和品类不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 类型和城区不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 类型和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 类型和品类和城区不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 类型和城区和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=shop_category,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                # 类型和商圈和品类
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('id').order_by('-shop_telephonenumber')
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        shop_category=shop_category,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by('-shop_telephonenumber')
                elif shop_type != 'None' and shop_region != 'None' and shop_business_district != 'None' and shop_category != 'None':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(shop_city=city
                                                                                    ).order_by('-id').order_by(
                        '-shop_telephonenumber')
                elif shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.all(shop_city=city
                                                                                 ).order_by('-id').order_by(
                        '-shop_telephonenumber')
        elif order == 'ascending':
            # 搜索逻辑
            # 区域和商圈等于空
            if shop_business_district == None or str(shop_business_district) == 'None':
                shop_business_district = '区域'
            if shop_category == None or str(shop_business_district) == 'None':
                shop_category = '商圈'
            if shop_region == None or str(shop_region) == 'None':
                shop_region == '行业'
            if name != '' and name != None:
                if name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    print('数据', name)
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region=shop_region, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region=shop_region,
                        shop_business_district__in=shop_business_district, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region=shop_region,
                        shop_business_district__in=shop_business_district, shop_category__in=shop_category,
                        shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region=shop_region,
                        shop_business_district__in=shop_business_district, shop_category__in=shop_category,
                        shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category, shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region=shop_region, shop_category__in=shop_category,
                        shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_category__in=shop_category, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region=shop_region, shop_category__in=shop_category,
                        shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_category__in=shop_category, shop_tags__contains=shop_type,
                        shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region=shop_region, shop_tags__contains=shop_type,
                        shop_city=city)
            # 搜索逻辑
            # 区域和商圈等于空
            else:
                if shop_business_district == '区域' and shop_region != '行业' and shop_region != None and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 商圈和品类等于空
                elif shop_business_district != '区域' and shop_category == '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 区域和品类等于空
                elif shop_category != '商圈' and shop_region != '行业' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 区域和商圈不等于空
                elif shop_business_district != '区域' and shop_category != '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 商圈和品类不等于空
                elif shop_region != '行业' and shop_category != '商圈' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 区域和品类不等于空
                elif shop_business_district != '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif shop_category != '商圈' and shop_business_district == '区域' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和品类不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和城区不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和品类和城区不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和城区和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=shop_category,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和商圈和品类
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('id').order_by(
                        'shop_telephonenumber')
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        shop_category=shop_category,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif shop_type != 'None' and shop_region != 'None' and shop_business_district != 'None' and shop_category != 'None':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(shop_city=city
                                                                                    ).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(shop_city=city
                                                                                    ).order_by('-id').order_by(
                        'shop_telephonenumber')
        else:
            if shop_business_district == None or str(shop_business_district) == 'None':
                shop_business_district = '区域'
            if shop_category == None or str(shop_business_district) == 'None':
                shop_category = '商圈'
            if shop_region == None or str(shop_region) == 'None':
                shop_region == '行业'
            if name != '' and name != None:
                if name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district, shop_category__in=shop_category,
                        shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district, shop_category__in=shop_category,
                        shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category, shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region, shop_category__in=shop_category,
                        shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_category__in=shop_category, shop_city=city)
                elif name != None and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_region__in=shop_region, shop_category__in=shop_category,
                        shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_category__in=shop_category, shop_tags__contains=shop_type,
                        shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_name__icontains=name, shop_tags__contains=shop_type, shop_city=city)
                elif name != None and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type != '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(shop_city=city,
                                                                                    shop_name__icontains=name,
                                                                                    shop_tags__contains=shop_type)
            # 搜索逻辑
            # 区域和商圈等于空
            else:
                # 搜索逻辑
                # 区域和商圈等于空
                if shop_business_district == '区域' and shop_region != '行业' and shop_region != None and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id')
                # 商圈和品类等于空
                elif shop_business_district != '区域' and shop_category == '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id')
                # 区域和品类等于空
                elif shop_category != '商圈' and shop_region != '行业' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_category__id=shop_category,
                        shop_city=city).order_by('-id')
                # 区域和商圈不等于空
                elif shop_business_district != '区域' and shop_category != '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id')
                # 商圈和品类不等于空
                elif shop_region != '行业' and shop_category != '商圈' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id')
                # 区域和品类不等于空
                elif shop_business_district != '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_business_district__in=shop_business_district,
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id')
                elif shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district,
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id')
                elif shop_category != '商圈' and shop_business_district == '区域' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id')
                # 类型不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_city=city).order_by('-id')
                # 类型和品类不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_city=city).order_by('-id')
                # 类型和城区不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id')
                # 类型和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=shop_category,
                        shop_city=city).order_by('-id')
                # 类型和品类和城区不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id')
                # 类型和城区和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=shop_category,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id')
                # 类型和商圈和品类
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_category__contains__in=shop_category,
                        shop_city=city).order_by('id')
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=shop_region,
                        shop_category__in=shop_category,
                        shop_business_district__in=shop_business_district,
                        shop_city=city).order_by('-id')
                elif shop_type != 'None' and shop_region != 'None' and shop_business_district != 'None' and shop_category != 'None':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(shop_city=city
                                                                                    ).order_by('-id')
                elif shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_all_data.objects.filter(shop_city=city
                                                                                    ).order_by('-id')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    total = problems.count()
    problems = problems[i:j]
    dict = []
    data = {"rows": dict, "total": total}
    for p in problems:
        dic = {}
        dic['shop_id'] = p.shop_id
        dic['shop_name'] = p.shop_name
        dic['shop_start'] = p.shop_start
        dic['shop_review_count'] = p.shop_review_count
        dic['shop_bad_review'] = p.shop_bad_review
        dic['shop_per_capita_consumption'] = p.shop_per_capita_consumption
        dic['shop_region'] = p.shop_region
        dic['shop_effect'] = p.shop_effect
        dic['shop_service'] = p.shop_service
        dic['shop_surroundings'] = p.shop_surroundings
        dic['shop_business_district'] = p.shop_business_district
        dic['shop_category'] = p.shop_category
        dic['shop_address'] = p.shop_address
        dic['shop_telephonenumber'] = p.shop_telephonenumber
        if p.shop_tags != None:
            dic['shop_tags'] = p.shop_tags[0:2]
        else:
            dic['shop_tags'] = p.shop_tags
        dic['shop_kp_name'] = p.shop_kp_name
        dic['shop_kp_position'] = p.shop_kp_position
        dic['shop_kp_wechat_id'] = p.shop_kp_wechat_id
        dic['shop_kp_category'] = p.shop_kp_category
        dic['shop_kp_city'] = p.shop_kp_city
        dic['shop_add_form'] = p.shop_add_form
        dic['shop_edit'] = p.shop_edit
        dic['shop_city'] = p.shop_city
        dict.append(dic)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    resultdict['total'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


def get_shop_edit_pull(request):
    shop_id = request.GET.get('shop_id')
    print('id', shop_id)
    a = models.Dazhongdianping_liren_all_data.objects.filter(shop_id=shop_id)
    print('备注备注', a, a[0].shop_edit)
    edit = ''
    for i in a:
        edit += i.shop_edit
    print(edit)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['data'] = edit
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def delete_visit(request):
    id = request.GET.get('id')
    problems = models.My_visit.objects.filter(id=id).delete()
    resultdict = {}
    if problems != None:
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 1
    else:
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 2
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def table_simple_visit(request):
    page = request.GET.get('currentPage')
    rows = request.GET.get('pagesize')
    username = request.GET.get('username')
    print(page)
    print(rows)
    print(username)
    problems = models.My_visit.objects.filter(
        visit_name=username).order_by('-id')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    total = problems.count()
    problems = problems[i:j]
    dict = []
    data = {"rows": dict, "total": total}
    for p in problems:
        dic = {}
        dic['id'] = p.id
        dic['visit_id'] = p.visit_id
        dic['visit_shop_name'] = p.visit_shop_name
        dic['visit_time'] = p.visit_time
        dic['visit_name'] = p.visit_name
        dic['visit_data'] = eval(p.visit_data)
        dict.append(dic)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    resultdict['total'] = total
    resultdict['data'] = dict
    print(dict)
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def get_to_do(request):
    username = request.GET.get('username')
    shop_name = request.GET.get('shop_name')
    # 月份
    month = request.GET.get('month')
    try:
        order = models.Order.objects.filter(order_contract_sales=username)
        money = 0  # 订单金额
        for p in order:
            if month == p.order_date[0:7]:
                money += int(p.order_amount)
        # 计算提成点
        commission_point = 0
        commission_point_data = models.Setting_storage.objects.all()
        todo_count = 0
        todo_count_number = 0
        commission_point_json = ''
        for c in commission_point_data:
            commission_point_json = c.commission_form
        count = []
        for o in eval(commission_point_json):
            count.append(int(o['commission_performance']))
        for a in sorted(count):
            if money >= a:
                for o in eval(commission_point_json):
                    if a == int(o['commission_performance']):
                        commission_point = int(o['commission_commission_point'])
            else:
                performance = 0
        Order = models.Order.objects.filter(order_contract_sales=username)
        for a in Order:
            money2 = int(a.order_amount) - int(a.cost_fees)
            if month == str(a.order_date[0:7]):
                todo_count = models.To_do.objects.filter(
                    order_id=a.contract_id).count()
                pending_review_count = models.Pending_review.objects.filter(
                    order_id=a.contract_id).count()
                completed_count = models.Completed.objects.filter(
                    order_id=a.contract_id).count()
                count = todo_count + pending_review_count + completed_count
                print(a.sign_contract_shop)
                models.To_do.objects.filter(order_id=a.contract_id).update(
                    money=math.floor(int(money2 * commission_point / 100 / 3 / count)))
                models.Pending_review.objects.filter(
                    order_id=a.contract_id).update(
                    money=math.floor(int(money2 * commission_point / 100 / 3 / count)))
                models.Completed.objects.filter(
                    order_id=a.contract_id).update(
                    money=math.floor(int(money2 * commission_point / 100 / 3 / count)))
        dict = []
        print('username', username)
        print('shop_name', shop_name)
        print('month', month)
        if shop_name == '待办事项':
            problems = models.To_do.objects.filter(
                username=username, time__icontains=month).order_by('-id')
        else:
            problems = models.To_do.objects.filter(
                username=username, shop_name=shop_name, time__icontains=month).order_by('-id')

        # print(d1)
        for p in problems:
            order_date_year = int(p.time[0:4])
            order_date_month = int(p.time[5:7])
            if '0' == p.time[5:6]:
                order_date_month = int(p.time[6:7])
            order_date_day = int(p.time[8:10])
            if '0' == p.time[8:9]:
                order_date_day = int(p.time[9:10])
            a = datetime.date(order_date_year, order_date_month, order_date_day)
            if '-' not in str(datetime.date.today() - a):
                dict.append({
                    'project': p.project,
                    'shop_name': p.shop_name,
                    'time': p.time,
                    'money': p.money,
                    'schedule': p.schedule,
                    'username': p.username,
                    'status': '已过期',
                    'order_id': p.order_id,
                    'edit': p.edit
                })
            else:
                dict.append({
                    'project': p.project,
                    'shop_name': p.shop_name,
                    'time': p.time,
                    'money': p.money,
                    'schedule': p.schedule,
                    'username': p.username,
                    'status': p.status,
                    'order_id': p.order_id,
                    'edit': p.edit
                })
        dict = sorted(dict, key=lambda keys: keys['time'])
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 1
        resultdict['data'] = dict
        return JsonResponse(resultdict, safe=False)
    except:
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)


@csrf_exempt
def get_benyuejiangjing(request):
    page = request.GET.get('currentPage')
    rows = request.GET.get('pagesize')
    username = request.GET.get('username')
    month = request.GET.get('month')
    print(username)
    print(month)
    print(page)
    print(rows)
    to_do = models.To_do.objects.filter(username=username,
                                        time__contains=month).order_by('-id')
    pending_review = models.Pending_review.objects.filter(
        username=username, time__contains=month).order_by('-id')
    completed = models.Completed.objects.filter(
        username=username, time__contains=month).order_by('-id')
    dict = []
    total = 0
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    total = total + to_do.count() + pending_review.count() + completed.count()
    if to_do != '<QuerySet []>':
        for t in to_do:
            order_date_year = int(t.time[0:4])
            order_date_month = int(t.time[5:7])
            if '0' == t.time[5:6]:
                order_date_month = int(t.time[6:7])
            order_date_day = int(t.time[8:10])
            if '0' == t.time[8:9]:
                order_date_day = int(t.time[9:10])
            a = datetime.date(order_date_year, order_date_month, order_date_day)
            if '-' not in str(datetime.date.today() - a):
                print('shop_name', t.shop_name)
                dict.append({
                    'project': t.project,
                    'shop_name': t.shop_name,
                    'time': t.time,
                    'money': t.money,
                    "status": '已过期'
                })
            elif '-' in str(datetime.date.today() - a):
                dict.append({
                    'project': t.project,
                    'shop_name': t.shop_name,
                    'time': t.time,
                    'money': t.money,
                    "status": '未完成'
                })
    if pending_review != '<QuerySet []>':
        for p in pending_review:
            dict.append({
                'project': p.project,
                'shop_name': p.shop_name,
                'time': p.time,
                'money': p.money,
                "status": '待审核'
            })
    if completed != '<QuerySet []>':
        for c in completed:
            dict.append({
                'project': c.project,
                'shop_name': c.shop_name,
                'time': c.time,
                'money': c.money,
                "status": '已完成'
            })
    dict = dict[i:j]
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    resultdict['total'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def get_benyueyeji(request):
    page = request.GET.get('currentPage')
    rows = request.GET.get('pagesize')
    username = request.GET.get('username')
    month = request.GET.get('month')
    order_data = models.Order.objects.filter(
        order_contract_sales=username,
        order_date__contains=month).order_by('-id')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    total = order_data.count()
    order_data = order_data[i:j]
    dict = []
    for p in order_data:
        dict.append({
            'contract_id': p.contract_id,
            'order_date': p.order_date[0:10],
            'order_start_date': p.order_start_date[0:10],
            'sign_contract_shop': p.sign_contract_shop,
            'customer_source': p.customer_source,
            'contract_status': p.contract_status,
            'contracted_projects': p.contracted_projects,
            'shop_industry': p.shop_industry,
            'shop_kp_name': p.shop_kp_name,
            'shop_telephonenumber': p.shop_telephonenumber,
            'order_numbers': p.order_numbers,
            'shop_cooperation_duration': p.shop_cooperation_duration,
            'order_end_date': p.order_end_date,
            'order_amount': p.order_amount,
            'cost_fees': p.cost_fees,
            'city': p.city,
            'payment_method': p.payment_method,
            'order_contract_sales': p.order_contract_sales,
            'shop_remark': p.shop_remark,
            'shop_id': p.shop_id,
            'order_form': eval(p.order_form),
            'tags': p.tags
        })
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    resultdict['total'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def get_benyuejiangjing_xiayue(request):
    page = request.GET.get('currentPage')
    rows = request.GET.get('pagesize')
    username = request.GET.get('username')
    month = request.GET.get('month')
    month = datetime.datetime.strptime(month + '-01', '%Y-%m-%d')
    month = last_day_of_month(month)
    month = str(month + datetime.timedelta(days=1))[0:7]
    to_do = models.To_do.objects.filter(username=username,
                                        time__contains=month).order_by('-id')
    pending_review = models.Pending_review.objects.filter(
        username=username, time__contains=month).order_by('-id')
    completed = models.Completed.objects.filter(
        username=username, time__contains=month).order_by('-id')
    dict = []
    total = 0
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    total = total + to_do.count() + pending_review.count() + completed.count()
    if to_do != '<QuerySet []>':
        for t in to_do:
            order_date_year = int(t.time[0:4])
            order_date_month = int(t.time[5:7])
            if '0' == t.time[5:6]:
                order_date_month = int(t.time[6:7])
            order_date_day = int(t.time[8:10])
            if '0' == t.time[8:9]:
                order_date_day = int(t.time[9:10])
            a = datetime.date(order_date_year, order_date_month, order_date_day)
            if '-' not in str(datetime.date.today() - a):
                print('shop_name', t.shop_name)
                dict.append({
                    'project': t.project,
                    'shop_name': t.shop_name,
                    'time': t.time,
                    'money': t.money,
                    "status": '已过期'
                })
            elif '-' in str(datetime.date.today() - a):
                dict.append({
                    'project': t.project,
                    'shop_name': t.shop_name,
                    'time': t.time,
                    'money': t.money,
                    "status": '未完成'
                })
    if pending_review != '<QuerySet []>':
        for p in pending_review:
            dict.append({
                'project': p.project,
                'shop_name': p.shop_name,
                'time': p.time,
                'money': p.money,
                "status": '待审核'
            })
    if completed != '<QuerySet []>':
        for c in completed:
            dict.append({
                'project': c.project,
                'shop_name': c.shop_name,
                'time': c.time,
                'money': c.money,
                "status": '已完成'
            })
    dict = dict[i:j]
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    resultdict['total'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def get_pending_review(request):
    username = request.GET.get('username')
    shop_name = request.GET.get('shop_name')
    month = request.GET.get('month')

    if shop_name == '待审核事项':
        problems = models.Pending_review.objects.filter(
            username=username, time__contains=month).order_by('-id')
    else:
        problems = models.Pending_review.objects.filter(
            username=username, shop_name=shop_name, time__contains=month).order_by('-id')
    dict = []
    for p in problems:
        dict.append({
            'project': p.project,
            'shop_name': p.shop_name,
            'status': p.status,
            'time': p.time,
            'money': p.money,
            'schedule': p.schedule,
            'username': p.username,
            'submitter': p.submitter,
            'success_time': p.success_time,
            'submit_time': p.submit_time,
            "edit": p.edit,
            'order_id': p.order_id
        })
    dict = sorted(dict, key=lambda keys: keys['time'], reverse=True)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def get_completed(request):
    username = request.GET.get('username')
    shop_name = request.GET.get('shop_name')
    month = request.GET.get('month')
    print(username)
    print('日期', month)
    if shop_name == '已完成事项':
        problems = models.Completed.objects.filter(
            username=username, time__contains=month).order_by('-id')
    else:
        problems = models.Completed.objects.filter(
            username=username, shop_name=shop_name, time__contains=month).order_by('-id')
    dict = []
    for p in problems:
        dict.append({
            'project': p.project,
            'shop_name': p.shop_name,
            'status': p.status,
            'time': p.time,
            'money': p.money,
            'schedule': p.schedule,
            'username': p.username,
            'submitter': p.submitter,
            'success_time': p.success_time,
            'submit_time': p.submit_time,
            'order_id': p.order_id
        })
    dict = sorted(dict, key=lambda keys: keys['time'], reverse=True)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def post_completed(request):
    project = request.GET.get('project')
    shop_name = request.GET.get('shop_name')
    time = request.GET.get('time')
    money = request.GET.get('money')
    schedule = request.GET.get('schedule')
    username = request.GET.get('username')
    submitter = request.GET.get('submitter')
    order_id = request.GET.get('order_id')
    submit_time = request.GET.get('submit_time')
    success_time = datetime.date.today()
    completed = models.Completed.objects.filter(shop_name=shop_name)
    tp_do = models.To_do.objects.filter(shop_name=shop_name)
    pending_review = models.Pending_review.objects.filter(shop_name=shop_name)
    count = len(completed) + len(tp_do) + len(pending_review)
    schedule = int(float(schedule)) + (100 / count)
    problems = models.Completed.objects.create(project=project,
                                               shop_name=shop_name,
                                               time=time,
                                               money=money,
                                               schedule=int(schedule),
                                               order_id=order_id,
                                               username=username,
                                               submitter=submitter,
                                               status='已完成',
                                               submit_time=submit_time,
                                               success_time=success_time)
    if problems != None:
        models.Pending_review.objects.filter(project=project,
                                             shop_name=shop_name,
                                             time=time).delete()
        models.Completed.objects.filter(shop_name=shop_name).update(
            schedule=schedule)
        models.To_do.objects.filter(shop_name=shop_name).update(
            schedule=schedule)
        models.Pending_review.objects.filter(shop_name=shop_name).update(
            schedule=schedule)
        db = pymysql.connect("localhost", "root", "bakj123456", "rock")
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM user_userprofile where first_name = '" + username + "'")
        data = cursor.fetchall()
        username = data[0][4]
        wx = WeChat()
        wx.send_data('任务审核成功通知\n'
                     '店名：' + shop_name + '\n'
                                         '任务名：' + project + '\n'
                                                            '审核通过时间：' + str(success_time) + '\n', username)
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)


@csrf_exempt
def audit_failure(request):
    project = request.GET.get('project')
    shop_name = request.GET.get('shop_name')
    time = request.GET.get('time')
    money = request.GET.get('money')
    order_id = request.GET.get('order_id')
    schedule = request.GET.get('schedule')
    username = request.GET.get('username')
    edit = request.GET.get('edit')
    success_time = datetime.date.today()
    problems = models.To_do.objects.create(project=project,
                                           shop_name=shop_name,
                                           time=time,
                                           money=money,
                                           schedule=schedule,
                                           username=username,
                                           order_id=order_id,
                                           edit=edit,
                                           status='审核未通过')
    if problems != None:
        models.Pending_review.objects.filter(project=project,
                                             shop_name=shop_name,
                                             time=time).delete()
        db = pymysql.connect("localhost", "root", "bakj123456", "rock")
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM user_userprofile where first_name = '" + username + "'")
        data = cursor.fetchall()
        username = data[0][4]
        wx = WeChat()
        wx.send_data('任务审核失败通知\n'
                     '店名：' + shop_name + '\n'
                                         '任务名：' + project + '\n'
                                                            '审核时间：' + str(success_time) + '\n'
                                                                                          '备注：' + str(edit) + '\n',
                     username)
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)


@csrf_exempt
def table_simple_pending_review(request):
    page = request.GET.get('currentPage')
    rows = request.GET.get('pagesize')
    name_data = request.GET.get('name')
    username = request.GET.get('username')
    xsname = request.GET.get('xiaoshou')
    print(xsname)
    if username == '超级管理员':
        db = pymysql.connect("localhost", "root", "bakj123456", "rock")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM user_userprofile where avatar = 'admin'")
        data = cursor.fetchall()
        xsname = []
        for i in data:
            xsname.append(i[5])
        problems = models.Pending_review.objects.filter(username__in=xsname)
    else:
        db = pymysql.connect("localhost", "root", "bakj123456", "rock")
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM user_userprofile WHERE first_name='" + username + "'")
        data = cursor.fetchall()
        group = data[0][14]
        cursor2 = db.cursor()
        cursor2.execute(
            "SELECT * FROM user_userprofile WHERE group_name='" + group + "'")
        data2 = cursor2.fetchall()
        name = []
        for row in data2:
            name.append(row[5])
        print('name', name)
        db.close()
        cursor2.close()
        if name_data == '':
            problems = models.Pending_review.objects.all(
                Q(project__contains=name_data)
                | Q(shop_name__contains=name_data), username__in=name)
        else:
            problems = models.Pending_review.objects.filter(username__in=name)
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    total = problems.count()
    problems = problems[i:j]
    dict = []
    for p in problems:
        dict.append({
            'project': p.project,
            'shop_name': p.shop_name,
            'time': p.time,
            'money': p.money,
            'schedule': p.schedule,
            'username': p.username,
            'submitter': p.submitter,
            'success_time': p.success_time,
            'submit_time': p.submit_time,
            "edit": p.edit,
            "lat": p.lat,
            "lng": p.lng,
            "order_id": p.order_id,
            'url': p.url
        })
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    resultdict['total'] = total
    resultdict['data'] = dict
    print(dict)
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def table_simple_to_do(request):
    page = request.GET.get('currentPage')
    rows = request.GET.get('pagesize')
    suatus = request.GET.get('suatus')
    username = request.GET.get('username')
    name = request.GET.get('name')
    data = request.GET.get('data')
    db = pymysql.connect("localhost", "root", "bakj123456", "rock")
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM user_userprofile WHERE first_name='" + name + "'")
    data = cursor.fetchall()
    group = data[0][14]
    if name == '超级管理员':
        cursor2 = db.cursor()
        cursor2.execute("SELECT * FROM user_userprofile")
    else:
        cursor2 = db.cursor()
        cursor2.execute(
            "SELECT * FROM user_userprofile WHERE group_name='" + group + "'")
    data2 = cursor2.fetchall()
    name_data = []
    for row in data2:
        name_data.append(row[5])
    if name == '超级管理员':
        pass
    else:
        name_data.remove(name)
    if username == '' and group != '销售':
        problems_todo = models.To_do.objects.filter(
            username__in=name_data).order_by('-id')
        problems_completed = models.Completed.objects.filter(
            username__in=name_data).order_by('-id')
        problems_pending_review = models.Pending_review.objects.filter(
            username__in=name_data).order_by('-id')
    else:
        problems_todo = models.To_do.objects.filter(
            username=username).order_by('-id')
        problems_completed = models.Completed.objects.filter(
            username=username).order_by('-id')
        problems_pending_review = models.Pending_review.objects.filter(
            username=username).order_by('-id')

    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    dict = []
    print('j', j)
    print('i', i)
    print('suatus', suatus)
    total = 0
    if suatus == '已完成':
        total = problems_completed.count()
        for p in problems_completed[i:j]:
            dict.append({
                'project': p.project,
                'shop_name': p.shop_name,
                'time': p.time,
                'money': p.money,
                'schedule': p.schedule,
                'username': p.username,
                'suatus': '已完成',
                "order_id": p.order_id,
                'url': p.url,
                'submitter': p.submitter,
                'submit_time': p.submit_time,
                'success_time': p.success_time,
                'order_id': p.order_id
            })
    elif suatus == '未完成':
        total = problems_todo.count()
        for p in problems_todo[i:j]:
            dict.append({
                'project': p.project,
                'shop_name': p.shop_name,
                'time': p.time,
                'money': p.money,
                'schedule': p.schedule,
                'username': p.username,
                'suatus': '未完成',
                "order_id": p.order_id
            })
    elif suatus == '待审核':
        total = problems_pending_review.count()
        for p in problems_pending_review[i:j]:
            dict.append({
                'project': p.project,
                'shop_name': p.shop_name,
                'time': p.time,
                'money': p.money,
                'schedule': p.schedule,
                'submitter': p.submitter,
                'username': p.username,
                'submit_time': p.submit_time,
                'suatus': '待审核',
                "order_id": p.order_id
            })
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['total'] = total
    resultdict['state'] = 1
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def select_shop_data(request):
    name = request.GET.get('shop_name')
    page = request.GET.get('currentPage')
    rows = request.GET.get('pagesize')
    problems = models.Dazhongdianping_liren_user_data.objects.filter(
        Q(shop_name__contains=name) | Q(shop_id=name) | Q(shop_start=name)
        | Q(shop_review_count=name)
        | Q(shop_per_capita_consumption=name)
        | Q(shop_region__contains=name)
        | Q(shop_business_district__contains=name)
        | Q(shop_category__contains=name) | Q(shop_address__contains=name))
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    total = problems.count()
    problems = problems[i:j]
    dict = []
    data = {"rows": dict, "total": total}
    for p in problems:
        dic = {}
        dic['shop_id'] = p.shop_id
        dic['shop_name'] = p.shop_name
        dic['shop_start'] = p.shop_start
        dic['shop_review_count'] = p.shop_review_count
        dic['shop_bad_review'] = p.shop_bad_review
        dic['shop_per_capita_consumption'] = p.shop_per_capita_consumption
        dic['shop_region'] = p.shop_region
        dic['shop_effect'] = p.shop_effect
        dic['shop_service'] = p.shop_service
        dic['shop_surroundings'] = p.shop_surroundings
        dic['shop_business_district'] = p.shop_business_district
        dic['shop_category'] = p.shop_category
        dic['shop_address'] = p.shop_address
        dic['shop_telephonenumber'] = p.shop_telephonenumber
        if p.shop_tags != None:
            dic['shop_tags'] = p.shop_tags[0:2]
        else:
            dic['shop_tags'] = p.shop_tags
        dic['shop_kp_name'] = p.shop_kp_name
        dic['shop_kp_position'] = p.shop_kp_position
        dic['shop_kp_wechat_id'] = p.shop_kp_wechat_id
        dic['shop_kp_category'] = p.shop_kp_category
        dic['shop_kp_city'] = p.shop_kp_city
        dic['shop_add_form'] = p.shop_add_form
        dic['shop_edit'] = p.shop_edit
        dict.append(dic)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    resultdict['total'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def table_simple_order_data(request):
    username = request.GET.get('username')
    page = request.GET.get('currentPage')
    rows = request.GET.get('pagesize')
    order = request.GET.get('order_by')
    title = request.GET.get('title')
    month = request.GET.get('month')
    print('title', title)
    print('month', month)
    # 2020-03-31
    if order == 'ascending':
        if title != '':
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title)
                | Q(contract_id__contains=title),
                order_contract_sales=username).order_by('order_start_date')
        elif month != '' and month != None:
            month = datetime.datetime(int(month[0:4]), int(month[5:7]),
                                      int(month[8:10]))
            month = month + datetime.timedelta(days=1)
            problems = models.Order.objects.filter(
                Q(order_date__contains=str(month)[0:7]),
                order_contract_sales=username).order_by('order_start_date')
        elif title != '' and month != None:
            month = datetime.datetime(int(month[0:4]), int(month[5:7]),
                                      int(month[8:10]))
            month = month + datetime.timedelta(days=1)
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title)
                | Q(contract_id__contains=title)
                | Q(order_date__contains=str(month)[0:7]),
                order_contract_sales=username).order_by('order_start_date')
        else:
            problems = models.Order.objects.filter(
                order_contract_sales=username).order_by('order_start_date')
    elif order == 'descending':
        if title != '':
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title)
                | Q(contract_id__contains=title),
                order_contract_sales=username).order_by('-order_start_date')
        elif month != '' and month != None:
            month = datetime.datetime(int(month[0:4]), int(month[5:7]),
                                      int(month[8:10]))
            month = month + datetime.timedelta(days=1)
            problems = models.Order.objects.filter(
                Q(order_date__contains=str(month)[0:7]),
                order_contract_sales=username).order_by('-order_start_date')
        elif title != '' and month != None:
            month = datetime.datetime(int(month[0:4]), int(month[5:7]),
                                      int(month[8:10]))
            month = month + datetime.timedelta(days=1)
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title)
                | Q(contract_id__contains=title)
                | Q(order_date__contains=str(month)[0:7]),
                order_contract_sales=username).order_by('-order_start_date')
        else:
            problems = models.Order.objects.filter(
                order_contract_sales=username).order_by('-order_start_date')
    else:
        if title != '':
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title)
                | Q(contract_id__contains=title),
                order_contract_sales=username).order_by('-id')
        elif month != '' and month != None:
            month = datetime.datetime(int(month[0:4]), int(month[5:7]),
                                      int(month[8:10]))
            month = month + datetime.timedelta(days=1)
            print('进入Month', month)
            problems = models.Order.objects.filter(
                Q(order_date__contains=str(month)[0:7]),
                order_contract_sales=username).order_by('-id')
        elif title != '' and month != None:
            month = datetime.datetime(int(month[0:4]), int(month[5:7]),
                                      int(month[8:10]))
            month = month + datetime.timedelta(days=1)
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title)
                | Q(contract_id__contains=title)
                | Q(order_date__contains=str(month)[0:7])).order_by('-id')
        else:
            problems = models.Order.objects.filter(
                order_contract_sales=username).order_by('-id')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    total = problems.count()
    problems = problems[i:j]
    dict = []
    data = {"rows": dict, "total": total}
    today = str(datetime.datetime.today())[0:10]
    for u in problems:
        # 截止的日期
        strftime = datetime.datetime.strptime(u.order_end_date, "%Y-%m-%d")
        # 今天的日期
        strftime2 = datetime.datetime.strptime(today, "%Y-%m-%d")
        # 判断是否超时
        if (strftime > strftime2) == False:
            models.Order.objects.filter(contract_id=u.contract_id).update(tags='断约')

            models.Dazhongdianping_liren_all_data.objects.filter(shop_city=u.city, shop_name=u.sign_contract_shop,
                                                                 shop_id=u.shop_id).update(shop_tags='断约')
    for p in problems:
        dic = {}
        dic['contract_id'] = p.contract_id
        dic['order_date'] = p.order_date[0:10]
        dic['order_start_date'] = p.order_start_date[0:10]
        dic['sign_contract_shop'] = p.sign_contract_shop
        dic['customer_source'] = p.customer_source
        dic['contract_status'] = p.contract_status
        dic['contracted_projects'] = p.contracted_projects
        dic['shop_industry'] = p.shop_industry
        dic['shop_kp_name'] = p.shop_kp_name
        dic['shop_telephonenumber'] = p.shop_telephonenumber
        dic['order_numbers'] = p.order_numbers
        dic['shop_cooperation_duration'] = p.shop_cooperation_duration
        dic['order_end_date'] = p.order_end_date
        dic['order_amount'] = p.order_amount
        dic['cost_fees'] = p.cost_fees
        dic['city'] = p.city
        dic['payment_method'] = p.payment_method
        dic['order_contract_sales'] = p.order_contract_sales
        dic['shop_remark'] = p.shop_remark
        dic['shop_id'] = p.shop_id
        dic['order_form'] = eval(p.order_form)
        # 今天的日期
        d1 = datetime.datetime(int(str(today)[0:4]), int(str(today)[5:7]),
                               int(str(today)[8:10]))
        # 截止的日期
        d2 = datetime.datetime(int(p.order_end_date[0:4]),
                               int(p.order_end_date[5:7]),
                               int(p.order_end_date[8:10]))
        # 判断到期时间
        if '-' in str((d2 - d1).days):
            dic['remaining_number_of_days'] = ('已过期' + str(
                (d2 - d1).days) + '天')
            dic['zhuangtai'] = '已到期'
        else:
            dic['remaining_number_of_days'] = ('剩余' + str(
                (d2 - d1).days) + '天')
            dic['zhuangtai'] = '剩余'
        dic['tags'] = p.tags
        dict.append(dic)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    resultdict['total'] = total
    resultdict['data'] = dict
    # print(resultdict)
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def delete_order(request):
    '''
    删除订单
    '''
    order_id = request.GET.get('order_id')
    shop_id = request.GET.get('shop_id')
    # 更改商户为断约状态
    models.Dazhongdianping_liren_all_data.objects.filter(
        shop_id=shop_id).update(shop_tags="断约")
    # 订单以及任务删除
    order = models.Order.objects.filter(contract_id=order_id).delete()
    todo = models.To_do.objects.filter(order_id=order_id).delete()
    completed = models.Completed.objects.filter(order_id=order_id).delete()
    pending_review = models.Pending_review.objects.filter(
        order_id=order_id).delete()
    if str(todo) == '<QuerySet []>' and str(
            completed) == '<QuerySet []>' and str(
        pending_review) == '<QuerySet []>':
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 12
        return JsonResponse(resultdict, safe=False)
    else:
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)


@csrf_exempt
def create_table(request):
    shop_id = request.GET.get('shop_id')
    shop_name = request.GET.get('shop_name')
    shop_start = request.GET.get('shop_start')
    shop_review_count = request.GET.get('shop_review_count')
    shop_per_capita_consumption = request.GET.get(
        'shop_per_capita_consumption')
    shop_effect = request.GET.get('shop_effect')
    shop_service = request.GET.get('shop_service')
    shop_surroundings = request.GET.get('shop_surroundings')
    shop_address = request.GET.get('shop_address')
    shop_telephonenumber = request.GET.get('shop_telephonenumber')
    shop_business_district = request.GET.get('shop_business_district')
    shop_category = request.GET.get('shop_category')
    shop_city = request.GET.get('shop_city')
    shop_region = request.GET.get('shop_region')
    b = models.Dazhongdianping_liren_all_data.objects.filter(
        shop_id=shop_id).count()
    c = models.Dazhongdianping_liren_user_data.objects.filter(
        shop_id=shop_id).count()
    if b != 0:
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 2
        return JsonResponse(resultdict, safe=False)
    if c != 0:
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 3
        return JsonResponse(resultdict, safe=False)
    if b == 0 and c == 0:
        models.Dazhongdianping_liren_all_data.objects.create(
            shop_id=shop_id,
            shop_name=shop_name,
            shop_start=shop_start,
            shop_review_count=shop_review_count,
            shop_per_capita_consumption=shop_per_capita_consumption,
            shop_effect=shop_effect,
            shop_service=shop_service,
            shop_surroundings=shop_surroundings,
            shop_address=shop_address,
            shop_telephonenumber=shop_telephonenumber,
            shop_business_district=shop_business_district,
            shop_category=shop_category,
            shop_city=shop_city,
            shop_region=shop_region)
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)


@csrf_exempt
def table_simple_order_data_all(request):
    username = request.GET.get('username')
    page = request.GET.get('currentPage')
    rows = request.GET.get('pagesize')
    order = request.GET.get('order_by')
    title = request.GET.get('title')
    month = request.GET.get('month')
    print(month)
    if str(month) == 'None' or str(month) == None:
        month == ''
    if order == 'ascending':
        if title != '' and username == '' and month == '':
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title) |
                Q(contract_id__contains=title)).order_by('order_start_date')
        elif title != '' and month != '' and username == '':
            month = datetime.datetime(
                int(month[0:4]), int(month[5:7]), int(month[8:10]))

            month = month + datetime.timedelta(days=1)
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title) |
                Q(contract_id__contains=title),
                order_date__contains=str(month)[0:7]).order_by('order_start_date')
        elif title != '' and month != '' and username != '':
            month = datetime.datetime(int(month[0:4]), int(month[5:7]),
                                      int(month[8:10]))
            month = month + datetime.timedelta(days=1)
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title) |
                Q(contract_id__contains=title),
                order_date__contains=str(month)[0:7], order_contract_sales__contains=username).order_by(
                'order_start_date')
        elif title == '' and username != '' and month == '':
            problems = models.Order.objects.filter(
                order_contract_sales__contains=username).order_by('order_start_date')
        elif title == '' and username != '' and month != '':
            month = datetime.datetime(int(month[0:4]), int(month[5:7]),
                                      int(month[8:10]))
            month = month + datetime.timedelta(days=1)
            problems = models.Order.objects.filter(
                order_contract_sales__contains=username,
                order_date__contains=str(month)[0:7]).order_by('order_start_date')
        elif title != '' and username != '' and month == '':
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title) | Q(
                    contract_id__contains=title),
                order_contract_sales__contains=username).order_by('order_start_date')
        elif title == '' and username == '' and month != '':
            try:
                month = datetime.datetime(int(month[0:4]), int(month[5:7]),
                                          int(month[8:10]))
                month = month + datetime.timedelta(days=1)
                problems = models.Order.objects.filter(order_date__contains=str(month)[0:7]).order_by(
                    'order_start_date')
            except:
                problems = models.Order.ojects.all().order_by('order_start_date')
        else:
            problems = models.Order.objects.all().order_by('order_start_date')
    elif order == 'descending':
        if title != '' and username == '' and month == '':
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title) |
                Q(contract_id__contains=title)).order_by('-order_start_date')
        elif title != '' and month != '' and username == '':
            month = datetime.datetime(
                int(month[0:4]), int(month[5:7]), int(month[8:10]))
            month = month + datetime.timedelta(days=1)
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title) |
                Q(contract_id__contains=title),
                order_date__contains=str(month)[0:7]).order_by('-order_start_date')
        elif title != '' and month != '' and username != '':
            month = datetime.datetime(int(month[0:4]), int(month[5:7]),
                                      int(month[8:10]))
            month = month + datetime.timedelta(days=1)
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title) |
                Q(contract_id__contains=title),
                order_date__contains=str(month)[0:7], order_contract_sales__contains=username).order_by(
                '-order_start_date')
        elif title == '' and username != '' and month == '':
            problems = models.Order.objects.filter(
                order_contract_sales__contains=username).order_by('-order_start_date')
        elif title == '' and username != '' and month != '':
            month = datetime.datetime(int(month[0:4]), int(month[5:7]),
                                      int(month[8:10]))
            month = month + datetime.timedelta(days=1)
            problems = models.Order.objects.filter(
                order_contract_sales__contains=username,
                order_date__contains=str(month)[0:7]).order_by('-order_start_date')
        elif title != '' and username != '' and month == '':
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title) | Q(
                    contract_id__contains=title),
                order_contract_sales__contains=username).order_by('-order_start_date')
        elif title == '' and username == '' and month != '':
            month = datetime.datetime(int(month[0:4]), int(month[5:7]),
                                      int(month[8:10]))
            month = month + datetime.timedelta(days=1)
            problems = models.Order.objects.filter(order_date__contains=str(month)[0:7]).order_by('-order_start_date')
        else:
            problems = models.Order.objects.all().order_by('-order_start_date')
    else:
        if title != '' and username == '' and month == '':
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title) |
                Q(contract_id__contains=title)).order_by('-id')
        elif title != '' and month != '' and username == '':
            month = datetime.datetime(
                int(month[0:4]), int(month[5:7]), int(month[8:10]))
            print('month', month)
            month = month + datetime.timedelta(days=1)
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title) |
                Q(contract_id__contains=title),
                order_date__contains=str(month)[0:7]).order_by('-id')
        elif title != '' and month != '' and username != '':
            month = datetime.datetime(int(month[0:4]), int(month[5:7]),
                                      int(month[8:10]))
            month = month + datetime.timedelta(days=1)
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title) |
                Q(contract_id__contains=title),
                order_date__contains=str(month)[0:7], order_contract_sales__contains=username).order_by('-id')
        elif title == '' and username != '' and month == '':
            problems = models.Order.objects.filter(
                order_contract_sales__contains=username).order_by('-id')
        elif title == '' and username != '' and month != '':
            try:
                month = datetime.datetime(int(month[0:4]), int(month[5:7]),
                                          int(month[8:10]))
                month = month + datetime.timedelta(days=1)
                problems = models.Order.objects.filter(
                    order_contract_sales__contains=username,
                    order_date__contains=str(month)[0:7]).order_by('-id')
            except:
                problems = models.Order.objects.filter(
                    order_contract_sales__contains=username).order_by('-id')
        elif title != '' and username != '' and month == '':
            problems = models.Order.objects.filter(
                Q(sign_contract_shop__contains=title) | Q(
                    contract_id__contains=title),
                order_contract_sales__contains=username).order_by('-id')
        elif title == '' and username == '' and month != '':
            try:
                month = datetime.datetime(int(month[0:4]), int(month[5:7]),
                                          int(month[8:10]))
                month = month + datetime.timedelta(days=1)
                problems = models.Order.objects.filter(order_date__contains=str(month)[0:7]).order_by('-id')
            except:
                problems = models.Order.objects.all().order_by('-id')
        else:
            problems = models.Order.objects.all().order_by('-id')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    total = problems.count()
    problems = problems[i:j]
    tags_xuyue = ''
    today = str(datetime.datetime.today())[0:10]
    for u in problems:
        # 截止的日期
        strftime = datetime.datetime.strptime(u.order_end_date, "%Y-%m-%d")
        # 今天的日期
        strftime2 = datetime.datetime.strptime(today, "%Y-%m-%d")
        # 判断是否超时
        if (strftime > strftime2) == False:
            models.Order.objects.filter(contract_id=u.contract_id).update(tags='断约')

            models.Dazhongdianping_liren_all_data.objects.filter(shop_city=u.city, shop_name=u.sign_contract_shop,
                                                                 shop_id=u.shop_id).update(shop_tags='断约')
    dict = []
    data = {"rows": dict, "total": total}
    print('page', page)
    print('rows', rows)
    today = datetime.date.today()
    for p in problems:
        dic = {}
        dic['id'] = p.id
        dic['contract_id'] = p.contract_id
        dic['order_date'] = p.order_date[0:10]
        dic['order_start_date'] = p.order_start_date[0:10]
        dic['sign_contract_shop'] = p.sign_contract_shop
        dic['customer_source'] = p.customer_source
        dic['contract_status'] = p.contract_status
        dic['contracted_projects'] = p.contracted_projects
        dic['shop_industry'] = p.shop_industry
        dic['shop_kp_name'] = p.shop_kp_name
        dic['shop_telephonenumber'] = p.shop_telephonenumber
        dic['order_numbers'] = p.order_numbers
        dic['shop_cooperation_duration'] = p.shop_cooperation_duration
        dic['order_end_date'] = p.order_end_date
        dic['order_amount'] = p.order_amount
        dic['cost_fees'] = p.cost_fees
        dic['city'] = p.city
        dic['payment_method'] = p.payment_method
        dic['order_contract_sales'] = p.order_contract_sales
        dic['shop_remark'] = p.shop_remark
        dic['shop_id'] = p.shop_id
        dic['order_form'] = eval(p.order_form)
        # 今天的日期
        d1 = datetime.datetime(int(str(today)[0:4]), int(str(today)[5:7]),
                               int(str(today)[8:10]))
        # 截止的日期
        d2 = datetime.datetime(int(p.order_end_date[0:4]),
                               int(p.order_end_date[5:7]),
                               int(p.order_end_date[8:10]))
        # 判断到期时间
        if '-' in str((d2 - d1).days):
            dic['remaining_number_of_days'] = ('已过期' + str(
                (d2 - d1).days) + '天')
            dic['zhuangtai'] = '已到期'
        else:
            dic['remaining_number_of_days'] = ('剩余' + str(
                (d2 - d1).days) + '天')
            dic['zhuangtai'] = '剩余'
        dic['tags'] = p.tags
        dict.append(dic)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    resultdict['total'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def order_select(request):
    contract_id = request.GET.get('contract_id')
    order_numbers = request.GET.get('order_numbers')  # 门店数
    payment_method = request.GET.get('payment_method')  # 支付方
    contract_status = request.GET.get('contract_status')  # 签约状态
    contracted_projects = request.GET.get('contracted_projects')  # 签约项目
    customer_source = request.GET.get('customer_source')
    shop_industry = request.GET.get('shop_industry')
    shop_kp_name = request.GET.get('shop_kp_name')
    shop_telephonenumber = request.GET.get('shop_telephonenumber')
    shop_remark = request.GET.get('shop_remark')
    shop_id = request.GET.get('shop_id')
    user_name = request.GET.get('user_name')
    edit_data = models.Dazhongdianping_liren_all_data.objects.filter(
        shop_id=shop_id)
    data = datetime.date.today()
    form_data = ''
    for i in edit_data:
        form_data = i.shop_edit
    print(data)
    print(user_name)
    print(shop_remark)
    print(shop_id)
    if form_data == '':
        print('进入')
        if shop_remark != '':
            edit_data = models.Dazhongdianping_liren_all_data.objects.filter(
                shop_id=shop_id).update(shop_edit='修改人:' + user_name + '，时间:' +
                                                  str(data) + '，内容:' + shop_remark + '￥')
    else:
        print('进入', type(shop_remark))
        if shop_remark != '':
            edit_data = models.Dazhongdianping_liren_all_data.objects.filter(
                shop_id=shop_id).update(shop_edit=form_data + '修改人:' +
                                                  user_name + '，时间:' + str(data) +
                                                  '，内容:' + shop_remark + '￥')
    if str(edit_data) != '<QuerySet []>':
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)


pull_edit = ''


# 全部商户数据显示

@csrf_exempt
# @required_login
def table_simple_user_data(request):
    page = request.GET.get('currentPage')
    rows = request.GET.get('pagesize')
    name = request.GET.get("search")
    username = request.GET.get("username")
    shop_business_district = request.GET.get('shop_business_district')  # 区域
    shop_category = request.GET.get('shop_category')  # 商圈
    shop_region = request.GET.get('shop_region')  # 品类
    shop_type = request.GET.get('shop_type')  # 类型
    order = request.GET.get('order')
    city = request.GET.get('city')
    city = eval(city)
    print(page)
    print(rows)
    print(name)
    print(username)
    print(shop_business_district)
    print(shop_category)
    print(shop_region)
    print(shop_type)
    if '[' in str(shop_region) or '[' in str(shop_category) or '[' in str(
            shop_business_district) or len(city) != 0:
        if order == 'descending':
            if name != '' and name != None:
                problems = models.Dazhongdianping_liren_user_data.objects.filter(
                    Q(shop_name__contains=name) | Q(shop_id=name)
                    | Q(shop_start=name)
                    | Q(shop_review_count=name)
                    | Q(shop_per_capita_consumption=name)
                    | Q(shop_region__contains=name)
                    | Q(shop_business_district__contains=name)
                    | Q(shop_category__contains=name)
                    | Q(shop_address__contains=name),
                    username=username)
            else:
                # 搜索逻辑
                # 区域和商圈等于空
                if shop_business_district == '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region__in=eval(shop_region),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 商圈和品类等于空
                elif shop_business_district != '区域' and shop_category == '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    print('进来了')
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 区域和品类等于空
                elif shop_category != '商圈' and shop_region != '行业' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 区域和商圈不等于空
                elif shop_business_district != '区域' and shop_category != '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district__in=eval(
                            shop_business_district),
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 商圈和品类不等于空
                elif shop_region != '行业' and shop_category != '商圈' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region__in=eval(shop_region),
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 区域和品类不等于空
                elif shop_business_district != '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district__in=eval(
                            shop_business_district),
                        shop_region__in=eval(shop_region),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                elif shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region__in=eval(shop_region),
                        shop_business_district__in=eval(
                            shop_business_district),
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                elif shop_category != '商圈' and shop_business_district == '区域' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 类型不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 类型和品类不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=eval(shop_region),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 类型和城区不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 类型和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 类型和品类和城区不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=eval(shop_region),
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 类型和城区和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=eval(shop_category),
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 类型和商圈和品类
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=eval(shop_region),
                        shop_category__in=eval(shop_category),
                        username=username).order_by('id').order_by(
                        '-shop_telephonenumber')
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        shop_category=shop_category,
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type == '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city, username=username).order_by(
                        '-id').order_by('-shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        shop_region__in=eval(shop_region),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        shop_region__in=eval(shop_region),
                        username=username,
                        shop_business_district__in=eval(shop_business_district)
                    ).order_by('-id').order_by('-shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_tags__contains=shop_type,
                        shop_region=shop_region,
                        shop_city__=city,
                        shop_category=shop_category,
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                elif len(
                        city
                ) == 0 and shop_type != 'None' and shop_region != 'None' and shop_business_district != 'None' and shop_category != 'None':
                    problems = models.Dazhongdianping_liren_user_data.objects.all(
                    ).order_by('-id').order_by('-shop_telephonenumber')
                elif len(
                        city
                ) == 0 and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.all(
                    ).order_by('-id').order_by('-shop_telephonenumber')
        elif order == 'ascending':
            if name != '' and name != None:
                problems = models.Dazhongdianping_liren_user_data.objects.filter(
                    Q(shop_name__contains=name) | Q(shop_id=name)
                    | Q(shop_start=name)
                    | Q(shop_review_count=name)
                    | Q(shop_per_capita_consumption=name)
                    | Q(shop_region__contains=name)
                    | Q(shop_business_district__contains=name)
                    | Q(shop_category__contains=name)
                    | Q(shop_address__contains=name),
                    username=username)
            else:
                # 搜索逻辑
                # 区域和商圈等于空
                if shop_business_district == '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region__in=eval(shop_region),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 商圈和品类等于空
                elif shop_business_district != '区域' and shop_category == '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 区域和品类等于空
                elif shop_category != '商圈' and shop_region != '行业' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 区域和商圈不等于空
                elif shop_business_district != '区域' and shop_category != '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district__in=eval(
                            shop_business_district),
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 商圈和品类不等于空
                elif shop_region != '行业' and shop_category != '商圈' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region__in=eval(shop_region),
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 区域和品类不等于空
                elif shop_business_district != '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district__in=eval(
                            shop_business_district),
                        shop_region__in=eval(shop_region),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region__in=eval(shop_region),
                        shop_business_district__in=eval(
                            shop_business_district),
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif shop_category != '商圈' and shop_business_district == '区域' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和品类不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=eval(shop_region),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和城区不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和品类和城区不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=eval(shop_region),
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和城区和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=eval(shop_category),
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和商圈和品类
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=eval(shop_region),
                        shop_category__in=eval(shop_category),
                        username=username).order_by('id').order_by(
                        'shop_telephonenumber')
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        shop_category=shop_category,
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type == '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city, username=username).order_by(
                        '-id').order_by('shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        shop_region__in=eval(shop_region),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        shop_region__in=eval(shop_region),
                        username=username,
                        shop_business_district__in=eval(shop_business_district)
                    ).order_by('-id').order_by('shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_tags__contains=shop_type,
                        shop_city__=city,
                        shop_region=shop_region,
                        shop_category=shop_category,
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif len(
                        city
                ) == 0 and shop_type != 'None' and shop_region != 'None' and shop_business_district != 'None' and shop_category != 'None':
                    problems = models.Dazhongdianping_liren_user_data.objects.all(
                    ).order_by('-id').order_by('shop_telephonenumber')
                elif len(
                        city
                ) == 0 and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.all(
                    ).order_by('-id').order_by('shop_telephonenumber')
        else:
            if name != '' and name != None:
                problems = models.Dazhongdianping_liren_user_data.objects.filter(
                    Q(shop_name__contains=name) | Q(shop_id=name)
                    | Q(shop_start=name)
                    | Q(shop_review_count=name)
                    | Q(shop_per_capita_consumption=name)
                    | Q(shop_region__contains=name)
                    | Q(shop_business_district__contains=name)
                    | Q(shop_category__contains=name)
                    | Q(shop_address__contains=name),
                    username=username)
            else:
                # 搜索逻辑
                # 区域和商圈等于空
                if shop_business_district == '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region__in=eval(shop_region),
                        username=username).order_by('-id')
                # 商圈和品类等于空
                elif shop_business_district != '区域' and shop_category == '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id')
                # 区域和品类等于空
                elif shop_category != '商圈' and shop_region != '行业' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_category__id=eval(shop_category),
                        username=username).order_by('-id')
                # 区域和商圈不等于空
                elif shop_business_district != '区域' and shop_category != '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district__in=eval(
                            shop_business_district),
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id')
                # 商圈和品类不等于空
                elif shop_region != '行业' and shop_category != '商圈' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region__in=eval(shop_region),
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id')
                # 区域和品类不等于空
                elif shop_business_district != '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district__in=eval(
                            shop_business_district),
                        shop_region__in=eval(shop_region),
                        username=username).order_by('-id')
                elif shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region__in=eval(shop_region),
                        shop_business_district__in=eval(
                            shop_business_district),
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id')
                elif shop_category != '商圈' and shop_business_district == '区域' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id')
                # 类型不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        username=username).order_by('-id')
                # 类型和品类不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=eval(shop_region),
                        username=username).order_by('-id')
                # 类型和城区不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id')
                # 类型和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=eval(shop_category),
                        username=username).order_by('-id')
                # 类型和品类和城区不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=eval(shop_region),
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id')
                # 类型和城区和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category__in=eval(shop_category),
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id')
                # 类型和商圈和品类
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=eval(shop_region),
                        shop_category__contains__in=eval(shop_category),
                        username=username).order_by('id')
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region__in=eval(shop_region),
                        shop_category__in=eval(shop_category),
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id')
                elif len(
                        city
                ) != 0 and shop_type == '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city, username=username).order_by('-id')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        username=username).order_by('-id')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        shop_region__in=eval(shop_region),
                        username=username).order_by('-id')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        shop_region__in=eval(shop_region),
                        username=username,
                        shop_business_district__in=eval(
                            shop_business_district)).order_by('-id')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_tags__contains=shop_type,
                        shop_region=shop_region,
                        shop_city__=city,
                        shop_category=shop_category,
                        shop_business_district__in=eval(
                            shop_business_district),
                        username=username).order_by('-id')
                elif len(
                        city
                ) == 0 and shop_type != 'None' and shop_region != 'None' and shop_business_district != 'None' and shop_category != 'None':
                    problems = models.Dazhongdianping_liren_user_data.objects.all(
                    ).order_by('-id')
                elif len(
                        city
                ) == 0 and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.all(
                    ).order_by('-id')
    else:
        shop_region = shop_region
        if order == 'descending':
            if name != '' and name != None:
                problems = models.Dazhongdianping_liren_user_data.objects.filter(
                    Q(shop_name__contains=name) | Q(shop_id=name)
                    | Q(shop_start=name)
                    | Q(shop_review_count=name)
                    | Q(shop_per_capita_consumption=name)
                    | Q(shop_region__contains=name)
                    | Q(shop_business_district__contains=name)
                    | Q(shop_category__contains=name)
                    | Q(shop_address__contains=name),
                    username=username)
            else:
                # 搜索逻辑
                # 区域和商圈等于空
                if shop_business_district == '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region=shop_region, username=username).order_by(
                        '-id').order_by('-shop_telephonenumber')
                # 商圈和品类等于空
                elif shop_business_district != '区域' and shop_category == '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district=shop_business_district,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 区域和品类等于空
                elif shop_category != '商圈' and shop_region != '行业' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_category=shop_category,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 区域和商圈不等于空
                elif shop_business_district != '区域' and shop_category != '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district=shop_business_district,
                        shop_category=shop_category,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 商圈和品类不等于空
                elif shop_region != '行业' and shop_category != '商圈' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region=shop_region,
                        shop_category=shop_category,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 区域和品类不等于空
                elif shop_business_district != '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district=shop_business_district,
                        shop_region=shop_region,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                elif shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region=shop_region,
                        shop_business_district=shop_business_district,
                        shop_category=shop_category,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                elif shop_category != '商圈' and shop_business_district == '区域' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_category=shop_category,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 类型不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 类型和品类不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 类型和城区不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_business_district=shop_business_district,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 类型和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category=shop_category,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 类型和品类和城区不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        shop_business_district=shop_business_district,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 类型和城区和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category=shop_category,
                        shop_business_district=shop_business_district,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 类型和商圈和品类
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        shop_category__contains=shop_category,
                        username=username).order_by('id').order_by(
                        '-shop_telephonenumber')
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        shop_category=shop_category,
                        shop_business_district=shop_business_district,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type == '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city, username=username).order_by(
                        '-id').order_by('-shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        shop_region__in=shop_region,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        shop_region__in=shop_region,
                        username=username,
                        shop_business_district__in=shop_business_district
                    ).order_by('-id').order_by('-shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_tags__contains=shop_type,
                        shop_region=shop_region,
                        shop_city__=city,
                        shop_category=shop_category,
                        shop_business_district__in=shop_business_district,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                elif len(
                        city
                ) == 0 and shop_type != 'None' and shop_region != 'None' and shop_business_district != 'None' and shop_category != 'None':
                    problems = models.Dazhongdianping_liren_user_data.objects.all(
                    ).order_by('-id').order_by('-shop_telephonenumber')
                elif len(
                        city
                ) == 0 and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.all(
                    ).order_by('-id').order_by('-shop_telephonenumber')
        elif order == 'ascending':
            if name != '' and name != None:
                problems = models.Dazhongdianping_liren_user_data.objects.filter(
                    Q(shop_name__contains=name) | Q(shop_id=name)
                    | Q(shop_start=name)
                    | Q(shop_review_count=name)
                    | Q(shop_per_capita_consumption=name)
                    | Q(shop_region__contains=name)
                    | Q(shop_business_district__contains=name)
                    | Q(shop_category__contains=name)
                    | Q(shop_address__contains=name))
            else:
                # 搜索逻辑
                # 区域和商圈等于空
                if shop_business_district == '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region=shop_region, username=username).order_by(
                        '-id').order_by('shop_telephonenumber')
                # 商圈和品类等于空
                elif shop_business_district != '区域' and shop_category == '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district=shop_business_district,
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 区域和品类等于空
                elif shop_category != '商圈' and shop_region != '行业' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_category=shop_category,
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 区域和商圈不等于空
                elif shop_business_district != '区域' and shop_category != '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district=shop_business_district,
                        shop_category=shop_category,
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 商圈和品类不等于空
                elif shop_region != '行业' and shop_category != '商圈' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region=shop_region,
                        shop_category=shop_category,
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 区域和品类不等于空
                elif shop_business_district != '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district=shop_business_district,
                        shop_region=shop_region,
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region=shop_region,
                        shop_business_district=shop_business_district,
                        shop_category=shop_category,
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif shop_category != '商圈' and shop_business_district == '区域' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_category=shop_category,
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type,
                          username=username)).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和品类不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和城区不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_business_district=shop_business_district,
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category=shop_category,
                        username=username).order_by('-id').order_by(
                        '-shop_telephonenumber')
                # 类型和品类和城区不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        shop_business_district=shop_business_district,
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和城区和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category=shop_category,
                        shop_business_district=shop_business_district,
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                # 类型和商圈和品类
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        shop_category__contains=shop_category,
                        username=username).order_by('id').order_by(
                        'shop_telephonenumber')
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        shop_category=shop_category,
                        shop_business_district=shop_business_district,
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type == '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city, username=username).order_by(
                        '-id').order_by('shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        username=username).order_by(
                        'shop_telephonenumber').order_by(
                        'shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        shop_region__in=shop_region,
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        shop_region__in=shop_region,
                        username=username,
                        shop_business_district__in=shop_business_district
                    ).order_by('-id').order_by('shop_telephonenumber')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_tags__contains=shop_type,
                        shop_region=shop_region,
                        shop_city__=city,
                        shop_category=shop_category,
                        shop_business_district__in=shop_business_district,
                        username=username).order_by('-id').order_by(
                        'shop_telephonenumber')
                elif len(
                        city
                ) == 0 and shop_type != 'None' and shop_region != 'None' and shop_business_district != 'None' and shop_category != 'None':
                    problems = models.Dazhongdianping_liren_user_data.objects.all(
                    ).order_by('-id').order_by('shop_telephonenumber')
                elif len(
                        city
                ) == 0 and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.all(
                    ).order_by('-id').order_by('shop_telephonenumber')
        else:
            if name != '' and name != None:
                problems = models.Dazhongdianping_liren_user_data.objects.filter(
                    Q(shop_name__contains=name) | Q(shop_id=name)
                    | Q(shop_start=name)
                    | Q(shop_review_count=name)
                    | Q(shop_per_capita_consumption=name)
                    | Q(shop_region__contains=name)
                    | Q(shop_business_district__contains=name)
                    | Q(shop_category__contains=name)
                    | Q(shop_address__contains=name),
                    username=username)
            else:
                # 搜索逻辑
                # 区域和商圈等于空
                if shop_business_district == '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region=shop_region,
                        username=username).order_by('-id')
                # 商圈和品类等于空
                elif shop_business_district != '区域' and shop_category == '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district=shop_business_district,
                        username=username).order_by('-id')
                # 区域和品类等于空
                elif shop_category != '商圈' and shop_region != '行业' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_category=shop_category,
                        username=username).order_by('-id')
                # 区域和商圈不等于空
                elif shop_business_district != '区域' and shop_category != '商圈' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district=shop_business_district,
                        shop_category=shop_category,
                        username=username).order_by('-id')
                # 商圈和品类不等于空
                elif shop_region != '行业' and shop_category != '商圈' and shop_business_district == '区域' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region=shop_region,
                        shop_category=shop_category,
                        username=username).order_by('-id')
                # 区域和品类不等于空
                elif shop_business_district != '区域' and shop_region != '行业' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_business_district=shop_business_district,
                        shop_region=shop_region,
                        username=username).order_by('-id')
                elif shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_region=shop_region,
                        shop_business_district=shop_business_district,
                        shop_category=shop_category,
                        username=username).order_by('-id')
                elif shop_category != '商圈' and shop_business_district == '区域' and shop_region == '行业' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_category=shop_category,
                        username=username).order_by('-id')
                # 类型不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        username=username).order_by('-id')
                # 类型和品类不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        username=username).order_by('-id')
                # 类型和城区不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_business_district=shop_business_district,
                        username=username).order_by('-id')
                # 类型和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category=shop_category,
                        username=username).order_by('-id')
                # 类型和品类和城区不等于空
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        shop_business_district=shop_business_district,
                        username=username).order_by('-id')
                # 类型和城区和商圈不等于空
                elif shop_type != '合作状态' and shop_region == '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_category=shop_category,
                        shop_business_district=shop_business_district,
                        username=username).order_by('-id')
                # 类型和商圈和品类
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        shop_category__contains=shop_category,
                        username=username).order_by('id')
                elif shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        Q(shop_tags__contains=shop_type),
                        shop_region=shop_region,
                        shop_category=shop_category,
                        shop_business_district=shop_business_district,
                        username=username).order_by('-id')
                elif len(
                        city
                ) != 0 and shop_type == '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city, username=username).order_by('-id')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        username=username).order_by('-id')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district == '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        shop_region__in=shop_region,
                        username=username).order_by('-id')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category == '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_city__in=city,
                        shop_tags__contains=shop_type,
                        shop_region__in=shop_region,
                        username=username,
                        shop_business_district__in=shop_business_district).order_by('-id')
                elif len(
                        city
                ) != 0 and shop_type != '合作状态' and shop_region != '行业' and shop_business_district != '区域' and shop_category != '商圈':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        shop_tags__contains=shop_type,
                        shop_region=shop_region,
                        shop_city__=city,
                        shop_category=shop_category,
                        shop_business_district__in=shop_business_district,
                        username=username).order_by('-id')
                elif len(
                        city
                ) == 0 and shop_type != 'None' and shop_region != 'None' and shop_business_district != 'None' and shop_category != 'None':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        username=username).order_by('-id')
                elif len(
                        city
                ) == 0 and shop_region == '行业' and shop_business_district == '区域' and shop_category == '商圈' and shop_type == '合作状态':
                    problems = models.Dazhongdianping_liren_user_data.objects.filter(
                        username=username).order_by('-id')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    total = problems.count()
    problems = problems[i:j]
    dict = []
    data = {"rows": dict, "total": total}
    private_sea_time = ''
    setting = models.Setting_storage.objects.all()
    for i in setting:
        private_sea_time = i.private_sea_time
    year = str(datetime.date.today())[0:4]
    month = str(datetime.date.today())[5:7]
    day = str(datetime.date.today())[8:10]
    now_time = datetime.datetime(int(year), int(month), int(day))
    for p in problems:
        dic = {}
        dic['shop_id'] = p.shop_id
        dic['shop_name'] = p.shop_name
        dic['shop_start'] = p.shop_start
        dic['shop_review_count'] = p.shop_review_count
        dic['shop_per_capita_consumption'] = p.shop_per_capita_consumption
        dic['shop_region'] = p.shop_region
        dic['shop_effect'] = p.shop_effect
        dic['shop_service'] = p.shop_service
        dic['shop_surroundings'] = p.shop_surroundings
        dic['shop_business_district'] = p.shop_business_district
        dic['shop_category'] = p.shop_category
        dic['shop_address'] = p.shop_address
        dic['shop_telephonenumber'] = p.shop_telephonenumber
        if p.shop_tags != None:
            dic['shop_tags'] = p.shop_tags[0:2]
        else:
            dic['shop_tags'] = p.shop_tags
        dic['shop_kp_name'] = p.shop_kp_name
        dic['shop_kp_position'] = p.shop_kp_position
        dic['shop_kp_wechat_id'] = p.shop_kp_wechat_id
        dic['shop_kp_category'] = p.shop_kp_category
        dic['shop_kp_city'] = p.shop_kp_city
        dic['shop_add_form'] = p.shop_add_form
        dic['shop_city'] = p.shop_city
        dic['shop_edit'] = p.shop_edit
        # 超时回退思路 ,取出存入时间的数据,对比今天数字
        pull_year = str(p.pull_date)[0:4]
        pull_month = str(p.pull_date)[5:7]
        pull_day = str(p.pull_date)[8:10]
        private_sea_data = models.Setting_storage.objects.all()
        dict_today = []
        for a in private_sea_data:
            dict_today.append(a.private_sea_time)
        difference_time = dict_today[0]
        pull_time = datetime.datetime(int(pull_year), int(pull_month),
                                      int(pull_day))
        pull_time = pull_time + datetime.timedelta(days=int(difference_time))
        if '-' in str(pull_time - now_time):
            shop_add = models.Dazhongdianping_liren_all_data.objects.create(
                shop_id=p.shop_id,
                shop_name=p.shop_name,
                shop_start=p.shop_start,
                shop_review_count=p.shop_review_count,
                shop_per_capita_consumption=p.shop_per_capita_consumption,
                shop_effect=p.shop_effect,
                shop_surroundings=p.shop_surroundings,
                shop_service=p.shop_service,
                shop_region=p.shop_region,
                shop_business_district=p.shop_business_district,
                shop_category=p.shop_category,
                shop_address=p.shop_address,
                shop_telephonenumber=p.shop_telephonenumber,
                shop_edit=p.shop_edit,
                shop_tags=p.shop_tags,
                shop_kp_name=p.shop_kp_name,
                shop_kp_wechat_id=p.shop_kp_wechat_id,
                shop_kp_city=p.shop_kp_city,
                shop_kp_category=p.shop_kp_category,
                shop_add_form=p.shop_add_form,
                shop_kp_position=p.shop_kp_position)
            if shop_add != None:
                models.Dazhongdianping_liren_user_data.objects.filter(
                    shop_id=p.shop_id).delete()
        else:
            dict.append(dic)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    resultdict['total'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


# 显示编辑信息

@csrf_exempt
def get_private_sea(request):
    data = models.Setting_storage.objects.all()
    private_sea_time = 0
    private_sea_length = 0
    for i in data:
        private_sea_time = i.private_sea_time
        private_sea_length = i.private_sea_length
    resultdict = {}
    resultdict['private_sea_time'] = private_sea_time
    resultdict['private_sea_length'] = private_sea_length
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def private_sea_edit(request):
    private_sea_time = request.GET.get('private_sea_time')
    private_sea_length = request.GET.get('private_sea_length')
    data = models.Setting_storage.objects.all().update(
        private_sea_time=private_sea_time,
        private_sea_length=private_sea_length)
    resultdict = {}
    resultdict['private_sea_time'] = private_sea_time
    resultdict['private_sea_length'] = private_sea_length
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def table_simple_get_edit(request):
    shop_id = request.GET.get('shop_id')
    leixing = request.GET.get('leixing')
    if leixing == '公海':
        edit_data = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_id=shop_id)
    else:
        edit_data = models.Dazhongdianping_liren_user_data.objects.filter(
            shop_id=shop_id)
    edit = ''
    for p in edit_data:
        edit = p.shop_edit
    edit = re.split("￥", edit)
    print(edit)
    dict = []
    for p in edit:
        dict.append({'label': '' + p + '', 'id': '' + p + ''})
    global pull_edit
    pull_edit = edit
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def edit_shop_add_form_data(request):
    shop_id = request.GET.get('shop_id')
    leixing = request.GET.get('leixing')
    index = int(request.GET.get('index'))
    value = request.GET.get('value')
    if leixing == '公海':
        edit_form = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_id=shop_id)
    else:
        edit_form = models.Dazhongdianping_liren_user_data.objects.filter(
            shop_id=shop_id)

    edit = ""
    for p in edit_form:
        edit = p.shop_add_form
    edit = eval(edit)
    edit[index]['value'] = value
    models.Dazhongdianping_liren_all_data.objects.filter(
        shop_id=shop_id).update(shop_add_form=edit)
    models.Dazhongdianping_liren_user_data.objects.filter(
        shop_id=shop_id).update(shop_add_form=edit)
    return JsonResponse(1, safe=False)


@csrf_exempt
def edit_shop_add_form_data_edit_baifang(request):
    edit_id = request.GET.get('id')
    shop_id = request.GET.get('shop_id')
    index = int(request.GET.get('index'))
    value = request.GET.get('value')
    edit_form = models.My_visit.objects.filter(id=edit_id)
    edit = ""
    for p in edit_form:
        edit = p.visit_data
    edit = eval(edit)
    edit[index]['value'] = value
    models.My_visit.objects.filter(id=edit_id).update(visit_data=edit)
    models.Dazhongdianping_liren_user_data.objects.filter(
        shop_id=shop_id).update(shop_add_form=edit)
    return JsonResponse(1, safe=False)


@csrf_exempt
def edit_shop_add_form_data_baifang(request):
    data = datetime.date.today()
    shop_id = request.GET.get('shop_id')
    shop_name = request.GET.get('shop_name')
    username = request.GET.get('username')
    form_data = request.GET.get('form_data')
    shop_kp_categorys = request.GET.get('shop_kp_categorys')
    time = request.GET.get('time')
    print('form_data', eval(form_data))
    form_data = eval(form_data)
    for f in range(0, len(form_data)):
        if '备注' in form_data[f]['label'] or '备注' == form_data[f]['label']:
            a = models.Dazhongdianping_liren_user_data.objects.filter(
                shop_id=shop_id)
            edit_data = ''
            for i in a:
                edit_data = i.shop_edit
            models.Dazhongdianping_liren_user_data.objects.filter(
                shop_id=shop_id).update(shop_edit=edit_data + '修改人:' +
                                                  username + '，时间:' + str(data) +
                                                  '，内容:' + form_data[f]['value'] + '￥')
        if '类别' in form_data[f]['label'] or '类别' == form_data[f]['label']:
            print(form_data[f]['value'])
            print('shop_id', shop_id)
            models.Dazhongdianping_liren_user_data.objects.filter(
                shop_id=shop_id).update(shop_kp_category=form_data[f]['value'])
    test = models.Dazhongdianping_liren_user_data.objects.filter(
        shop_id=shop_id)
    tag = ''
    for i in test:
        tag = i.shop_tags
    if tag == '新签' or tag == '续约':
        shop_kp_categorys = ''
    print('tags', tag)
    models.Dazhongdianping_liren_user_data.objects.filter(
        shop_id=shop_id).update(shop_add_form=form_data)
    models.My_visit.objects.create(
        visit_shop_name=shop_name,
        visit_id=shop_id,
        visit_name=username,
        visit_data=form_data,
        visit_time=time,
    )
    return JsonResponse(1, safe=False)


@csrf_exempt
def edit_order_form_data(request):
    shop_id = request.GET.get('shop_id')
    index = int(request.GET.get('index'))
    value = request.GET.get('value')
    print('shop_id', shop_id)
    edit_form = models.Order.objects.filter(sign_contract_shop=shop_id)
    edit = ""
    for p in edit_form:
        edit = p.order_form
    print(edit_form)
    edit = eval(edit)
    edit[index]['value'] = value
    models.Order.objects.filter(sign_contract_shop=shop_id).update(
        order_form=edit)
    return JsonResponse(1, safe=False)


@csrf_exempt
def table_simple_data_edit(request):
    data = datetime.date.today()
    shop_id = request.GET.get('shop_id')
    shop_edit_data = request.GET.get('shop_edit')
    shop_region = request.GET.get('shop_region')
    shop_business_district = request.GET.get('shop_business_district')
    shop_category = request.GET.get('shop_category')
    shop_address = request.GET.get('shop_address')
    user_name = request.GET.get('user_name')
    shop_tags = request.GET.get('shop_tags')
    shop_kp_name = request.GET.get('shop_kp_name')
    shop_telephonenumber = request.GET.get('shop_telephonenumber')
    shop_kp_position = request.GET.get('shop_kp_position')
    shop_kp_wechat_id = request.GET.get('shop_kp_wechat_id')
    shop_kp_city = request.GET.get('shop_kp_city')
    shop_kp_category = request.GET.get('shop_kp_category')
    shop_effect = request.GET.get('shop_effect')
    shop_service = request.GET.get('shop_service')
    shop_surroundings = request.GET.get('shop_surroundings')
    if shop_tags == '1':
        shop_tags = '新签,'
    elif shop_tags == '2':
        shop_tags = '断约,'
    elif shop_tags == '3':
        shop_tags = '续约,'
    elif shop_tags == '4':
        shop_tags = '新店,'
    else:
        shop_tags = shop_tags
    if shop_edit_data == None:
        delete_data = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_id=shop_id
        ).update(
            shop_tags=shop_tags,
            # shop_start=shop_start,
            # shop_review_count=shop_review_count,
            # shop_per_capita_consumption=shop_per_capita_consumption,
            # shop_effect=shop_effect,
            # shop_service=shop_service,
            # shop_surroundings=shop_surroundings,
            shop_region=shop_region,
            shop_business_district=shop_business_district,
            shop_category=shop_category,
            shop_address=shop_address,
            shop_kp_name=shop_kp_name,
            shop_telephonenumber=shop_telephonenumber,
            shop_kp_position=shop_kp_position,
            shop_kp_wechat_id=shop_kp_wechat_id,
            shop_kp_city=shop_kp_city,
            shop_effect=shop_effect,
            shop_surroundings=shop_surroundings,
            shop_service=shop_service,
            shop_kp_category=shop_kp_category)
        if delete_data != None:
            resultdict = {}
            resultdict['code'] = 0
            resultdict['msg'] = ""
            resultdict['state'] = 1
            return JsonResponse(resultdict, safe=False)
    elif shop_edit_data != None:
        edit_data = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_id=shop_id)
        form_data = ''
        for i in edit_data:
            form_data = i.shop_edit
        delete_data = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_id=shop_id
        ).update(
            shop_edit=form_data + '修改人:' + user_name + '，时间:' + str(data) +
                      '，内容:' + shop_edit_data + '￥',
            shop_tags=shop_tags,
            # shop_start=shop_start,
            # shop_review_count=shop_review_count,
            # shop_per_capita_consumption=shop_per_capita_consumption,
            # shop_effect=shop_effect,
            # shop_service=shop_service,
            # shop_surroundings=shop_surroundings,
            shop_region=shop_region,
            shop_business_district=shop_business_district,
            shop_category=shop_category,
            shop_address=shop_address,
            shop_kp_name=shop_kp_name,
            shop_telephonenumber=shop_telephonenumber,
            shop_kp_position=shop_kp_position,
            shop_kp_wechat_id=shop_kp_wechat_id,
            shop_kp_city=shop_kp_city,
            shop_effect=shop_effect,
            shop_surroundings=shop_surroundings,
            shop_service=shop_service,
            shop_kp_category=shop_kp_category)
        if delete_data != None:
            resultdict = {}
            resultdict['code'] = 0
            resultdict['msg'] = ""
            resultdict['state'] = 1
            return JsonResponse(resultdict, safe=False)


@csrf_exempt
def table_simple_get_form(request):
    shop_id = request.GET.get('shop_id')
    leixing = request.GET.get('leixing')
    if leixing == '私海':
        edit_form = models.Dazhongdianping_liren_user_data.objects.filter(
            shop_id=shop_id)
    else:
        edit_form = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_id=shop_id)
    edit = ""
    for p in edit_form:
        edit = p.shop_add_form
        print('p.shop_add_form', p.shop_add_form)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['data'] = eval(edit)
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def table_simple_get_order_form(request):
    edit_form = models.Setting_storage.objects.all()
    edit = ""
    for p in edit_form:
        edit = p.order_form
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['data'] = eval(edit)
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def table_simple_get_todo_form(request):
    edit_form = models.Setting_storage.objects.all()
    edit = ""
    for p in edit_form:
        edit = p.todo_form
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['data'] = eval(edit)
    print(edit)
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def table_simple_get_order_form(request):
    edit_form = models.Setting_storage.objects.all()
    edit = ""
    for p in edit_form:
        edit = p.order_form
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['data'] = eval(edit)
    print(edit)
    return JsonResponse(resultdict, safe=False)


# 显示标签信息
@csrf_exempt
@required_login
def table_simple_get_tags(request):
    shop_id = request.POST.get('shop_id')
    print(shop_id)
    tags_data = models.Dazhongdianping_liren_all_data.objects.filter(
        shop_id=shop_id)
    tags = ''
    for p in tags_data:
        tags = p.shop_tags
    tags = re.split("￥", tags)
    print(tags)
    return JsonResponse(tags, safe=False)


@csrf_exempt
@required_login
def table_simple_get_tags_new(request):
    shop_id = request.POST.get('shop_id')
    tags_data = models.Dazhongdianping_liren_new_all_data.objects.filter(
        shop_id=shop_id)
    tags = ''
    for p in tags_data:
        tags = p.shop_tags
    tags = re.split(",", tags)
    print(tags)
    return JsonResponse(tags, safe=False)


@csrf_exempt
@required_login
def table_simple_get_tags_user(request):
    shop_id = request.POST.get('shop_id')
    tags_data = models.Dazhongdianping_liren_user_data.objects.filter(
        shop_id=shop_id)
    tags = ''
    for p in tags_data:
        tags = p.shop_tags
    tags = re.split(",", tags)
    return JsonResponse(tags, safe=False)


@csrf_exempt
# 显示标签信息
def get_user_shop(request):
    username = request.GET.get('username')
    user_data = models.Dazhongdianping_liren_user_data.objects.filter(
        username=username)
    shop_kp_name = ''
    shop_telephonenumber = ''
    shop_region = ''
    dict = []
    for i in user_data:
        dict.append({'label': i.shop_name, 'id': i.shop_id})
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['shop_kp_name'] = shop_kp_name
    resultdict['shop_telephonenumber'] = shop_telephonenumber
    resultdict['shop_region'] = shop_region
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def get_shop_name(request):
    username = request.GET.get('username')
    month = request.GET.get('month')
    todo = models.To_do.objects.filter(username=username, time__icontains=month)
    pending_review = models.Pending_review.objects.filter(username=username, time__icontains=month)
    completed = models.Completed.objects.filter(username=username, time__icontains=month)
    todo_dict = []
    for t in todo:
        todo_dict.append({'label': t.shop_name, 'value': t.shop_name})
    pending_review_dict = []
    for t in pending_review:
        pending_review_dict.append({
            'label': t.shop_name,
            'value': t.shop_name
        })
    completed_dict = []
    for t in completed:
        completed_dict.append({'label': t.shop_name, 'value': t.shop_name})
    todo_dict = [dict(t) for t in set([tuple(d.items()) for d in todo_dict])]
    pending_review_dict = [
        dict(t) for t in set([tuple(d.items()) for d in pending_review_dict])
    ]
    completed_dict = [
        dict(t) for t in set([tuple(d.items()) for d in completed_dict])
    ]
    todo_dict.append({'label': '待办事项', 'value': '待办事项'})
    pending_review_dict.append({'label': '待审核事项', 'value': '待审核事项'})
    completed_dict.append({'label': '已完成事项', 'value': '已完成事项'})
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['todo_dict'] = todo_dict
    resultdict['pending_review_dict'] = pending_review_dict
    resultdict['completed_dict'] = completed_dict
    print('todo_dict', todo_dict)
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def get_shop_date(request):
    shop_id = request.GET.get('shop_id')
    user_data = models.Dazhongdianping_liren_user_data.objects.filter(
        shop_id=shop_id)
    print('id', shop_id)
    shop_kp_name = ''
    shop_telephonenumber = ''
    shop_region = ''
    shop_name = ''
    dict = []
    for i in user_data:
        dict.append({'label': i.shop_name, 'id': i.shop_id})
        shop_kp_name = i.shop_kp_name
        shop_telephonenumber = i.shop_telephonenumber
        shop_region = i.shop_region
        shop_name = i.shop_name
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['shop_kp_name'] = shop_kp_name
    resultdict['shop_name'] = shop_name
    resultdict['shop_telephonenumber'] = shop_telephonenumber
    resultdict['shop_region'] = shop_region
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
@required_login
def table_simple_new_get_tags(request):
    shop_id = request.POST.get('shop_id')
    tags_data = models.Dazhongdianping_liren_new_all_data.objects.filter(
        shop_id=shop_id)
    tags = ''
    for p in tags_data:
        tags = p.shop_tags
    tags = re.split(",", tags)
    return JsonResponse(tags, safe=False)


@csrf_exempt
def get_form(request):
    edit_form = models.Setting_storage.objects.all()
    edit = ""
    for p in edit_form:
        edit = p.edit_form
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['data'] = eval(edit)
    print(edit)
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def get_order_form(request):
    edit_form = models.Setting_storage.objects.all()
    edit = ""
    for p in edit_form:
        edit = p.order_form
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['data'] = eval(edit)
    print(edit)
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def get_todo_form(request):
    edit_form = models.Setting_storage.objects.all()
    edit = ""
    for p in edit_form:
        edit = p.todo_form
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['data'] = eval(edit)
    print(edit)
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def get_commission_form(request):
    edit_form = models.Setting_storage.objects.all()
    edit = ""
    for p in edit_form:
        edit = p.commission_form
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['data'] = eval(edit)
    print(edit)
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def edit_form(request):
    edit_data = request.GET.get('edit_data')
    print(edit_data)
    edit_form = models.Setting_storage.objects.update(edit_form=edit_data)
    return JsonResponse(1, safe=False)


@csrf_exempt
def edit_order_form(request):
    edit_data = request.GET.get('edit_data')
    print(edit_data)
    edit_form = models.Setting_storage.objects.update(order_form=edit_data)
    return JsonResponse(1, safe=False)


@csrf_exempt
def edit_todo_form(request):
    edit_data = request.GET.get('edit_data')
    # 先获取之前的日期
    for i in eval(edit_data):
        if i['select'] == '重复任务':
            old = models.Setting_storage.objects.all()
            # 之前的时间
            old_time = eval(old[0].todo_form)
            for old_t in old_time:
                if old_t['name'] == i['name']:
                    old_time = old_t['time']
                    # 现在更新的时间
                    new_time = i['time']
                    # 获取订单
                    Order = models.Order.objects.filter(tags__in=('续约', '新签'))
                    # 订单获取完成，需要匹配任务，包括已完成，未完成，待审核
                    # 匹配完成之后怎么修改日期呢？ 每个任务只有ID和任务名不一样，根据ID无法判断，只能根据任务名
                    # 首先应该先创建任务，按照创建订单时创建任务的方法创建，然后去待完成，待审核，已完成里匹配，最后对匹配成功的修改
                    for o in Order:
                        # 开始的时间
                        date_time = o.order_start_date
                        year = int(date_time[0:4])
                        month = int(date_time[5:7])
                        if '10' in date_time[5:7]:
                            month = '10'
                        else:
                            if '0' in date_time[5:7]:
                                month = int(date_time[6:7])
                        day = int(date_time[8:10])
                        cur_day = datetime.date(year, month, day)
                        # 结束的时间
                        date_time_end = o.order_end_date
                        year_end = int(date_time_end[0:4])
                        month_end = int(date_time_end[5:7])
                        if '10' in date_time_end[5:7]:
                            month_end = '10'
                        else:
                            if '0' in date_time_end[5:7]:
                                month_end = int(date_time_end[6:7])
                        day_end = int(date_time_end[8:10]) - 1
                        # 订单开始的时间
                        cur_day = datetime.date(year, month, day)
                        # 订单结束的时间
                        next_day = datetime.date(int(year_end), int(month_end),
                                                 int(day_end))
                        # 　两个日期之间的差值
                        difference = int((next_day - cur_day).days)
                        count = int(difference) / int(new_time)
                        old_count = int(difference) / int(old_time)
                        commission_point = 0
                        commission_point_data = models.Setting_storage.objects.all(
                        )
                        commission_point_json = ''
                        for c in commission_point_data:
                            commission_point_json = c.commission_form
                        count_c = []
                        for o_c in eval(commission_point_json):
                            count_c.append(int(o_c['commission_performance']))
                        for a in sorted(count_c):
                            if int(o.order_amount) >= a:
                                for c_o in eval(commission_point_json):
                                    if a == int(c_o['commission_performance']):
                                        commission_point = int(
                                            c_o['commission_commission_point'])
                        count = round(count)
                        old_count = round(old_count)
                        original_time = cur_day
                        money = int(o.order_amount) * (int(commission_point) /
                                                       100) * (1 / 3)
                        money = money * 2
                        print(count + 1)
                        for b in range(0, count + 1):
                            if count > old_count:
                                # 创建任务
                                # 查询任务是否存在
                                todo_create = models.To_do.objects.filter(
                                    order_id=o.contract_id,
                                    project='第' + str(b + 1) + '次' + i['name'])
                                completed_create = models.Completed.objects.filter(
                                    order_id=o.contract_id,
                                    project='第' + str(b + 1) + '次' + i['name'])
                                pending_review_create = models.Pending_review.objects.filter(
                                    order_id=o.contract_id,
                                    project='第' + str(b + 1) + '次' + i['name'])

                                if todo_create.count(
                                ) != 0 and completed_create.count(
                                ) == 0 and pending_review_create.count() == 0:
                                    models.To_do.objects.update(
                                        project='第' + str(b + 1) + '次' +
                                                i['name'],
                                        shop_name=o.sign_contract_shop,
                                        order_id=o.contract_id,
                                        # 开始日期加上任务的时间
                                        time=original_time + datetime.timedelta(
                                            days=int(new_time)),
                                        money=money,
                                        schedule=0,
                                        username=o.order_contract_sales,
                                        status='未审核')
                                elif todo_create.count(
                                ) == 0 and completed_create.count(
                                ) != 0 and pending_review_create.count() == 0:
                                    models.Completed.objects.update(
                                        project='第' + str(b + 1) + '次' +
                                                i['name'],
                                        shop_name=o.sign_contract_shop,
                                        order_id=o.contract_id,
                                        # 开始日期加上任务的时间
                                        time=original_time + datetime.timedelta(
                                            days=int(new_time)),
                                        money=money,
                                        schedule=0,
                                        username=o.order_contract_sales,
                                        status='未审核')
                                elif todo_create.count(
                                ) == 0 and completed_create.count(
                                ) == 0 and pending_review_create.count() != 0:
                                    models.Pending_review.objects.update(
                                        project='第' + str(b + 1) + '次' +
                                                i['name'],
                                        shop_name=o.sign_contract_shop,
                                        order_id=o.contract_id,
                                        # 开始日期加上任务的时间
                                        time=original_time + datetime.timedelta(
                                            days=int(new_time)),
                                        money=money,
                                        schedule=0,
                                        username=o.order_contract_sales,
                                        status='未审核')
                                elif todo_create.count(
                                ) == 0 and completed_create.count(
                                ) == 0 and pending_review_create.count() == 0:
                                    print('第', str(b + 1), '次')
                                    quchong = models.To_do.objects.filter(
                                        project='第' + str(b + 1) + '次' +
                                                i['name'],
                                        shop_name=o.sign_contract_shop,
                                        order_id=o.contract_id,
                                        # 开始日期加上任务的时间
                                        time=original_time + datetime.timedelta(
                                            days=int(new_time)),
                                        money=money,
                                        schedule=0,
                                        username=o.order_contract_sales,
                                        status='未审核')
                                    print('quchong', quchong.count())
                                    if quchong.count() == 0:
                                        quchong_data = models.To_do.objects.create(
                                            project='第' + str(b + 1) + '次' +
                                                    i['name'],
                                            shop_name=o.sign_contract_shop,
                                            order_id=o.contract_id,
                                            # 开始日期加上任务的时间
                                            time=original_time + datetime.timedelta(
                                                days=int(new_time)),
                                            money=money,
                                            schedule=0,
                                            username=o.order_contract_sales,
                                            status='未审核')
                                        print('去重')
                                    else:
                                        print(quchong.count())
                            if old_count > count:
                                todo_data = models.To_do.objects.filter(
                                    order_id=o.contract_id)
                                completed_data = models.Completed.objects.filter(
                                    order_id=o.contract_id)
                                pending_review_data = models.Pending_review.objects.filter(
                                    order_id=o.contract_id)
                                print(old_count - count)
                                count_data = todo_data.count(
                                ) + completed_data.count(
                                ) + pending_review_data.count()
                                for old in range(0, old_count - count):
                                    print('第' + str(count_data) + '次' +
                                          i['name'])
                                    todo_delete = models.To_do.objects.filter(
                                        order_id=o.contract_id,
                                        project='第' + str(count_data) + '次' +
                                                i['name']).delete()
                                    completed_delete = ''
                                    if str(todo_delete) == '<QuerySet []>':
                                        completed_delete = models.Completed.objects.filter(
                                            order_id=o.contract_id,
                                            project='第' + str(count_data) +
                                                    '次' + i['name']).delete()
                                    elif str(completed_delete
                                             ) == '<QuerySet []>':
                                        pending_review_delete = models.Pending_review.objects.filter(
                                            order_id=o.contract_id,
                                            project='第' + str(count_data) +
                                                    '次' + i['name']).delete()
                                    count_data = count_data - 1
                                old_count = count
                            # todo = models.To_do.objects.filter(order_id=o.order_id,project='第'+str(b+1)+'次' + i['time'])
                            todo = models.To_do.objects.filter(
                                order_id=o.contract_id,
                                project='第' + str(b + 1) + '次' + i['name'])
                            completed = models.Completed.objects.filter(
                                order_id=o.contract_id,
                                project='第' + str(b + 1) + '次' + i['name'])
                            pending_review = models.Pending_review.objects.filter(
                                order_id=o.contract_id,
                                project='第' + str(b + 1) + '次' + i['name'])
                            if str(todo) != '<QuerySet []>' and str(
                                    completed) == '<QuerySet []>' and str(
                                pending_review) == '<QuerySet []>':
                                models.To_do.objects.filter(
                                    order_id=o.contract_id,
                                    project='第' + str(b + 1) + '次' +
                                            i['name']).update(time=original_time + datetime.timedelta(
                                    days=int(new_time)))
                            elif str(todo) == '<QuerySet []>' and str(
                                    completed) != '<QuerySet []>' and str(
                                pending_review) == '<QuerySet []>':
                                models.Completed.objects.filter(
                                    order_id=o.contract_id,
                                    project='第' + str(b + 1) + '次' +
                                            i['name']).update(time=original_time + datetime.timedelta(
                                    days=int(new_time)))
                            elif str(todo) == '<QuerySet []>' and str(
                                    completed) == '<QuerySet []>' and str(
                                pending_review) != '<QuerySet []>':
                                models.Pending_review.objects.filter(
                                    order_id=o.contract_id,
                                    project='第' + str(b + 1) + '次' +
                                            i['name']).update(time=original_time + datetime.timedelta(
                                    days=int(new_time)))
                            original_time = original_time + datetime.timedelta(
                                days=int(new_time))

    edit_form = models.Setting_storage.objects.update(todo_form=edit_data)
    todo_quchong = models.To_do.objects.all()
    project = ''
    order_id = ''
    shop_name = ''
    schedule = ''
    username = ''
    status = ''
    money = ''
    a = 0
    for t in todo_quchong:
        if a == 0:
            project = t.project
            order_id = t.order_id
            shop_name = t.shop_name
            schedule = t.schedule
            username = t.username
            status = t.status
            money = t.money
        else:
            project = t.project
            order_id = t.order_id
            shop_name = t.shop_name
            schedule = t.schedule
            username = t.username
            status = t.status
            money = t.money
            if models.To_do.objects.filter(project=project,
                                           order_id=t.order_id).count() != 0:
                models.To_do.objects.filter(project=project,
                                            order_id=t.order_id).delete()
                models.To_do.objects.create(
                    project=t.project,
                    shop_name=t.shop_name,
                    time=t.time,
                    money=t.money,
                    schedule=t.schedule,
                    username=t.username,
                    status=t.status,
                    order_id=t.order_id,
                )
        a = a + 1
    # models.To_do.objects.filter()
    return JsonResponse(1, safe=False)


@csrf_exempt
def edit_commission_form(request):
    edit_data = request.GET.get('edit_data')
    edit_form = models.Setting_storage.objects.update(
        commission_form=edit_data)
    print(edit_form)
    return JsonResponse(1, safe=False)


# 显示编辑信息
@csrf_exempt
@required_login
def table_simple_new_get_edit(request):
    shop_id = request.POST.get('shop_id')
    name = request.POST.get('name')
    if name == 'user':
        edit_data = models.Dazhongdianping_liren_user_data.objects.filter(
            shop_id=shop_id)
        edit = ''
        for p in edit_data:
            edit = p.shop_edit
        edit = re.split(" ", edit)
        print(edit)
        return JsonResponse(edit, safe=False)
    else:
        print(shop_id)
        edit_data = models.Dazhongdianping_liren_new_all_data.objects.filter(
            shop_id=shop_id)
        edit = ''
        for p in edit_data:
            edit = p.shop_edit
        edit = re.split(" ", edit)
        print(edit)
        return JsonResponse(edit, safe=False)


# 销售私海数据展示
@csrf_exempt
@required_login
def table_simple_private_sea_data(request):
    page = request.GET.get('page')
    rows = request.GET.get('limit')
    name = request.GET.get("search")
    search_shop_category = request.GET.get("search_shop_category")
    print(search_shop_category)
    if search_shop_category != '全部':
        problems = models.Dazhongdianping_liren_user_data.objects.filter(
            username=search_shop_category)
    elif search_shop_category == '全部':
        problems = models.Dazhongdianping_liren_user_data.objects.all()
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    print(problems)
    total = problems.count()
    problems = problems[i:j]
    resultdict = {}
    resultdict['total'] = total
    dict = []
    data = {"rows": dict, "total": total}
    for p in problems:
        dic = {}
        dic['username'] = p.username
        # 根据ID查询评论数，星级
        dic['shop_id'] = p.shop_id
        dic['shop_name'] = p.shop_name
        dic['shop_start'] = p.shop_start
        dic['shop_review_count'] = p.shop_review_count
        dic['shop_bad_review'] = p.shop_bad_review
        dic['shop_per_capita_consumption'] = p.shop_per_capita_consumption
        dic['shop_effect'] = p.shop_effect
        dic['shop_service'] = p.shop_service
        dic['shop_surroundings'] = p.shop_surroundings
        dic['shop_region'] = p.shop_region
        dic['shop_business_district'] = p.shop_business_district
        dic['shop_category'] = p.shop_category
        dic['shop_address'] = p.shop_address
        dic['shop_telephonenumber'] = p.shop_telephonenumber
        dict.append(dic)
    return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
@required_login
def change_private_sea_username(request):
    problems = models.Dazhongdianping_liren_user_data.objects.all()
    dict = []
    for p in problems:
        dict.append(p.username)
    dict2 = list(set(dict))
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 0
    resultdict['data'] = dict2
    print(dict2)
    return JsonResponse(resultdict, safe=False)


# 新店商户数据显示
@csrf_exempt
@required_login
def table_simple_new_data(request):
    page = request.GET.get('page')
    rows = request.GET.get('limit')
    name = request.GET.get("search")
    shop_business_district = request.GET.get(
        'search_shop_business_district')  # 区域
    shop_category = request.GET.get('search_shop_category')  # 商圈
    shop_region = request.GET.get('search_shop_region')  # 品类
    print('区域', shop_business_district)
    print('品类', shop_region)
    print('商圈:', shop_category)
    shop_business_district = shop_business_district[0:2]
    print('要搜索的区域', shop_business_district)
    # 搜索逻辑
    # 区域和商圈等于空
    if shop_business_district == '全部' and shop_region != '全部' and shop_category == '全部':
        problems = models.Dazhongdianping_liren_new_all_data.objects.filter(
            shop_region=shop_region)
    # 商圈和品类等于空
    elif shop_business_district != '全部' and shop_category == '全部' and shop_region == '全部':
        problems = models.Dazhongdianping_liren_new_all_data.objects.filter(
            shop_business_district__contains=shop_business_district)
    # 区域和品类等于空
    elif shop_category != '全部' and shop_region != '全部' and shop_business_district == '全部':
        problems = models.Dazhongdianping_liren_new_all_data.objects.filter(
            shop_category=shop_category)
    # 区域和商圈不等于空
    elif shop_business_district != '全部' and shop_category != '全部' and shop_region == '全部':
        problems = models.Dazhongdianping_liren_new_all_data.objects.filter(
            shop_business_district__contains=shop_business_district,
            shop_category=shop_category)
    # 商圈和品类不等于空
    elif shop_region != '全部' and shop_category != '全部' and shop_business_district == '全部':
        problems = models.Dazhongdianping_liren_new_all_data.objects.filter(
            shop_region=shop_region, shop_category__contains=shop_category)
    # 区域和品类不等于空
    elif shop_business_district != '全部' and shop_region != '全部' and shop_category == '全部':
        problems = models.Dazhongdianping_liren_new_all_data.objects.filter(
            shop_business_district__contains=shop_business_district,
            shop_region__contains=shop_region)
    elif shop_region != '全部' and shop_business_district != '全部' and shop_business_district != '全部':
        problems = models.Dazhongdianping_liren_new_all_data.objects.filter(
            shop_region__contains=shop_region,
            shop_business_district__contains=shop_business_district,
            shop_category__contains=shop_category)
    elif shop_category != '全部' and shop_business_district == '全部' and shop_region == '全部':
        problems = models.Dazhongdianping_liren_new_all_data.objects.filter(
            shop_category__contains=shop_category)
    elif name != None:
        problems = models.Dazhongdianping_liren_new_all_data.objects.filter(
            Q(shop_name__contains=name) | Q(shop_id=name) | Q(shop_start=name)
            | Q(shop_review_count=name)
            | Q(shop_per_capita_consumption=name)
            | Q(shop_region__contains=name)
            | Q(shop_business_district__contains=name)
            | Q(shop_category__contains=name) | Q(shop_address__contains=name))
    elif shop_region == '全部' and shop_business_district == '全部' and shop_category == '全部':
        problems = models.Dazhongdianping_liren_new_all_data.objects.all()
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    total = problems.count()
    problems = problems[i:j]
    # resultdict = {}
    # resultdict['total'] = total
    dict = []
    data = {"rows": dict, "total": total}
    for p in problems:
        dic = {}
        dic['shop_id'] = p.shop_id
        dic['shop_name'] = p.shop_name
        dic['shop_start'] = p.shop_start
        dic['shop_review_count'] = p.shop_review_count
        dic['shop_per_capita_consumption'] = p.shop_per_capita_consumption
        dic['shop_region'] = p.shop_region
        dic['shop_effect'] = p.shop_effect
        dic['shop_service'] = p.shop_service
        dic['shop_surroundings'] = p.shop_surroundings
        dic['shop_business_district'] = p.shop_business_district
        dic['shop_category'] = p.shop_category
        dic['shop_address'] = p.shop_address
        dic['shop_telephonenumber'] = p.shop_telephonenumber
        dic['shop_edit'] = p.shop_edit
        dic['shop_tags'] = p.shop_tags
        dict.append(dic)
    return HttpResponse(json.dumps(data), content_type="application/json")


# 签约商户数据显示
@csrf_exempt
@required_login
def table_simple_data_signing(request):
    page = request.GET.get('page')
    rows = request.GET.get('limit')
    name = request.GET.get("search")
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    problems = models.Dazhongdianping_liren_signing_data.objects.all()
    total = problems.count()
    problems = problems[i:j]
    resultdict = {}
    resultdict['total'] = total
    dict = []
    data = {"rows": dict, "total": total}
    for p in problems:
        dic = {}
        dic['shop_id'] = p.shop_id
        # 根据ID查询评论数，星级
        dic['shop_name'] = p.shop_name
        dic['shop_user'] = p.shop_user
        dic['shop_password'] = p.shop_password
        dic['shop_review_count'] = p.shop_review_count
        dic['shop_start'] = p.shop_start
        dic['shop_cookie'] = p.shop_cookie
        dic['shop_storekey'] = p.shop_storekey
        dic['shop_exposures'] = p.shop_exposures
        dic['shop_visitors'] = p.shop_visitors
        dic['shop_orders'] = p.shop_orders
        dic['shop_reservations'] = p.shop_reservations
        dic['shop_consumption'] = p.shop_consumption
        dic['shop_new_reviews_count'] = p.shop_new_reviews_count
        dic['shop_new_bad_review'] = p.shop_new_bad_review
        dic['shop_bad_review_response'] = p.shop_bad_review_response
        dict.append(dic)
    return HttpResponse(json.dumps(data), content_type="application/json")


def transfer_details_page(request):
    problems = models.Dazhongdianping_liren_signing_data.objects.all()
    return render(request, "lyear_echarts.html", {"dFata": problems})


@csrf_exempt
def city_statistics(request):
    city = request.GET.get('city')
    print(city)
    problems = models.Dazhongdianping_liren_all_data.objects.filter(
        shop_city=city)
    dist = []
    for i in problems:
        dist.append(i.shop_business_district)
    urban_area_data = list(set(dist))
    i = 0
    while i < len(urban_area_data):
        if '区' not in urban_area_data[i]:
            urban_area_data.pop(i)
            i -= 1
        else:
            pass
        i += 1
    # 区域筛选
    dict = []
    # print(urban_area_data)
    for i in urban_area_data:
        dic = {}
        dic['quyu'] = i
        dic['meifa'] = problems.filter(shop_business_district__contains=i,
                                       shop_region='美发').count()
        dic['meirong'] = problems.filter(shop_business_district__contains=i,
                                         shop_region='美容/SPA').count()
        dic['meijiameijie'] = problems.filter(
            shop_business_district__contains=i, shop_region='美甲美睫').count()
        dic['yixuemeirong'] = problems.filter(
            shop_business_district__contains=i, shop_region='医学美容').count()
        dic['yujia'] = problems.filter(shop_business_district__contains=i,
                                       shop_region='瑜伽').count()
        dic['wudao'] = problems.filter(shop_business_district__contains=i,
                                       shop_region='舞蹈').count()
        dic['wenxiu'] = problems.filter(shop_business_district__contains=i,
                                        shop_region='纹绣').count()
        dic['shoushenxianti'] = problems.filter(
            shop_business_district__contains=i, shop_region='瘦身纤体').count()
        dic['wenshen'] = problems.filter(shop_business_district__contains=i,
                                         shop_region='纹身').count()
        dic['qudou'] = problems.filter(shop_business_district__contains=i,
                                       shop_region='祛痘').count()
        dic['huazhuangping'] = problems.filter(
            shop_business_district__contains=i, shop_region='化妆品').count()
        dic['chanhousuxing'] = problems.filter(
            shop_business_district__contains=i, shop_region='产后塑形').count()
        dic['yangfa'] = problems.filter(shop_business_district__contains=i,
                                        shop_region='养发').count()
        dict.append(dic)
    models.Citydata.objects.filter(city=city).update(data=dict)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


def select_citydata(request):
    city = request.GET.get('city')
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['state'] = 1
    resultdict['data'] = eval(
        models.Citydata.objects.filter(city=city).first().data)
    return JsonResponse(resultdict, safe=False)


def update_city(request):
    city = request.GET.get("city")
    username = request.GET.get("username")
    print(city)
    print(username)
    db = pymysql.connect("localhost", "root", "bakj123456", "rock")
    cursor = db.cursor()
    cursor.execute("UPDATE user_userprofile  SET introduction='" + city +
                   "'  where first_name='" + username + "'")
    db.commit()
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    cursor.close()
    # 关闭数据库连接
    db.close()
    return JsonResponse(resultdict, safe=False)


def select_city(request):
    username = request.GET.get("username")
    db = pymysql.connect("localhost", "root", "bakj123456", "rock")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_userprofile where first_name='" +
                   username + "'")
    data = cursor.fetchall()
    admin = ''
    for row in data:
        admin = row[13]
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['data'] = admin
    cursor.close()
    # 关闭数据库连接
    db.close()
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def select_user(request):
    username = request.GET.get("username")
    db = pymysql.connect("localhost", "root", "bakj123456", "rock")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_userprofile where first_name='" +
                   username + "'")
    data = cursor.fetchall()
    admin = ''
    for row in data:
        admin = row[11]
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['data'] = admin
    cursor.close()
    # 关闭数据库连接
    db.close()
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def create_user(request):
    db = pymysql.connect("localhost", "root", "bakj123456", "rock")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_userprofile")
    data = cursor.fetchall()
    dict = []
    for row in data:
        dic = {}
        dic['first_name'] = row[5]
        dic['username'] = row[4]
        dic['avatar'] = row[11]
        dic['group'] = row[14]
        dict.append(dic)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['data'] = dict
    cursor.close()
    # 关闭数据库连接
    db.close()
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def create_user_data(request):
    username = request.GET.get('username')
    first_name = request.GET.get('first_name')
    avatar = request.GET.get('avatar')
    group = request.GET.get('group')
    db = pymysql.connect("localhost", "root", "bakj123456", "rock")
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO user_userprofile(id,password, last_login, is_superuser, username,first_name,last_name,email,is_staff,is_active,date_joined,avatar,role,introduction,group_name) VALUES (Null, 'pbkdf2_sha256$150000$VoNrmhBIWqeu$NqcuyPp8KjuLGzk1z1xVe22fE46vfg2LSKcnjD5+AYc=', Null, '1', '"
        + username + "','" + first_name +
        "','张','admin@13.com','1','1','2020-01-31 13:11:18.000000','" +
        avatar + "','admin','北京市','" + group + "')")
    db.commit()
    cursor.close()
    # 关闭数据库连接
    db.close()
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""

    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def delete_user(request):
    username = request.GET.get('username')
    db = pymysql.connect("localhost", "root", "bakj123456", "rock")
    cursor = db.cursor()
    cursor.execute("DELETE FROM user_userprofile WHERE username = '" +
                   username + "'")
    db.commit()
    cursor.close()
    # 关闭数据库连接
    db.close()
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    return JsonResponse(resultdict, safe=False)


# 更改商户备注信息
@csrf_exempt
def dadata_edit(request):
    data = datetime.date.today()
    shop_id = request.GET.get('shop_id')
    shop_edit_data = request.GET.get('shop_edit')
    shop_region = request.GET.get('shop_region')
    shop_business_district = request.GET.get('shop_business_district')
    shop_category = request.GET.get('shop_category')
    shop_address = request.GET.get('shop_address')
    user_name = request.GET.get('user_name')
    shop_tags = request.GET.get('shop_tags')
    shop_kp_name = request.GET.get('shop_kp_name')
    shop_telephonenumber = request.GET.get('shop_telephonenumber')
    shop_kp_position = request.GET.get('shop_kp_position')
    shop_kp_wechat_id = request.GET.get('shop_kp_wechat_id')
    shop_kp_city = request.GET.get('shop_kp_city')
    shop_kp_category = request.GET.get('shop_kp_category')
    shop_effect = request.GET.get('shop_effect')
    shop_service = request.GET.get('shop_service')
    shop_surroundings = request.GET.get('shop_surroundings')
    if shop_tags == '1':
        shop_tags = '新签,'
    elif shop_tags == '2':
        shop_tags = '断约,'
    elif shop_tags == '3':
        shop_tags = '续约,'
    elif shop_tags == '4':
        shop_tags = '新店,'
    else:
        shop_tags = shop_tags
    if shop_edit_data == None:
        delete_data = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_id=shop_id
        ).update(
            shop_tags=shop_tags,
            # shop_start=shop_start,
            # shop_review_count=shop_review_count,
            # shop_per_capita_consumption=shop_per_capita_consumption,
            # shop_effect=shop_effect,
            # shop_service=shop_service,
            # shop_surroundings=shop_surroundings,
            shop_region=shop_region,
            shop_business_district=shop_business_district,
            shop_category=shop_category,
            shop_address=shop_address,
            shop_kp_name=shop_kp_name,
            shop_telephonenumber=shop_telephonenumber,
            shop_kp_position=shop_kp_position,
            shop_kp_wechat_id=shop_kp_wechat_id,
            shop_kp_city=shop_kp_city,
            shop_effect=shop_effect,
            shop_surroundings=shop_surroundings,
            shop_service=shop_service,
            shop_kp_category=shop_kp_category)
        if delete_data != None:
            resultdict = {}
            resultdict['code'] = 0
            resultdict['msg'] = ""
            resultdict['state'] = 1
            return JsonResponse(resultdict, safe=False)
    elif shop_edit_data != None:
        edit_data = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_id=shop_id)
        print(edit_data[0].shop_edit)
        delete_data = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_id=shop_id
        ).update(
            shop_edit=edit_data[0].shop_edit + '修改人:' + user_name + '，时间:' +
                      str(data) + '，内容:' + shop_edit_data + '￥',
            shop_tags=shop_tags,
            # shop_start=shop_start,
            # shop_review_count=shop_review_count,
            # shop_per_capita_consumption=shop_per_capita_consumption,
            # shop_effect=shop_effect,
            # shop_service=shop_service,
            # shop_surroundings=shop_surroundings,
            shop_region=shop_region,
            shop_business_district=shop_business_district,
            shop_category=shop_category,
            shop_address=shop_address,
            shop_kp_name=shop_kp_name,
            shop_telephonenumber=shop_telephonenumber,
            shop_kp_position=shop_kp_position,
            shop_kp_wechat_id=shop_kp_wechat_id,
            shop_kp_city=shop_kp_city,
            shop_effect=shop_effect,
            shop_surroundings=shop_surroundings,
            shop_service=shop_service,
            shop_kp_category=shop_kp_category)
        if delete_data != None:
            resultdict = {}
            resultdict['code'] = 0
            resultdict['msg'] = ""
            resultdict['state'] = 1
            return JsonResponse(resultdict, safe=False)


# 更改商户备注信息

@csrf_exempt
def table_simple_user_data_edit(request):
    data = datetime.date.today()
    shop_edit_data = request.GET.get('shop_edit')
    shop_id = request.GET.get('shop_id')
    username = request.GET.get('username')
    if shop_edit_data == None:
        if delete_data != None:
            resultdict = {}
            resultdict['code'] = 0
            resultdict['msg'] = ""
            resultdict['state'] = 1
            return JsonResponse(resultdict, safe=False)
    elif shop_edit_data != None:
        edit_data = models.Dazhongdianping_liren_user_data.objects.filter(
            shop_id=shop_id)
        form_data = ''
        for i in edit_data:
            form_data = i.shop_edit
        delete_data = models.Dazhongdianping_liren_user_data.objects.filter(
            shop_id=shop_id).update(
            shop_edit=form_data + '修改人:' + username + '，时间:' + str(data) +
                      '，内容:' + shop_edit_data + '￥', )
        if delete_data != None:
            resultdict = {}
            resultdict['code'] = 0
            resultdict['msg'] = ""
            resultdict['state'] = 1
            return JsonResponse(resultdict, safe=False)


# 更改商户备注信息
@csrf_exempt
@required_login
def table_simple_new_data_edit(request):
    shop_id = request.POST.get('shop_id')
    shop_edit = request.POST.get('shop_edit')
    user_name = request.POST.get('user_name')
    shop_tags = request.POST.get('shop_tags')
    print('前端页面传来的新店数据', shop_tags)
    if ' ' in shop_edit:
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['shop_edit'] = shop_edit
        resultdict['state'] = 2
        return JsonResponse(resultdict, safe=False)
    elif shop_edit == "" and shop_tags != "":
        shop_edit = re.sub(r'\s+', '', shop_edit)
        resultdict = {}
        data = str(datetime.datetime.now())[0:10]
        edit_data = models.Dazhongdianping_liren_new_all_data.objects.filter(
            shop_id=shop_id)
        edit = ''
        for p in edit_data:
            edit = p.shop_edit
        delete_data = models.Dazhongdianping_liren_new_all_data.objects.filter(
            shop_id=shop_id).update(shop_tags=shop_tags)
        if delete_data != None:
            resultdict['code'] = 0
            resultdict['msg'] = ""
            resultdict['shop_edit'] = shop_edit
            resultdict['state'] = 1
            return JsonResponse(resultdict, safe=False)
    elif shop_edit != "" and shop_tags == "":
        shop_edit = re.sub(r'\s+', '', shop_edit)
        resultdict = {}
        data = str(datetime.datetime.now())[0:10]
        edit_data = models.Dazhongdianping_liren_new_all_data.objects.filter(
            shop_id=shop_id)
        edit = ''
        for p in edit_data:
            edit = p.shop_edit
        delete_data = models.Dazhongdianping_liren_new_all_data.objects.filter(
            shop_id=shop_id).update(shop_edit=edit + '修改人:' + user_name +
                                              '，时间:' + data + '，内容:' + shop_edit + ' ')
        if delete_data != None:
            resultdict['code'] = 0
            resultdict['msg'] = ""
            resultdict['shop_edit'] = shop_edit
            resultdict['state'] = 1
            return JsonResponse(resultdict, safe=False)
    elif shop_edit != "" and shop_tags != "":
        shop_edit = re.sub(r'\s+', '', shop_edit)
        resultdict = {}
        data = str(datetime.datetime.now())[0:10]
        # shop_edit = '['+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'``]:'+str(shop_edit)
        edit_data = models.Dazhongdianping_liren_new_all_data.objects.filter(
            shop_id=shop_id)
        edit = ''
        for p in edit_data:
            edit = p.shop_edit
        delete_data = models.Dazhongdianping_liren_new_all_data.objects.filter(
            shop_id=shop_id).update(shop_edit=edit + '修改人:' + user_name +
                                              '，时间:' + data + '，内容:' + shop_edit + ' ',
                                    shop_tags=shop_tags)
        if delete_data != None:
            resultdict['code'] = 0
            resultdict['msg'] = ""
            resultdict['shop_edit'] = shop_edit
            resultdict['state'] = 1
            return JsonResponse(resultdict, safe=False)
    elif shop_edit == "" or shop_tags == "":
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['shop_edit'] = shop_edit
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)


# 更改新店商户备注信息
@csrf_exempt
@required_login
def table_simple_new_data_edit(request):
    shop_id = request.POST.get('shop_id')
    shop_edit = request.POST.get('shop_edit')
    print(shop_edit)
    resultdict = {}
    # shop_edit = '['+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'``]:'+str(shop_edit)
    delete_data = models.Dazhongdianping_liren_new_all_data.objects.filter(
        shop_id=shop_id).update(shop_edit=shop_edit)
    if delete_data != None:
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['shop_edit'] = shop_edit
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)


@csrf_exempt
def pull_add(request):
    resultdict = {}
    username = request.GET.get('username')
    shop_id = request.GET.get('shop_id')
    shop_name = request.GET.get('shop_name')
    shop_start = request.GET.get('shop_start')
    shop_review_count = request.GET.get('shop_review_count')
    shop_bad_review = request.GET.get('shop_bad_review')
    shop_per_capita_consumption = request.GET.get(
        'shop_per_capita_consumption')
    shop_effect = request.GET.get('shop_effect')
    shop_surroundings = request.GET.get('shop_surroundings')
    shop_service = request.GET.get('shop_service')
    shop_region = request.GET.get('shop_region')
    shop_business_district = request.GET.get('shop_business_district')
    shop_category = request.GET.get('shop_category')
    shop_address = request.GET.get('shop_address')
    shop_telephonenumber = request.GET.get('shop_telephonenumber')
    shop_edit = request.GET.get('shop_edit')
    shop_tags = request.GET.get('shop_tags')
    shop_kp_name = request.GET.get('shop_kp_name')
    shop_kp_wechat_id = request.GET.get('shop_kp_wechat_id')
    shop_kp_city = request.GET.get('shop_kp_city')
    shop_kp_category = request.GET.get('shop_kp_category')
    shop_kp_position = request.GET.get('shop_kp_position')
    shop_add_form = request.GET.get('shop_add_form')
    shop_city = request.GET.get('shop_city')
    # position = request.POST.get('position')
    pull_date = datetime.date.today()
    private_sea_data = models.Setting_storage.objects.all()
    dict_today = []
    print('id', shop_id)
    print('username', username)
    print(shop_name)
    print('edit', shop_edit)
    print(shop_start)
    for p in private_sea_data:
        dict_today.append(p.private_sea_length)
    difference_len = dict_today[0]
    print('长度', difference_len)
    data = models.Dazhongdianping_liren_user_data.objects.filter(
        shop_id=shop_id)
    shop_count = models.Dazhongdianping_liren_user_data.objects.filter(
        username=username)
    p = models.Dazhongdianping_liren_user_data.objects.filter(
        username=username, shop_id=shop_id)
    if str(p) == '<QuerySet []>':
        if str(type(shop_tags)) == "<class 'NoneType'>":
            if len(shop_count) >= difference_len:
                print('用户下的商户数量', len(shop_count))
                resultdict['code'] = 0
                resultdict['msg'] = ""
                resultdict['state'] = 3
                return JsonResponse(resultdict, safe=False)
            else:
                if str(data) != '<QuerySet []>':
                    resultdict['code'] = 0
                    resultdict['msg'] = ""
                    resultdict['state'] = 2
                    return JsonResponse(resultdict, safe=False)
                else:
                    if shop_add_form == 'null':
                        pull_data = models.Dazhongdianping_liren_user_data.objects.create(
                            username=username,
                            shop_id=shop_id,
                            shop_name=shop_name,
                            shop_start=shop_start,
                            shop_review_count=shop_review_count,
                            shop_bad_review=shop_bad_review,
                            shop_per_capita_consumption=shop_per_capita_consumption,
                            shop_effect=shop_effect,
                            shop_surroundings=shop_surroundings,
                            shop_service=shop_service,
                            shop_region=shop_region,
                            shop_business_district=shop_business_district,
                            shop_category=shop_category,
                            shop_address=shop_address,
                            shop_telephonenumber=shop_telephonenumber,
                            shop_edit=shop_edit,
                            shop_tags=shop_tags,
                            shop_kp_name=shop_kp_name,
                            shop_kp_wechat_id=shop_kp_wechat_id,
                            shop_kp_city=shop_kp_city,
                            shop_kp_category=shop_kp_category,
                            shop_kp_position=shop_kp_position,
                            shop_city=shop_city,
                            pull_date=pull_date)
                        if pull_data != None:
                            models.Dazhongdianping_liren_all_data.objects.filter(
                                shop_id=shop_id).delete()
                            print('成功')
                            resultdict['code'] = 0
                            resultdict['msg'] = ""
                            resultdict['state'] = 1
                            return JsonResponse(resultdict, safe=False)
                    else:
                        pull_data = models.Dazhongdianping_liren_user_data.objects.create(
                            username=username,
                            shop_id=shop_id,
                            shop_name=shop_name,
                            shop_start=shop_start,
                            shop_review_count=shop_review_count,
                            shop_bad_review=shop_bad_review,
                            shop_per_capita_consumption=shop_per_capita_consumption,
                            shop_effect=shop_effect,
                            shop_surroundings=shop_surroundings,
                            shop_service=shop_service,
                            shop_region=shop_region,
                            shop_business_district=shop_business_district,
                            shop_category=shop_category,
                            shop_address=shop_address,
                            shop_telephonenumber=shop_telephonenumber,
                            shop_edit=shop_edit,
                            shop_tags=shop_tags,
                            shop_kp_name=shop_kp_name,
                            shop_kp_wechat_id=shop_kp_wechat_id,
                            shop_kp_city=shop_kp_city,
                            shop_kp_category=shop_kp_category,
                            shop_kp_position=shop_kp_position,
                            shop_add_form=eval(shop_add_form),
                            shop_city=shop_city,
                            pull_date=pull_date)
                        if pull_data != None:
                            models.Dazhongdianping_liren_all_data.objects.filter(
                                shop_id=shop_id).delete()
                            print('成功')
                            resultdict['code'] = 0
                            resultdict['msg'] = ""
                            resultdict['state'] = 1
                            return JsonResponse(resultdict, safe=False)
        else:
            if len(shop_count) >= difference_len:
                print('用户下的商户数量', len(shop_count))
                resultdict['code'] = 0
                resultdict['msg'] = ""
                resultdict['state'] = 3
                return JsonResponse(resultdict, safe=False)
            else:
                if str(data) != '<QuerySet []>':
                    resultdict['code'] = 0
                    resultdict['msg'] = ""
                    resultdict['state'] = 2
                    return JsonResponse(resultdict, safe=False)
                else:
                    if shop_add_form == 'null':
                        pull_data = models.Dazhongdianping_liren_user_data.objects.create(
                            username=username,
                            shop_id=shop_id,
                            shop_name=shop_name,
                            shop_start=shop_start,
                            shop_review_count=shop_review_count,
                            shop_bad_review=shop_bad_review,
                            shop_per_capita_consumption=shop_per_capita_consumption,
                            shop_effect=shop_effect,
                            shop_surroundings=shop_surroundings,
                            shop_service=shop_service,
                            shop_region=shop_region,
                            shop_business_district=shop_business_district,
                            shop_category=shop_category,
                            shop_address=shop_address,
                            shop_telephonenumber=shop_telephonenumber,
                            shop_edit=shop_edit,
                            shop_tags=shop_tags,
                            shop_kp_name=shop_kp_name,
                            shop_kp_wechat_id=shop_kp_wechat_id,
                            shop_kp_city=shop_kp_city,
                            shop_kp_category=shop_kp_category,
                            shop_kp_position=shop_kp_position,
                            shop_city=shop_city,
                            pull_date=pull_date)
                        if pull_data != None:
                            models.Dazhongdianping_liren_all_data.objects.filter(
                                shop_id=shop_id).delete()
                            print('成功')
                            resultdict['code'] = 0
                            resultdict['msg'] = ""
                            resultdict['state'] = 1
                            return JsonResponse(resultdict, safe=False)
                    else:
                        pull_data = models.Dazhongdianping_liren_user_data.objects.create(
                            username=username,
                            shop_id=shop_id,
                            shop_name=shop_name,
                            shop_start=shop_start,
                            shop_review_count=shop_review_count,
                            shop_bad_review=shop_bad_review,
                            shop_per_capita_consumption=shop_per_capita_consumption,
                            shop_effect=shop_effect,
                            shop_surroundings=shop_surroundings,
                            shop_service=shop_service,
                            shop_region=shop_region,
                            shop_business_district=shop_business_district,
                            shop_category=shop_category,
                            shop_address=shop_address,
                            shop_telephonenumber=shop_telephonenumber,
                            shop_edit=shop_edit,
                            shop_tags=shop_tags,
                            shop_kp_name=shop_kp_name,
                            shop_kp_wechat_id=shop_kp_wechat_id,
                            shop_kp_city=shop_kp_city,
                            shop_kp_category=shop_kp_category,
                            shop_kp_position=shop_kp_position,
                            shop_add_form=eval(shop_add_form),
                            shop_city=shop_city,
                            pull_date=pull_date)
                        if pull_data != None:
                            models.Dazhongdianping_liren_all_data.objects.filter(
                                shop_id=shop_id).delete()
                            print('成功')
                            resultdict['code'] = 0
                            resultdict['msg'] = ""
                            resultdict['state'] = 1
                            return JsonResponse(resultdict, safe=False)


def pull_back(request):
    username = request.GET.get('username')
    shop_id = request.GET.get('shop_id')
    shop_name = request.GET.get('shop_name')
    shop_start = request.GET.get('shop_start')
    shop_review_count = request.GET.get('shop_review_count')
    shop_per_capita_consumption = request.GET.get(
        'shop_per_capita_consumption')
    shop_effect = request.GET.get('shop_effect')
    shop_surroundings = request.GET.get('shop_surroundings')
    shop_service = request.GET.get('shop_service')
    shop_region = request.GET.get('shop_region')
    shop_business_district = request.GET.get('shop_business_district')
    shop_category = request.GET.get('shop_category')
    shop_address = request.GET.get('shop_address')
    shop_telephonenumber = request.GET.get('shop_telephonenumber')
    shop_edit = request.GET.get('shop_edit')
    shop_tags = request.GET.get('shop_tags')
    shop_kp_name = request.GET.get('shop_kp_name')
    shop_kp_wechat_id = request.GET.get('shop_kp_wechat_id')
    shop_kp_city = request.GET.get('shop_kp_city')
    shop_kp_category = request.GET.get('shop_kp_category')
    shop_kp_position = request.GET.get('shop_kp_position')
    shop_add_form = request.GET.get('shop_add_form')
    print(shop_id)
    print(shop_add_form)
    try:
        if shop_add_form == 'null':
            shop_add_form = ''
        shop_city = request.GET.get('shop_city')
        print(shop_city)
        select_all_data = models.Dazhongdianping_liren_all_data.objects.filter(
            shop_id=shop_id)
        if str(select_all_data) != '<QuerySet []>':
            shop = models.Dazhongdianping_liren_all_data.objects.filter(
                shop_id=shop_id).update(
                shop_id=shop_id,
                shop_name=shop_name,
                shop_start=shop_start,
                shop_review_count=shop_review_count,
                shop_bad_review=0,
                shop_per_capita_consumption=shop_per_capita_consumption,
                shop_effect=shop_effect,
                shop_surroundings=shop_surroundings,
                shop_service=shop_service,
                shop_region=shop_region,
                shop_business_district=shop_business_district,
                shop_category=shop_category,
                shop_address=shop_address,
                shop_telephonenumber=shop_telephonenumber,
                shop_edit=shop_edit,
                shop_tags=shop_tags,
                shop_kp_name=shop_kp_name,
                shop_kp_wechat_id=shop_kp_wechat_id,
                shop_kp_city=shop_kp_city,
                shop_kp_category=shop_kp_category,
                shop_add_form=eval(shop_add_form),
                shop_city=shop_city,
                shop_kp_position=shop_kp_position)
            if shop != None:
                models.Dazhongdianping_liren_user_data.objects.filter(
                    shop_id=shop_id).delete()
                resultdict = {}
                resultdict['code'] = 0
                resultdict['msg'] = ""
                resultdict['state'] = 1
                return JsonResponse(resultdict, safe=False)
        else:
            shop = models.Dazhongdianping_liren_all_data.objects.create(
                shop_id=shop_id,
                shop_name=shop_name,
                shop_start=shop_start,
                shop_review_count=shop_review_count,
                shop_bad_review=0,
                shop_per_capita_consumption=shop_per_capita_consumption,
                shop_effect=shop_effect,
                shop_surroundings=shop_surroundings,
                shop_service=shop_service,
                shop_region=shop_region,
                shop_business_district=shop_business_district,
                shop_category=shop_category,
                shop_address=shop_address,
                shop_telephonenumber=shop_telephonenumber,
                shop_edit=shop_edit,
                shop_tags=shop_tags,
                shop_kp_name=shop_kp_name,
                shop_kp_wechat_id=shop_kp_wechat_id,
                shop_kp_city=shop_kp_city,
                shop_kp_category=shop_kp_category,
                shop_add_form=eval(shop_add_form),
                shop_city=shop_city,
                shop_kp_position=shop_kp_position)
            if shop != None:
                models.Dazhongdianping_liren_user_data.objects.filter(
                    shop_id=shop_id).delete()
                resultdict = {}
                resultdict['code'] = 0
                resultdict['msg'] = ""
                resultdict['state'] = 1
                return JsonResponse(resultdict, safe=False)
    except:
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 2
        return JsonResponse(resultdict, safe=False)


def login(request):
    if request.method == "GET":
        name = request.GET.get("username")
        pwd = request.GET.get("password")
        if username is not None and password is not None:
            islogin = models.User.objects.filter(name=name, pwd=pwd)
            if islogin:
                login(request, islogin)
                return JsonResponse({
                    "status": 0,
                    "message": "Login Success",
                    "username": name
                })
            else:
                return JsonResponse({
                    "status": 1,
                    "message": "登录失败, 请检查用户名或者密码是否输入正确."
                })
        else:
            return JsonResponse({"status": 2, "message": "参数错误"})


def logout(request):
    ret = redirect(reverse('login'))
    # cookie写法
    # ret.delete_cookie('is_login')
    # ret.delete_cookie('user')
    # ret.delete_cookie('last_time')
    # session写法
    request.session.flush()
    return ret


def index(request):
    return render(request, 'index.html')


# 添加销售组

def create_group(request):
    group_name = request.GET.get('group_name')
    a = models.Group.objects.filter(group_name=group_name).count()
    if a == 0:
        models.Group.objects.create(group_name=group_name)
        resultdict = {}
        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)
    else:
        if a != 0:
            resultdict = {}
            resultdict['code'] = 0
            resultdict['msg'] = ""
            resultdict['state'] = 2
            return JsonResponse(resultdict, safe=False)


def get_group_data(request):
    a = models.Group.objects.all()
    group_data = []
    for i in a:
        dict = {}
        dict['id'] = i.group_name
        dict['label'] = i.group_name
        group_data.append(dict)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['data'] = group_data
    print(group_data)
    return JsonResponse(resultdict, safe=False)


def update_user_data_yes(request):
    first_name = request.GET.get('first_name')
    avatar = request.GET.get('avatar')
    group = request.GET.get('group')
    db = pymysql.connect("localhost", "root", "bakj123456", "rock")
    cursor = db.cursor()
    cursor.execute("UPDATE user_userprofile SET group_name='" + group +
                   "',avatar='" + avatar + "' where first_name='" + first_name + "'")
    db.commit()
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    cursor.close()
    # 关闭数据库连接
    db.close()
    return JsonResponse(resultdict, safe=False)


def get_xiaoshou_data(request):
    username = request.GET.get('username')
    db = pymysql.connect("localhost", "root", "bakj123456", "rock")
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM user_userprofile WHERE first_name='" + username + "'")
    data = cursor.fetchall()
    group = data[0][14]

    if username == '超级管理员':
        cursor2 = db.cursor()
        cursor2.execute("SELECT * FROM user_userprofile")
    else:
        cursor2 = db.cursor()
        cursor2.execute(
            "SELECT * FROM user_userprofile WHERE group_name='" + group + "'")
    data2 = cursor2.fetchall()
    name = []
    for row in data2:
        name.append({'value': row[5], 'label': row[5]})
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ""
    resultdict['data'] = name
    print(name)
    cursor.close()
    # 关闭数据库连接
    db.close()
    cursor2.close()
    return JsonResponse(resultdict, safe=False)


def get_performance_this_month(request):
    # 当前时间
    # try:
    now_data = request.GET.get('now_data')
    # 上个月的时间
    old_data = request.GET.get('old_data')
    year1 = datetime.datetime.strptime(eval(now_data)[1], "%Y-%m").year
    year2 = datetime.datetime.strptime(eval(now_data)[0], "%Y-%m").year
    month1 = datetime.datetime.strptime(eval(now_data)[1], "%Y-%m").month
    month2 = datetime.datetime.strptime(eval(now_data)[0], "%Y-%m").month
    num = (year1 - year2) * 12 + (month1 - month2)
    if num == 0:
        order_now_data = models.Order.objects.filter(date=eval(now_data)[0])
        order_old_data = models.Order.objects.filter(date=eval(old_data)[0])
    else:
        now_date_data = getMonthRangList(eval(now_data)[0], eval(now_data)[1])
        order_now_data = models.Order.objects.filter(date__in=now_date_data)
        # 相差的月份加1
        num += 1
        old_date = []
        a = datetime.datetime(int(eval(now_data)[0][0:4]), int(eval(now_data)[0][5:7]), 1)
        a = str(a - relativedelta(months=3))[0:7]
        b = datetime.datetime(int(eval(now_data)[1][0:4]), int(eval(now_data)[1][5:7]), 1)
        b = str(b - relativedelta(months=3))[0:7]
        old_date.append(a)
        old_date.append(b)
        old_date_data = getMonthRangList(old_date[0], old_date[1])
        print('old_date', old_date_data)
        order_old_data = models.Order.objects.filter(date__in=old_date_data)
    if order_old_data.count() == 0:
        now_money = 0
        old_money = 0
        for ond in order_now_data:
            now_money += int(ond.order_amount)
        float3 = '100%'
        resultdict = {}
        resultdict['code'] = 0
        resultdict['float'] = float3
        resultdict['now_money'] = now_money
        return JsonResponse(resultdict, safe=False)
    elif order_now_data.count() == 0:
        now_money = 0
        old_money = 0
        for ood in order_old_data:
            old_money += int(ood.order_amount)
        float3 = '-100%'
        resultdict = {}
        resultdict['code'] = 0
        resultdict['float'] = float3
        resultdict['now_money'] = now_money
        return JsonResponse(resultdict, safe=False)
    else:
        now_money = 0
        old_money = 0
        for ond in order_now_data:
            now_money += int(ond.order_amount)
        for ood in order_old_data:
            old_money += int(ood.order_amount)
        float2 = (now_money - old_money) / old_money * 100
        float2 = round(float2, 2)
        float3 = str(float2) + '%'
        resultdict = {}
        resultdict['code'] = 0
        resultdict['float'] = float3
        resultdict['now_money'] = now_money
        return JsonResponse(resultdict, safe=False)


seng_date_data = '152.32.135.62'


def send_data(request):
    problems = models.To_do.objects.all()
    problems2 = models.Order.objects.all()
    date = models.Setting_storage.objects.all()[0].date
    today = datetime.date.today()
    today = str(today)
    if date == today:
        pass
    else:
        d1 = datetime.datetime(int(today[0:4]), int(today[5:7]), int(today[8:10]))
        models.Setting_storage.objects.all().update(date=today)
        for p in problems:
            d2 = datetime.datetime(int(p.time[0:4]), int(p.time[5:7]), int(p.time[8:10]))
            interval = d2 - d1
            db = pymysql.connect("  localhost", "root", "bakj123456", "rock")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user_userprofile WHERE first_name ='" + p.username + "'")
            data = cursor.fetchall()
            print(p.username)
            if '-' in str(interval.days):
                pass
            else:
                if int(interval.days) < 15:
                    wx = WeChat()
                    if seng_date_data == '152.32.135.62':
                        print('不发')
                    else:
                        wx.send_data(
                            '任务待办通知\n'
                            '店名：' + p.shop_name + '\n'
                                                  '任务名：' + p.project + '\n'
                                                                       '剩余天数：' + str(interval.days) + '（天）' + '\n'
                                                                                                              '过期时间：' + str(
                                p.time), data[0][4])

        for p2 in problems2:
            d2 = datetime.datetime(int(p2.order_end_date[0:4]), int(p2.order_end_date[5:7]),
                                   int(p2.order_end_date[8:10]))
            interval = d2 - d1
            print('interval', interval.days)
            db = pymysql.connect("localhost", "root", "bakj123456", "rock")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user_userprofile WHERE first_name ='" + p2.order_contract_sales + "'")
            data = cursor.fetchall()
            if '-' in str(interval.days):
                pass
            else:
                if int(interval.days) < 15:
                    wx = WeChat()
                    if seng_date_data == '152.32.135.62':
                        print('不发')
                    else:
                        wx.send_data(
                            '订单即将到期通知\n'
                            '店名：' + p2.sign_contract_shop + '\n'
                                                            '签单日期：' + str(p2.order_date) + '\n'
                                                                                           '签约时长：' + str(
                                p2.shop_cooperation_duration) + '个月' + '\n'
                                                                       '到期时间：' + str(p2.order_end_date) + '\n'
                                                                                                          '剩余天数：' + str(
                                interval.days) + '（天）', data[0][4])


def get_top_one(request):
    # 当前时间
    now_data = request.GET.get('now_data')
    year1 = datetime.datetime.strptime(eval(now_data)[1], "%Y-%m").year
    year2 = datetime.datetime.strptime(eval(now_data)[0], "%Y-%m").year
    month1 = datetime.datetime.strptime(eval(now_data)[1], "%Y-%m").month
    month2 = datetime.datetime.strptime(eval(now_data)[0], "%Y-%m").month
    num = (year1 - year2) * 12 + (month1 - month2)
    if num == 0:
        order_now_data = models.Order.objects.filter(date=eval(now_data)[0])
    else:
        old_date_data = getMonthRangList(eval(now_data)[0], eval(now_data)[1])
        order_now_data = models.Order.objects.filter(date__in=old_date_data)
    name = []
    for ond in order_now_data:
        if ond.order_contract_sales in name:
            pass
        else:
            name.append(ond.order_contract_sales)
    name_list = []
    # 查找每个人的名字
    for n in name:
        name_dict = {}
        name_dict['name'] = n
        name_dict['money'] = 0
        name_list.append(name_dict)
    # 根据每个人的名字匹配订单金额相加得出总业绩
    for money_ond in order_now_data:
        for nl in range(0, len(name_list)):
            if money_ond.order_contract_sales in name_list[nl].values():
                money = name_list[nl]['money']
                money += int(money_ond.order_amount)
                name_list[nl]['money'] = money
    # 进行字典排序
    name_list = sorted(
        name_list, key=operator.itemgetter('money'), reverse=True)
    # TOP姓名
    try:
        top_name = name_list[0]['name']
        # TOP业绩
        top_money = name_list[0]['money']
    except:
        top_name = '无'
        # TOP业绩
        top_money = '无'
    resultdict = {}
    resultdict['code'] = 0
    resultdict['top_name'] = top_name
    resultdict['top_money'] = top_money
    return JsonResponse(resultdict, safe=False)


def get_number_orders(request):
    now_data = request.GET.get('now_data')
    year1 = datetime.datetime.strptime(eval(now_data)[1], "%Y-%m").year
    year2 = datetime.datetime.strptime(eval(now_data)[0], "%Y-%m").year
    month1 = datetime.datetime.strptime(eval(now_data)[1], "%Y-%m").month
    month2 = datetime.datetime.strptime(eval(now_data)[0], "%Y-%m").month
    num = (year1 - year2) * 12 + (month1 - month2)

    if num == 0:
        number_orders = models.Order.objects.filter(date=eval(now_data, tags='断约')[0]).count()
        xinqian_number_orders = models.Order.objects.filter(date=eval(now_data)[0], tags='新签').count()
        xuyue_number_orders = models.Order.objects.filter(date=eval(now_data)[0], tags='续约').count()
    else:
        now_data = getMonthRangList(eval(now_data)[0], eval(now_data)[1])
        number_orders = models.Order.objects.filter(date__in=now_data, tags='断约').count()
        xinqian_number_orders = models.Order.objects.filter(date__in=now_data, tags='新签').count()
        xuyue_number_orders = models.Order.objects.filter(date__in=now_data, tags='续约').count()
    resultdict = {}
    resultdict['code'] = 0
    resultdict['number_orders'] = number_orders
    resultdict['xinqian_number_orders'] = xinqian_number_orders
    resultdict['xuyue_number_orders'] = xuyue_number_orders
    return JsonResponse(resultdict, safe=False)


def get_top_group(request):
    now_data = request.GET.get('now_data')
    year1 = datetime.datetime.strptime(eval(str(now_data))[-1], "%Y-%m").year
    year2 = datetime.datetime.strptime(eval(str(now_data))[0], "%Y-%m").year
    month1 = datetime.datetime.strptime(eval(str(now_data))[-1], "%Y-%m").month
    month2 = datetime.datetime.strptime(eval(str(now_data))[0], "%Y-%m").month
    num = (year1 - year2) * 12 + (month1 - month2)
    db = pymysql.connect("localhost", "root", "bakj123456", "rock")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_userprofile WHERE first_name !='超级管理员'")
    data = cursor.fetchall()
    list1 = []
    for i in data:
        list1.append(i[14])
    group_list = list(set(list1))
    group = []
    for g in group_list:
        cursor2 = db.cursor()
        cursor2.execute(
            "SELECT * FROM user_userprofile WHERE group_name ='" + g + "'")
        data2 = cursor2.fetchall()
        money = 0
        for d2 in data2:
            if num == 0:
                order_now_data = models.Order.objects.filter(date=eval(str(now_data))[0], order_contract_sales=d2[5])
            else:
                now_data = getMonthRangList(eval(str(now_data))[0], eval(str(now_data))[-1])
                order_now_data = models.Order.objects.filter(date__in=eval(str(now_data)), order_contract_sales=d2[5])
            for o_n_d in order_now_data:
                money += int(o_n_d.order_amount)
        dict = {}
        dict['group_name'] = g
        dict['money'] = money
        group.append(dict)
    group = sorted(group, key=operator.itemgetter('money'), reverse=True)
    group_name = group[0]['group_name']
    # TOP业绩
    group_money = group[0]['money']
    resultdict = {}
    resultdict['code'] = 0
    resultdict['group_name'] = group_name
    resultdict['group_money'] = group_money
    return JsonResponse(resultdict, safe=False)


def get_performance_this_year(request):
    # 当前时间
    now_data_list = request.GET.get('now_data_list')
    money = []
    for n in eval(now_data_list):
        order_now_data = models.Order.objects.filter(date__contains=n)
        data = []
        for ond in order_now_data:
            data.append(int(ond.order_amount))
        money.append(sum(data))
    resultdict = {}
    resultdict['code'] = 0
    resultdict['data'] = money
    return JsonResponse(resultdict, safe=False)


def get_qiandan_this_year(request):
    # 当前时间
    now_data_list = request.GET.get('now_data_list')
    money = []
    for n in eval(now_data_list):
        order_now_data = models.Order.objects.filter(
            order_date__contains=n).count()
        money.append(order_now_data)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['data'] = money
    return JsonResponse(resultdict, safe=False)


def get_xiaoshou_this_year(request):
    now_data_list = request.GET.get('now_data_list')
    db = pymysql.connect("localhost", "root", "bakj123456", "rock")
    print(now_data_list)
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM user_userprofile where group_name != '所有组' and group_name != '运营组'")
    data = cursor.fetchall()
    name = []
    name_data = []
    for i in data:
        name.append(i[5])
    for n in name:
        money = 0
        order_now_data = models.Order.objects.filter(date__in=eval(now_data_list), order_contract_sales=n)
        for o_n_d in order_now_data:
            money += int(o_n_d.order_amount)
        dict = {}
        dict['name'] = n
        dict['value'] = money
        name_data.append(dict)
    name_data = sorted(
        name_data, key=operator.itemgetter('value'), reverse=True)
    data = []
    resultdict = {}
    resultdict['code'] = 0
    resultdict['money'] = name_data
    return JsonResponse(resultdict, safe=False)


def get_xiaoshou_group_this_year(request):
    now_data_list = request.GET.get('now_data_list')
    print('now_data_list', now_data_list)
    db = pymysql.connect("localhost", "root", "bakj123456", "rock")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_userprofile where first_name != '超级管理员'")
    data = cursor.fetchall()
    group_list = []
    for i in data:
        if i[14] == '所有组' or i[14] == '运营组' or i[14] == '测试组':
            pass
        else:
            group_list.append(i[14])
    group_list = list(set(group_list))
    group_name_list = []
    count = 0
    for gl in group_list:
        money = 0
        cursor2 = db.cursor()
        cursor2.execute(
            "SELECT * FROM user_userprofile where group_name = '" + gl + "'")
        group_name = cursor2.fetchall()
        for gn in group_name:
            order_now_data = models.Order.objects.filter(date__in=eval(now_data_list), order_contract_sales=gn[5])
            for o_n_d in order_now_data:
                money += int(o_n_d.order_amount)
        count += money
        group_name_list.append({'name': gl, 'value': money})
    resultdict = {}
    resultdict['code'] = 0
    resultdict['money'] = group_name_list
    resultdict['count'] = count
    return JsonResponse(resultdict, safe=False)


def select_new_date(request):
    """

    """
    now_data = request.GET.get('now_data')
    lalala = eval(now_data)[0]
    if eval(now_data)[0] == eval(now_data)[1]:
        a = []
        a.append(lalala)
        resultdict = {}
        resultdict['code'] = 0
        resultdict['data'] = a
        return JsonResponse(resultdict, safe=False)
    else:
        now_date_data = getMonthRangList(eval(now_data)[0], eval(now_data)[1])
        resultdict = {}
        resultdict['code'] = 0
        resultdict['data'] = now_date_data
        return JsonResponse(resultdict, safe=False)


def select_order(request):
    """
    首页的加载的订单
    """
    today = datetime.date.today()
    now_data = request.GET.get('now_data')
    text = request.GET.get('text')
    if text == '2':
        if eval(now_data)[0] == eval(now_data)[1]:
            new_data = models.Order.objects.filter(date=eval(now_data)[0]).order_by('-id')
        else:
            now_date_data = getMonthRangList(eval(now_data)[0], eval(now_data)[1])
            new_data = models.Order.objects.filter(date__in=now_date_data).order_by('-id')
    else:
        new_data = models.Order.objects.filter(date=now_data).order_by('-id')
    data = []
    for nd in new_data:
        dic = {}
        dic['order_date'] = nd.order_date, '(签约时间)'
        dic['order_contract_sales'] = nd.order_contract_sales
        dic['sign_contract_shop'] = nd.sign_contract_shop
        dic['shop_cooperation_duration'] = nd.shop_cooperation_duration, '个月'
        dic['order_amount'] = '￥', nd.order_amount
        dic['tags'] = nd.tags
        data.append(dic)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['data'] = data
    return JsonResponse(resultdict, safe=False)


def transfer_update_order(request):
    '''
    订单切换销售
    '''
    order_id = request.GET.get('order_id')
    username = request.GET.get('username')
    if username != '':
        models.Order.objects.filter(contract_id=order_id).update(order_contract_sales=username)
        models.To_do.objects.filter(order_id=order_id).update(username=username)
        models.Pending_review.objects.filter(order_id=order_id).update(username=username)
        models.Completed.objects.filter(order_id=order_id).update(username=username)
        resultdict = {}
        resultdict['code'] = 0
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)


def selelct_xiaoshou(request):
    '''
    查找销售
    '''
    username = request.GET.get('username')
    new_data = models.Pending_review.objects.all()
    data = []
    for nd in new_data:
        data.append(nd.username)
    data = list(set(data))
    xs_data = []
    for d in data:
        xs_data.append({'id': d, 'label': d})
    xs_data.append({'id': '全部', 'label': '全部'})
    resultdict = {}
    resultdict['code'] = 0
    resultdict['data'] = xs_data
    return JsonResponse(resultdict, safe=False)


@csrf_exempt
def update_img(request):
    '''
    上传图片
    '''
    if request.method == "POST":
        fileDict = request.FILES.items()
        pic = request.FILES['image']
        pic_name = pic.name  # 上传文件名   /home/beiaikeji_admin/rock
        save_path = os.path.join('/home/beiaikeji_admin/rock', 'media', pic_name)
        with open(save_path, 'wb') as f:
            for content in pic.chunks():
                f.write(content)
        return HttpResponse(pic_name)


@csrf_exempt
def append_table(request):
    '''
    便捷添加商户
    '''
    url = request.GET.get('url')
    shop_id = re.sub('[http://www.dianping.com/shop/]', '', url)
    a = models.Dazhongdianping_liren_all_data.objects.filter(shop_id=shop_id).count()
    b = models.Dazhongdianping_liren_user_data.objects.filter(shop_id=shop_id).count()
    if a != 0:
        resultdict = {}
        resultdict['code'] = 0
        resultdict['state'] = 2
        return JsonResponse(resultdict, safe=False)
    elif b != 0:
        resultdict = {}
        resultdict['code'] = 0
        resultdict['state'] = 3
        return JsonResponse(resultdict, safe=False)
    else:
        try:
            headers = {
                'Host': 'www.dianping.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': 'http://www.dianping.com/beijing/ch50/g157p2?cpt=k4atm81SxpNVkePb%2Cl2hLlItDL98sr3Ua%2CH583cnHlE1Hx0C8b%2CH55UH3V6bgFhZ7Yb',
                'Connection': 'keep-alive',
                # 'Cookie': 'cy=2; cityid=2; cye=beijing; fspop=test; cye=beijing; _lxsdk_cuid=174767578bdc8-0be99bd08a01e98-4c3f247a-144000-174767578bdc8; _lxsdk=174767578bdc8-0be99bd08a01e98-4c3f247a-144000-174767578bdc8; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1599715244; _hc.v=2e0e52b5-6fb9-02a7-6543-2c0a63376f5e.1599715245; s_ViewType=10; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1599718287; _lxsdk_s=17476ccff76-811-2f8-1ce%7C%7C5',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }
            # 获取点评商户页面数据
            html_data = requests.get(url, headers=headers)
            # 解析HTMl
            html_data = etree.HTML(html_data.text)
            # print(html_data)
            # 店铺名
            shop_name = html_data.xpath('//div[@id="basic-info"]/h1[@class="shop-name"]/text()')[0].strip()
            # 星级
            start = html_data.xpath('//div[@class="brief-info"]/span[1]/@class')[0]
            start = int(re.findall(r'\d+', start)[0]) / 10
            # 评论数
            try:
                pinglun_count = html_data.xpath('//div[@class="brief-info"]/span[2]/text()')[0]
                pinglun_count = int(re.findall(r'\d+', pinglun_count)[0])
                # 人均消费
                # 效果
                try:
                    renjun = html_data.xpath('//div[@class="brief-info"]/span[3]/text()')[0]
                    renjun = int(re.findall(r'\d+', renjun)[0])
                except:
                    renjun = 0
                xiaoguo = html_data.xpath('//div[@class="brief-info"]/span[4]/text()')[0]
                xiaoguo = int(re.findall(r'\d+', xiaoguo)[0])
                # 服务
                fuwu = html_data.xpath('//div[@class="brief-info"]/span[5]/text()')[0]
                fuwu = int(re.findall(r'\d+', fuwu)[0])
                # 环境
                huanjing = html_data.xpath('//div[@class="brief-info"]/span[6]/text()')[0]
                huanjing = int(re.findall(r'\d+', huanjing)[0])
            except:
                pinglun_count = 0
                try:
                    renjun = html_data.xpath('//div[@class="brief-info"]/span[2]/text()')[0]
                    renjun = int(re.findall(r'\d+', renjun)[0])
                except:
                    renjun = 0
                # 效果
                xiaoguo = html_data.xpath('//div[@class="brief-info"]/span[3]/text()')[0]
                xiaoguo = int(re.findall(r'\d+', xiaoguo)[0])
                # 服务
                fuwu = html_data.xpath('//div[@class="brief-info"]/span[4]/text()')[0]
                fuwu = int(re.findall(r'\d+', fuwu)[0])
                # 环境
                huanjing = html_data.xpath('//div[@class="brief-info"]/span[5]/text()')[0]
                huanjing = int(re.findall(r'\d+', huanjing)[0])
            # 地址
            try:
                address = html_data.xpath('//div[@id="basic-info"]/div[2]/span[2]/text()')[0].strip()
            except:
                address = ''
            # 电话
            try:
                phone = html_data.xpath('//div[@id="basic-info"]/p[1]/span[2]/text()')[0].strip()
            except:
                phone = '没有标注'
            # 城市
            city = html_data.xpath('//span[@class="J-current-city"]/text()')[0]
            beijing = ['西城区', '海淀区', '东城区', '石景山区', '朝阳区', '丰台区', '顺义区', '房山区', '大兴区', '昌平区', '通州区', '密云区', '怀柔区',
                       '平谷区', '门头沟区', '延庆区']
            tianjing = ['和平区', '南开区', '河西区', '河北区', '红桥区', '河东区', '西青区', '东丽区', '滨海新区', '津南区', '北辰区', '武清区', '静海区',
                        '蓟州区', '宝坻区', '宁河区']
            shanghai = ['静安区', '长宁区', '徐汇区', '杨浦区', '黄浦区', '虹口区', '普陀区', '闵行区', '宝山区', '浦东新区', '松江区', '嘉定区', '青浦区',
                        '金山区', '奉贤区', '崇明区']
            chengdu = ['都江堰市', '彭州市', '锦江区', '青羊区', '武侯区', '成华区', '金牛区', '龙泉驿区', '双流区', '郫都区', '新都区', '温江区', '崇州市',
                       '金堂县', '青白江区', '邛崃市', '简阳市', '大邑县', '新津县', '蒲江县']
            xian = ['碑林区', '高新区', '莲湖区', '新城区', '雁塔区', '未央区', '长安区', '灞桥区', '鄠邑区', '临潼区', '高陵区', '周至县', '蓝田县', '阎良区']
            guangzhou = ['越秀区', '荔湾区', '天河区', '海珠区', '黄埔区', '番禺区', '白云区', '增城区', '花都区', '从化区', '南沙区']
            shenzhen = ['福田区', '南山区', '罗湖区', '盐田区', '龙华区', '龙岗区', '宝安区', '坪山区', '光明区']
            hangzhou = ['上城区', '西湖区', '拱墅区', '滨江区', '下城区', '江干区', '萧山区', '余杭区', '富阳区', '临安', '建德市', '桐庐县', '淳安县']
            nanjing = ['秦淮区', '鼓楼区', '玄武区', '建邺区', '雨花台区', '栖霞区', '江宁区', '浦口区', '六合区', '溧水区', '高淳区']
            suzhou = ['姑苏区', '虎丘区', '工业园区', '吴中区', '相城区', '昆山', '常熟', '吴江', '张家港', '太仓', '甪直']
            wuhan = ['江汉区', '江岸区', '武昌区', '汉阳区', '硚口区', '青山区', '洪山区', '江夏区', '蔡甸区', '东西湖区', '黄陂区', '新洲区', '汉南区']
            chongqing = ['渝中区', '江北区', '南岸区', '渝北区', '沙坪坝区', '九龙坡区', '北碚区', '大渡口区', '巴南区', '万州区', '永川区', '合川区', '涪陵区',
                         '江津区', '长寿区', '开州区', '大足区', '南川区', '綦江区', '荣昌区', '云阳县', '璧山区', '奉节县', '铜梁区', '垫江县', '潼南区',
                         '巫山县', '丰都县', '黔江区', '巫溪县', '酉阳土家族苗族自治县', '梁平区', '忠县', '秀山土家族苗族自治县', '石柱土家族自治县', '彭水苗族土家族自治县',
                         '武隆区', '城口县']
            if city in beijing:
                city = '北京'
            elif city in tianjing:
                city = '天津'
            elif city in shanghai:
                city = '上海'
            elif city in chengdu:
                city = '成都'
            elif city in xian:
                city = '西安'
            elif city in guangzhou:
                city = '广州'
            elif city in shenzhen:
                city = '深圳'
            elif city in hangzhou:
                city = '杭州'
            elif city in nanjing:
                city = '南京'
            elif city in suzhou:
                city = '苏州'
            elif city in wuhan:
                city = '武汉'
            elif city in chongqing:
                city = '重庆'
            # 区域
            quyu = html_data.xpath('//div[@class="breadcrumb"]/a[2]/text()')[0].strip()
            # 商圈
            shangquan = html_data.xpath('//div[@class="breadcrumb"]/a[3]/text()')[0].strip()
            # 品类
            pinlei = html_data.xpath('//div[@class="breadcrumb"]/a[4]/text()')[0].strip()
            models.Dazhongdianping_liren_all_data.objects.create(
                shop_id=shop_id,
                shop_name=shop_name,
                shop_start=start,
                shop_review_count=pinglun_count,
                shop_per_capita_consumption=renjun,
                shop_effect=xiaoguo,
                shop_service=fuwu,
                shop_surroundings=huanjing,
                shop_address=address,
                shop_telephonenumber=phone,
                shop_business_district=quyu,
                shop_category=shangquan,
                shop_region=pinlei,
                shop_edit='无',
                shop_city=city + '市'
            )
            resultdict = {}
            resultdict['code'] = 0
            resultdict['state'] = 1
            return JsonResponse(resultdict, safe=False)
        except:
            resultdict = {}
            resultdict['code'] = 0
            resultdict['state'] = 4
            return JsonResponse(resultdict, safe=False)


@csrf_exempt
def update_order_ok(order_date_before, order_date_after, order_start_date_before,
                    order_start_date_after, shop_cooperation_duration_before,
                    shop_cooperation_duration_after, order_amount_before, order_amount_after, cost_fees_before,
                    cost_fees_after,
                    order_id, order_contract_sales, order_end_date, sign_contract_shop, tags):
    # 订单修改完成审核之后调用
    wx = WeChat()
    wx.send_data('进入', 'gaoxiaofan')
    wx.send_data('order_date_before', 'gaoxiaofan')
    wx.send_data('order_date_after', 'gaoxiaofan')
    wx.send_data('order_start_date_before', 'gaoxiaofan')
    wx.send_data('order_start_date_after', 'gaoxiaofan')
    wx.send_data('shop_cooperation_duration_before', 'gaoxiaofan')
    wx.send_data('shop_cooperation_duration_after', 'gaoxiaofan')
    wx.send_data('order_amount_before', 'gaoxiaofan')
    wx.send_data('order_amount_after', 'gaoxiaofan')
    wx.send_data('cost_fees_before', 'gaoxiaofan')
    wx.send_data('cost_fees_after', 'gaoxiaofan')
    if order_amount_before == order_amount_after and cost_fees_before == cost_fees_after and order_date_before == order_date_after and order_start_date_before == order_start_date_after and shop_cooperation_duration_before == shop_cooperation_duration_after:
        pass
    elif order_amount_before != order_amount_after:
        models.Order.objects.filter(contract_id=order_id).update(order_amount=order_amount_after, tags=tags)
    elif cost_fees_before != cost_fees_after:
        models.Order.objects.filter(contract_id=order_id).update(cost_fees=cost_fees_after, tags=tags)
    elif order_date_before != order_date_after:
        order_start_date_year = int(order_date_after[0:4])
        order_start_date_month = int(order_date_after[5:7])
        if '0' == order_date_after[5:6]:
            order_start_date_month = int(order_date_after[6:7])
        order_start_date_day = int(order_date_after[8:10])
        if '0' == order_date_after[8:9]:
            order_start_date_day = int(order_date_after[9:10])
        order_date = datetime.date(order_start_date_year,
                                   order_start_date_month,
                                   order_start_date_day)
        models.Order.objects.filter(contract_id=order_id).update(order_date=order_date + datetime.timedelta(days=1),
                                                                 tags=tags)
    elif order_start_date_before != order_start_date_after:
        problems = models.Setting_storage.objects.all()
        now_date = datetime.date.today()
        first = now_date.replace(day=1)
        last_month = str(now_date)
        performance = 0
        commission_point = 0
        performance_data = models.Order.objects.filter(
            order_contract_sales=order_contract_sales)
        for i in performance_data:
            if str(last_month)[0:7] == i.order_date[0:7]:
                performance += int(i.order_amount)
        commission_point_data = models.Setting_storage.objects.all()
        commission_point_json = ''
        for c in commission_point_data:
            commission_point_json = c.commission_form
        count = []
        for o in eval(commission_point_json):
            count.append(int(o['commission_performance']))
        for a in sorted(count):
            if performance >= a:
                for o in eval(commission_point_json):
                    if a == int(o['commission_performance']):
                        commission_point = int(
                            o['commission_commission_point'])
            else:
                performance = 0
        date_time = str(order_start_date_after)
        year = int(date_time[0:4])
        month = int(date_time[5:7])
        if '0' == date_time[5:6]:
            month = int(str(date_time[6:7]))
        day = int(date_time[8:10])
        if '0' == date_time[8:9]:
            day = int(date_time[9:10])
        js = 0
        date = datetime.date(year, month, day)
        data = ''
        for i in problems:
            data = i.todo_form
        total_number_of_tasks = 0  # 任务总数
        # 计算任务总数
        for at in range(0, len(eval(data))):
            if eval(data)[at]['select'] == '单次任务':
                total_number_of_tasks = total_number_of_tasks + 1
            elif eval(data)[at]['select'] == '重复任务':
                frequency = eval(data)[at]['time']  # 获取重复任务的频率
                start_date = order_start_date_after
                end_date = order_end_date
                # 开始的时间
                date_time = str(order_start_date_after)
                year = int(date_time[0:4])
                month = int(date_time[5:7])
                if '0' == str(date_time[5:6]):
                    month = int(str(date_time[6:7]))
                day = int(date_time[8:10])
                if '0' == str(date_time[8:9]):
                    day = int(str(date_time[9:10]))
                cur_day = datetime.date(
                    int(year), int(month), int(day))
                # 结束的时间
                date_time_end = order_end_date
                year_end = int(date_time_end[0:4])
                month_end = int(date_time_end[5:7])
                if '0' == str(date_time_end[5:6]):
                    month_end = int(str(date_time_end[6:7]))
                day_end = int(date_time_end[8:10])
                if '0' == str(date_time_end[8:9]):
                    day_end = int(str(date_time_end[9:10]))
                # 订单开始的时间
                cur_day = datetime.date(
                    int(year), int(month), int(day))
                # 订单结束的时间
                next_day = datetime.date(int(year_end), int(month_end),
                                         int(day_end))
                # 　两个日期之间的差值
                difference = int((next_day - cur_day).days)
                count = int(difference) / int(frequency)
                count = round(count)
                total_number_of_tasks = total_number_of_tasks + count
        money = int(order_amount_after) * \
                (int(commission_point) / 100) * (1 / 3)
        money = money * 2
        print('提成点', money)
        print('任务总数', total_number_of_tasks)
        data = ''
        for i in problems:
            data = i.todo_form
        # 删除任务，重新分配
        models.To_do.objects.filter(order_id=order_id).delete()
        models.Completed.objects.filter(order_id=order_id).delete()
        models.Pending_review.objects.filter(order_id=order_id).delete()
        # 重新分配任务
        for a in range(0, len(eval(data))):
            if eval(data)[a]['select'] == '单次任务':
                models.To_do.objects.create(
                    project=eval(data)[a]['name'],
                    shop_name=sign_contract_shop,
                    order_id=contract_id,
                    # 开始日期加上任务的时间
                    time=date + \
                         datetime.timedelta(
                             days=int(eval(data)[a]['time'])),
                    money=round(money / total_number_of_tasks),
                    schedule=0,
                    username=order_contract_sales,
                    status='未审核')
            elif eval(data)[a]['select'] == '重复任务':

                # 重复频率
                frequency = eval(data)[a]['time']  # 获取重复任务的频率
                start_date = order_start_date_after
                end_date = order_end_date
                # 开始的时间
                date_time = str(order_start_date_after)
                year = int(date_time[0:4])
                month = int(date_time[5:7])
                if '0' == str(date_time[5:6]):
                    month = int(str(date_time[6:7]))
                day = int(date_time[8:10])
                if '0' == str(date_time[8:9]):
                    day = int(str(date_time[9:10]))
                cur_day = datetime.date(year, month, day)
                # 结束的时间
                date_time_end = order_end_date
                year_end = int(date_time_end[0:4])
                month_end = int(date_time_end[5:7])
                if '0' == str(date_time_end[5:6]):
                    month_end = int(str(date_time_end[6:7]))
                day_end = int(date_time_end[8:10])
                if '0' == str(date_time_end[8:9]):
                    day_end = int(str(date_time_end[9:10]))
                # 订单开始的时间
                cur_day = datetime.date(year, month, day)
                # 订单结束的时间
                print('day_end', day_end)
                next_day = datetime.date(
                    int(year_end), int(month_end), int(day_end))
                # 　两个日期之间的差值
                difference = int((next_day - cur_day).days)
                count = int(difference) / int(frequency)
                count = round(count)
                original_time = cur_day
                for b in range(0, count):
                    print('创建')
                    models.To_do.objects.create(
                        project='第' + str(b + 1) + '次' +
                                eval(data)[a]['name'],
                        shop_name=sign_contract_shop,
                        order_id=order_id,
                        time=original_time + datetime.timedelta(days=int(
                            eval(data)[a]['time'])),  # 开始日期加上任务的时间
                        money=round(money / total_number_of_tasks),
                        schedule=0,
                        username=order_contract_sales,
                        status='未审核')
                    original_time = original_time + \
                                    datetime.timedelta(
                                        days=int(eval(data)[a]['time']))
        order_start_date_year = int(order_start_date_after[0:4])
        order_start_date_month = int(order_start_date_after[5:7])
        if '0' == order_start_date_after[5:6]:
            order_start_date_month = int(order_start_date_after[6:7])
        order_start_date_day = int(order_start_date_after[8:10])
        if '0' == order_start_date_after[8:9]:
            order_start_date_day = int(order_start_date_after[9:10])
        order_start_date = datetime.date(order_start_date_year,
                                         order_start_date_month,
                                         order_start_date_day)
        models.Order.objects.filter(contract_id=order_id).update(
            order_start_date=order_start_date + datetime.timedelta(days=1), order_end_date=order_end_date, tags=tags)
    elif shop_cooperation_duration_before != shop_cooperation_duration_after:
        problems = models.Setting_storage.objects.all()
        now_date = datetime.date.today()
        first = now_date.replace(day=1)
        last_month = str(now_date)
        performance = 0
        commission_point = 0
        performance_data = models.Order.objects.filter(
            order_contract_sales=order_contract_sales)
        for i in performance_data:
            if str(last_month)[0:7] == i.order_date[0:7]:
                performance += int(i.order_amount)
        commission_point_data = models.Setting_storage.objects.all()
        commission_point_json = ''
        for c in commission_point_data:
            commission_point_json = c.commission_form
        count = []
        for o in eval(commission_point_json):
            count.append(int(o['commission_performance']))
        for a in sorted(count):
            if performance >= a:
                for o in eval(commission_point_json):
                    if a == int(o['commission_performance']):
                        commission_point = int(
                            o['commission_commission_point'])
            else:
                performance = 0
        date_time = str(order_start_date_after)
        year = int(date_time[0:4])
        month = int(date_time[5:7])
        if '0' == date_time[5:6]:
            month = int(str(date_time[6:7]))
        day = int(date_time[8:10])
        if '0' == date_time[8:9]:
            day = int(date_time[9:10])
        js = 0
        date = datetime.date(year, month, day)
        data = ''
        for i in problems:
            data = i.todo_form
        total_number_of_tasks = 0  # 任务总数
        # 计算任务总数
        for at in range(0, len(eval(data))):
            if eval(data)[at]['select'] == '单次任务':
                total_number_of_tasks = total_number_of_tasks + 1
            elif eval(data)[at]['select'] == '重复任务':
                frequency = eval(data)[at]['time']  # 获取重复任务的频率
                start_date = order_start_date_after
                end_date = order_end_date
                # 开始的时间
                date_time = str(order_start_date_after)
                year = int(date_time[0:4])
                month = int(date_time[5:7])
                if '0' == str(date_time[5:6]):
                    month = int(str(date_time[6:7]))
                day = int(date_time[8:10])
                if '0' == str(date_time[8:9]):
                    day = int(str(date_time[9:10]))
                cur_day = datetime.date(
                    int(year), int(month), int(day))
                # 结束的时间
                date_time_end = order_end_date
                year_end = int(date_time_end[0:4])
                month_end = int(date_time_end[5:7])
                if '0' == str(date_time_end[5:6]):
                    month_end = int(str(date_time_end[6:7]))
                day_end = int(date_time_end[8:10])
                if '0' == str(date_time_end[8:9]):
                    day_end = int(str(date_time_end[9:10]))
                # 订单开始的时间
                cur_day = datetime.date(
                    int(year), int(month), int(day))
                # 订单结束的时间
                next_day = datetime.date(int(year_end), int(month_end),
                                         int(day_end))
                # 　两个日期之间的差值
                difference = int((next_day - cur_day).days)
                count = int(difference) / int(frequency)
                count = round(count)
                total_number_of_tasks = total_number_of_tasks + count
        money = int(order_amount_after) * \
                (int(commission_point) / 100) * (1 / 3)
        money = money * 2
        print('提成点', money)
        print('任务总数', total_number_of_tasks)
        data = ''
        # 获得任务
        for i in problems:
            data = i.todo_form
        # 分配任务以及金额
        models.To_do.objects.filter(order_id=order_id).delete()
        models.Completed.objects.filter(order_id=order_id).delete()
        models.Pending_review.objects.filter(order_id=order_id).delete()
        for a in range(0, len(eval(data))):
            if eval(data)[a]['select'] == '单次任务':
                models.To_do.objects.create(
                    project=eval(data)[a]['name'],
                    shop_name=sign_contract_shop,
                    order_id=contract_id,
                    # 开始日期加上任务的时间
                    time=date + \
                         datetime.timedelta(
                             days=int(eval(data)[a]['time'])),
                    money=round(money / total_number_of_tasks),
                    schedule=0,
                    username=order_contract_sales,
                    status='未审核')
            elif eval(data)[a]['select'] == '重复任务':
                # 重复频率
                frequency = eval(data)[a]['time']  # 获取重复任务的频率
                start_date = order_start_date_after
                end_date = order_end_date
                # 开始的时间
                date_time = str(order_start_date_after)
                year = int(date_time[0:4])
                month = int(date_time[5:7])
                if '0' == str(date_time[5:6]):
                    month = int(str(date_time[6:7]))
                day = int(date_time[8:10])
                if '0' == str(date_time[8:9]):
                    day = int(str(date_time[9:10]))
                cur_day = datetime.date(year, month, day)
                # 结束的时间
                date_time_end = order_end_date
                year_end = int(date_time_end[0:4])
                month_end = int(date_time_end[5:7])
                if '0' == str(date_time_end[5:6]):
                    month_end = int(str(date_time_end[6:7]))
                day_end = int(date_time_end[8:10])
                if '0' == str(date_time_end[8:9]):
                    day_end = int(str(date_time_end[9:10]))
                # 订单开始的时间
                cur_day = datetime.date(year, month, day)
                # 订单结束的时间
                print('day_end', day_end)
                next_day = datetime.date(
                    int(year_end), int(month_end), int(day_end))
                # 　两个日期之间的差值
                difference = int((next_day - cur_day).days)
                count = int(difference) / int(frequency)
                count = round(count)
                original_time = cur_day
                for b in range(0, count):
                    models.To_do.objects.create(
                        project='第' + str(b + 1) + '次' +
                                eval(data)[a]['name'],
                        shop_name=sign_contract_shop,
                        order_id=order_id,
                        time=original_time + datetime.timedelta(days=int(
                            eval(data)[a]['time'])),  # 开始日期加上任务的时间
                        money=round(money / total_number_of_tasks),
                        schedule=0,
                        username=order_contract_sales,
                        status='未审核')
                    original_time = original_time + \
                                    datetime.timedelta(
                                        days=int(eval(data)[a]['time']))
        order_start_date_year = int(order_start_date_after[0:4])

        order_start_date_month = int(order_start_date_after[5:7])

        if '0' == order_start_date_after[5:6]:
            order_start_date_month = int(order_start_date_after[6:7])
        order_start_date_day = int(order_start_date_after[8:10])

        if '0' == order_start_date_after[8:9]:
            order_start_date_day = int(order_start_date_after[9:10])
        # 更新时间
        order_start_date = datetime.date(order_start_date_year, order_start_date_month, order_start_date_day)
        # 更新订单
        models.Order.objects.filter(contract_id=order_id).update(
            shop_cooperation_duration=shop_cooperation_duration_after, order_end_date=order_end_date, tags=tags)


def create_tuikuan_order(request):
    '''
    创建退款订单，需要获取前后变化的值，然后进行判断
    '''
    order_date_before = request.GET.get('order_date_before')
    order_date_after = request.GET.get('order_date_after')
    order_start_date_before = request.GET.get('order_start_date_before')
    order_start_date_after = request.GET.get('order_start_date_after')
    shop_cooperation_duration_before = request.GET.get('shop_cooperation_duration_before')
    shop_cooperation_duration_after = request.GET.get('shop_cooperation_duration_after')
    order_amount_before = request.GET.get('order_amount_before')
    order_amount_after = request.GET.get('order_amount_after')
    cost_fees_before = request.GET.get('cost_fees_before')
    cost_fees_after = request.GET.get('cost_fees_after')
    order_id = request.GET.get('order_id')
    order_contract_sales = request.GET.get('order_contract_sales')
    order_end_date = request.GET.get('order_end_date')
    sign_contract_shop = request.GET.get('sign_contract_shop')
    tags = request.GET.get('tags')
    username = request.GET.get('username')
    shop_name = request.GET.get('shop_name')
    cunzai = models.Tuikuan_Order.objects.filter(order_id=order_id).count()
    if cunzai == 0:
        # 创建退单
        models.Tuikuan_Order.objects.create(
            order_date_before=order_date_before,
            order_date_after=order_date_after,
            order_start_date_before=order_start_date_before,
            order_start_date_after=order_start_date_after,
            shop_cooperation_duration_before=shop_cooperation_duration_before,
            shop_cooperation_duration_after=shop_cooperation_duration_after,
            order_amount_before=order_amount_before,
            order_amount_after=order_amount_after,
            cost_fees_before=cost_fees_before,
            cost_fees_after=cost_fees_after,
            order_id=order_id,
            order_contract_sales=order_contract_sales,
            order_end_date=order_end_date,
            sign_contract_shop=sign_contract_shop,
            tags=tags
        )
        a = models.Order.objects.filter(contract_id=order_id)
        id = ''
        for p in a:
            id = p.id
        # 查找组名和组长
        db = pymysql.connect("localhost", "root", "bakj123456", "rock")
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM user_userprofile where first_name = '" + username + "'")
        data = cursor.fetchall()
        username_yinwen = data[0][4]
        group_name = data[0][14]
        cursor2 = db.cursor()
        cursor2.execute(
            "SELECT * FROM user_userprofile where group_name = '" + group_name + "'")
        data = cursor2.fetchall()
        admin_username = ''
        for a in data:
            if a[11] == 'admin':
                admin_username = a[4]
        # 判断是否是组长
        if admin_username == 'admin' or admin_username == '超级管理员':
            admin_username = 'pengyan'
            wx = Wx_Shenpi()
            wx.send_data_tuikuan(order_date_before, order_date_after, order_start_date_before, order_start_date_after,
                                 shop_cooperation_duration_before, shop_cooperation_duration_after, order_amount_before,
                                 order_amount_after, cost_fees_before, cost_fees_after, id, order_contract_sales,
                                 order_end_date, sign_contract_shop, tags, username, shop_name, order_id,
                                 admin_username)
        else:
            admin_username = 'pengyan'
            wx = Wx_Shenpi()
            wx.send_data_tuikuan(order_date_before, order_date_after, order_start_date_before, order_start_date_after,
                                 shop_cooperation_duration_before, shop_cooperation_duration_after, order_amount_before,
                                 order_amount_after, cost_fees_before, cost_fees_after, id, order_contract_sales,
                                 order_end_date, sign_contract_shop, tags, username, shop_name, order_id,
                                 admin_username)
        resultdict = {}
        resultdict['code'] = 0
        resultdict['state'] = 2
        return JsonResponse(resultdict, safe=False)
    else:
        resultdict = {}
        resultdict['code'] = 0
        resultdict['state'] = 1
        return JsonResponse(resultdict, safe=False)

def get_xiaoshou_jj(request):
    db = pymysql.connect("localhost", "root", "bakj123456", "rock")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_userprofile")
    data = cursor.fetchall()
    user = []
    for d in data:
        user.append({'label':d[5],'value':d[5]})
    resultdict = {}
    resultdict['code'] = 0
    resultdict['data'] = list(user)
    return JsonResponse(resultdict, safe=False)

def get_money_jj(request):
    username = request.GET.get('username')
    month = request.GET.get('month_data')
    page = request.GET.get('currentPage')
    rows = request.GET.get('pagesize')
    # 判断是否为空
    if username == '' and month != '':
        data = models.To_do.objects.filter(time__contains=month)
    elif username != '' and month == '':
        data = models.To_do.objects.filter(username=username)
    elif username != '' and month != '':
        data = models.To_do.objects.filter(username=username,time__contains=month)
    elif username == '' and month == '':
        data = models.To_do.objects.all()
    dict = []
    money = 0
    # 计算总金额
    for d in data:
        money += int(float(d.money))
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    total = data.count()
    data = data[i:j]
    for d in data:
        dic = {}
        dic['shop_name'] = d.shop_name
        dic['project'] = d.project
        dic['time'] = d.time
        dic['money'] = d.money
        dic['username'] = d.username
        dict.append(dic)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['data'] = dict
    resultdict['total'] = total
    resultdict['money'] = money
    return JsonResponse(resultdict, safe=False)
