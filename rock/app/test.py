# coding:utf-8
# # import hashlib
# import datetime
# import datetime
# from dateutil.relativedelta import relativedelta
# # def sign(param, appsecret, signmethod):
# from dateutil import rrule
# #     if signmethod !="MD5":
# #         return ''

# #     lists = []
# #     param_str = appsecret
# #     for item in param:
# #         lists.append(item)

# #     lists.sort()

# #     for key in lists:
# #         param_str = param_str + key + param[key]

# #     param_str += appsecret
# #     param_str = param_str.strip()

# #     return genMd5(param_str)


# # def genMd5(str):
# #     md5 = hashlib.md5()
# #     md5.update(str)
# #     md5.hexdigest()

# #     return md5.hexdigest()

# #params = {"sing": "1", "method": "2", "id": "1231", "key": "apdfa", "sort": "serr"}
# def getMonthRangList(start_month, end_month):
#         """
#         从开始日期到结束日期查询存在的月份列表，除去本月的数据
#         :param start_month:
#         :param end_month:
#         :return:
#         """
#         start_time = datetime.datetime.strptime(start_month, "%Y-%m")
#         end_time = datetime.datetime.strptime(end_month, "%Y-%m")
#         month_count = rrule.rrule(rrule.MONTHLY, dtstart=start_time, until=end_time).count()
#         now_month = datetime.datetime.strptime(str(datetime.datetime.now())[:7], "%Y-%m")
#         if start_time == now_month == end_time:
#             return []
#         else:
#             month_list = []
#             for x in range(month_count):
#                 year, month = [int(y) for y in str(start_time)[:7].split("-")]
#                 month = month + x
#                 if month > 12:
#                     year += 1
#                     month -= 12
#                 elif month < 1:
#                     year -= 1
#                     month += 12
#                 year, month = str(year), str(month)
#                 if len(month) == 1:
#                     month = "0" + month
#                 month_list.append(year + "-" + month)
#             # if str(now_month)[:7] in month_list:
#             #     month_list.remove(str(now_month)[:7])
#             return month_list
# #print (sign(params, 'SECRET', 'MD5'))
# # a = datetime.datetime(2020,5,1)
# # a = str(a - relativedelta(months=3))[0:7]
# # print(a)
# a = getMonthRangList('2020-01','2020-10')
# print(a)
# # today = datetime.date.today()
# # first = today.replace(day=1)
# # last_month = first - datetime.timedelta(days=1)
# # print(last_month.strftime("%Y-%m"))

# return r.text['media_id']
# import time
# import requests
# import json
# class Wx_Shenpi:
#     def __init__(self):
#         self.CORPID = 'wwaa5e1adc141fc4e4'  # 企业ID，在管理后台获取
#         # 自建应用的Secret，每个自建应用里都有单独的secret
#         self.CORPSECRET = 'bUGrb2L48lJ-41COkWg9HKLVM0jNFvWEb1VnLiMBz5w'
#         self.AGENTID = '1000040'  # 应用ID，在后台应用中获取

#     def _get_access_token(self):
#         url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
#         values = {'corpid': self.CORPID,
#                   'corpsecret': self.CORPSECRET,
#                   }
#         req = requests.post(url, params=values)
#         data = json.loads(req.text)
#         return data["access_token"]

#     def get_access_token(self):
#         try:
#             with open('./access_token.conf', 'r') as f:
#                 t, access_token = f.read().split()
#         except:
#             with open('./access_token.conf', 'w') as f:
#                 access_token = self._get_access_token()
#                 cur_time = time.time()
#                 f.write('\t'.join([str(cur_time), access_token]))
#                 return access_token
#         else:
#             cur_time = time.time()
#             if 0 < cur_time - float(t) < 7260:
#                 return access_token
#             else:
#                 with open('./access_token.conf', 'w') as f:
#                     access_token = self._get_access_token()
#                     f.write('\t'.join([str(cur_time), access_token]))
#                     return access_token
#     def get_img(self):
#         send_url = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=' + self.get_access_token()+'&type=file'
#         data = {'meida':open(r'D:\PythonProject\beiaikeji_admin\rock\media\8.jpg','rb')}
#         r = requests.post(url=send_url,files=data)
#         print(r.text)
#         dict_data = r.json()
#         return dict_data

# get_img = Wx_Shenpi()
# a = get_img.get_img()
# print(a['media_id'])
# import requests
# from lxml import etree
# import re

# # 链接
# url = 'https://www.dianping.com/shop/k6970OZYi7cH4DzH'
# headers = {
#     'Host': 'www.dianping.com',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#     'Accept-Encoding': 'gzip, deflate',
#     'Referer': 'http://www.dianping.com/beijing/ch50/g157p2?cpt=k4atm81SxpNVkePb%2Cl2hLlItDL98sr3Ua%2CH583cnHlE1Hx0C8b%2CH55UH3V6bgFhZ7Yb',
#     'Connection': 'keep-alive',
#     # 'Cookie': 'cy=2; cityid=2; cye=beijing; fspop=test; cye=beijing; _lxsdk_cuid=174767578bdc8-0be99bd08a01e98-4c3f247a-144000-174767578bdc8; _lxsdk=174767578bdc8-0be99bd08a01e98-4c3f247a-144000-174767578bdc8; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1599715244; _hc.v=2e0e52b5-6fb9-02a7-6543-2c0a63376f5e.1599715245; s_ViewType=10; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1599718287; _lxsdk_s=17476ccff76-811-2f8-1ce%7C%7C5',
#     'Upgrade-Insecure-Requests': '1',
#     'Cache-Control': 'max-age=0'
# }
# 获取点评商户页面数据
# html_data = requests.get(url,headers=headers)
# # 解析HTMl
# html_data = etree.HTML(html_data.text)
# # print(html_data)
# # 店铺名
# shop_name = html_data.xpath('//div[@id="basic-info"]/h1[@class="shop-name"]/text()')[0].strip()
# # 星级
# start = html_data.xpath('//div[@class="brief-info"]/span[1]/@class')[0]
# start = int(re.findall(r'\d+',start)[0]) / 10
# # 评论数
# try:
#     pinglun_count = html_data.xpath('//div[@class="brief-info"]/span[2]/text()')[0]
#     pinglun_count = int(re.findall(r'\d+',pinglun_count)[0])
#     # 人均消费
#     try:
#         renjun = html_data.xpath('//div[@class="brief-info"]/span[3]/text()')[0]
#         renjun = int(re.findall(r'\d+',renjun)[0])
#     except:
#         renjun = 0
#     # 效果
#     xiaoguo = html_data.xpath('//div[@class="brief-info"]/span[4]/text()')[0]
#     xiaoguo = int(re.findall(r'\d+',xiaoguo)[0])
#     # 服务
#     fuwu = html_data.xpath('//div[@class="brief-info"]/span[5]/text()')[0]
#     fuwu = int(re.findall(r'\d+',fuwu)[0])
#     # 环境
#     huanjing = html_data.xpath('//div[@class="brief-info"]/span[6]/text()')[0]
#     huanjing = int(re.findall(r'\d+',huanjing)[0])
# except:
#     pinglun_count = 0
#     try:
#         renjun = html_data.xpath('//div[@class="brief-info"]/span[2]/text()')[0]
#         renjun = int(re.findall(r'\d+',renjun)[0])
#     except:
#         renjun = 0
#     # 效果
#     xiaoguo = html_data.xpath('//div[@class="brief-info"]/span[3]/text()')[0]
#     xiaoguo = int(re.findall(r'\d+',xiaoguo)[0])
#     # 服务
#     fuwu = html_data.xpath('//div[@class="brief-info"]/span[4]/text()')[0]
#     fuwu = int(re.findall(r'\d+',fuwu)[0])
#     # 环境
#     huanjing = html_data.xpath('//div[@class="brief-info"]/span[5]/text()')[0]
#     huanjing = int(re.findall(r'\d+',huanjing)[0])
# # 地址
# try:
#     address = html_data.xpath('//div[@id="basic-info"]/div[2]/span[2]/text()')[0].strip()
# except:
#     phone = '没有标注'
# # 电话
# try:
#     phone = html_data.xpath('//div[@id="basic-info"]/p[1]/span[2]/text()')[0].strip()
# except:
#     phone = ''
# # 城市
# city = html_data.xpath('//span[@class="J-current-city"]/text()')[0]
# beijing = ['西城区','海淀区','东城区','石景山区','朝阳区','丰台区','顺义区','房山区','大兴区','昌平区','通州区','密云区','怀柔区','平谷区','门头沟区','延庆区']
# tianjing = ['和平区','南开区','河西区','河北区','红桥区','河东区','西青区','东丽区','滨海新区','津南区','北辰区','武清区','静海区','蓟州区','宝坻区','宁河区']
# shanghai = [ '静安区','长宁区','徐汇区','杨浦区','黄浦区','虹口区','普陀区','闵行区','宝山区','浦东新区','松江区','嘉定区','青浦区','金山区','奉贤区','崇明区']
# chengdu = ['都江堰市','彭州市','锦江区','青羊区','武侯区','成华区','金牛区','龙泉驿区','双流区','郫都区','新都区','温江区','崇州市','金堂县','青白江区','邛崃市','简阳市','大邑县','新津县','蒲江县']
# xian = ['碑林区','高新区','莲湖区','新城区','雁塔区','未央区','长安区','灞桥区','鄠邑区','临潼区','高陵区','周至县','蓝田县','阎良区']
# guangzhou = ['越秀区','荔湾区','天河区','海珠区','黄埔区','番禺区','白云区','增城区','花都区','从化区','南沙区']
# shenzhen = ['福田区','南山区','罗湖区','盐田区','龙华区','龙岗区','宝安区','坪山区','光明区']
# hangzhou = [ '上城区','西湖区','拱墅区','滨江区','下城区','江干区','萧山区','余杭区','富阳区','临安','建德市','桐庐县','淳安县']
# nanjing = ['秦淮区','鼓楼区','玄武区','建邺区','雨花台区','栖霞区','江宁区','浦口区','六合区','溧水区','高淳区']
# suzhou = ['姑苏区','虎丘区','工业园区','吴中区','相城区','昆山','常熟','吴江','张家港','太仓','甪直']
# wuhan = ['江汉区','江岸区','武昌区','汉阳区','硚口区','青山区','洪山区','江夏区','蔡甸区','东西湖区','黄陂区','新洲区','汉南区']
# chongqing = ['渝中区','江北区','南岸区','渝北区','沙坪坝区','九龙坡区','北碚区','大渡口区','巴南区','万州区','永川区','合川区','涪陵区','江津区','长寿区','开州区','大足区','南川区','綦江区','荣昌区','云阳县','璧山区','奉节县','铜梁区','垫江县','潼南区','巫山县','丰都县','黔江区','巫溪县','酉阳土家族苗族自治县','梁平区','忠县','秀山土家族苗族自治县','石柱土家族自治县','彭水苗族土家族自治县','武隆区','城口县']
# if city in beijing:
#     city = '北京'
# elif city in tianjing:
#     city = '天津'
# elif city in shanghai:
#     city = '上海'
# elif city in chengdu:
#     city = '成都'
# elif city in xian:
#     city = '西安'
# elif city in guangzhou:
#     city = '广州'
# elif city in shenzhen:
#     city = '深圳'
# elif city in hangzhou:
#     city = '杭州'
# elif city in nanjing:
#     city = '南京'
# elif city in suzhou:
#     city = '苏州'
# elif city in wuhan:
#     city = '武汉'
# elif city in chongqing:
#     city = '重庆'
# # 区域
# quyu = html_data.xpath('//div[@class="breadcrumb"]/a[2]/text()')[0].strip()
# # 商圈
# shangquan = html_data.xpath('//div[@class="breadcrumb"]/a[3]/text()')[0].strip()
# # 品类
# pinlei = html_data.xpath('//div[@class="breadcrumb"]/a[4]/text()')[0].strip()
# a = 9000 * 25 / 100 * 1 / 3 / 3
# print(a)
# import datetime
# order_date = '2020-09-18'
#
# order_date_year = int(order_date[0:4])
# order_date_month = int(order_date[5:7])
# if '0' == order_date[5:6]:
#     order_date_month = int(order_date[6:7])
# order_date_day = int(order_date[8:10])
# if '0' == order_date[8:9]:
#     order_date_day = int(order_date[9:10])
#
# a = datetime.date(order_date_year, order_date_month,order_date_day)
# print(datetime.date.today()-a)
import re
import pymysql

db_todo = pymysql.connect("localhost", "root", "bakj123456", "rock")
cursor_todo = db_todo.cursor()
order_data = '202009Djingbiao008'
str_todo = 'SELECT * FROM app_tuikuan_order where order_id = "' + str(order_data) +'"'
print(str_todo)
cursor_todo.execute(str_todo)
data_todo = cursor_todo.fetchall()
order_id = data_todo[0][1]
print(order_id)