import smtplib
from email.header import Header
from email.mime.text import MIMEText

from urllib import request
import re
import random
import sys
import os
from bs4 import BeautifulSoup


class Spider():
    #初始化
    def __init__(self):
        self.url = r'http://www.weather.com.cn/weather1d/101210101.shtml'

    def getPageCode(self):
        #构建UA
        user_agents=['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
                     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
                     'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533 + \(KHTML, like Gecko) Element Browser 5.0',
                     'IBM WebExplorer /v0.94',
                     'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
                     'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                     'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
                     'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \Version/6.0 Mobile/10A5355d Safari/8536.25',
                     'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \Chrome/28.0.1468.0 Safari/537.36',
                     'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
        # user_agent在一堆范围中随机获取
        # random.randint()获取随机数，防止网站认出是爬虫而访问受限
        index = random.randint(0,9)
        user_agent=user_agents[index]
        headers = {'User_agent': user_agent}
        #打开页面
        req = request.Request(self.url,headers=headers)
        req = request.urlopen(req)
        #print('HTTPMessage头信息：',req.info(),'\nHTTP状态码：',req.getcode(),'\n返回请求URL：',req.geturl())
        page = req.read()
        page = page.decode('utf-8')
        return page
        
class MailPostfix():
    # 第三方 SMTP 服务
    def __init__(self):
        self.mail_host = "smtp.163.com"      # SMTP服务器
        self.mail_user = "908422490"                  # 用户名
        self.mail_pass = "jinlingjie"               # 授权密码，非登录密码
        self.sender = '908422490@163.com'    # 发件人邮箱(最好写全, 不然会失败)
        self.receivers = ['908422490@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        #content = '我用Python'
        #title = '人生苦短'  # 邮件主题

    def sendEmail(self,title,content):
        message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
        message['From'] = "{}".format(self.sender)
        message['To'] = ",".join(self.receivers)
        message['Subject'] = title
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)  # 启用SSL发信, 端口一般是465
            smtpObj.login(self.mail_user, self.mail_pass)  # 登录验证
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())  # 发送
            print("mail has been send successfully.")
        except smtplib.SMTPException as e:
            print(str(e))
            
class BSTool():
    def getTodayAll(x):
        content=""
        bs=BeautifulSoup(x,'lxml')
        body=bs.body
        todayInfo=body.find('div',{'class':"today clearfix",'id':'today'})
        input_=todayInfo.find_all('input')
        for item in input_:
            print(item['value'])
            content+=item['value']

        today_SK=todayInfo.find('div',{'class':'t'})
        print(today_SK)
        test=today_SK.find('p',{'class':'time'})
        print(test)
            
        today_ZW=todayInfo.find('ul',{'class':'clearfix'})       
        li=today_ZW.find_all('li',recursive=False)
        for item in li:
            #print(item)
            #print(item.find('h1').string)
            #print(item.find('p',{'class':'wea'}).string)
            content+=item.find('h1').string
            content+=item.find('p',{'class':'wea'}).string
            p=item.find('p')
            for items in p:
                #print(items.find_next('p',{'class':'tem'}).span.string,"°C")
                #print(items.find_next('p',{'class':'win'}).span.string)
                #print(items.find_next('p',{'class':'sun'}).span.string)
                content+=str(items.find_next('p',{'class':'tem'}).span.string)
                content+=str(items.find_next('p',{'class':'win'}).span.string)
                content+=str(items.find_next('p',{'class':'sun'}).span.string)
                
        return content

class NewBSTool():
    def getTodayAll(x):
        content=""
        bs=BeautifulSoup(x,'html5lib')
        body=bs.body
        todayInfo=body.find('div',{'class':"today clearfix",'id':'today'})
        input_=todayInfo.find_all('input')
        for item in input_:
            print(item['value'])
            content+=item['value']

        today_SK=todayInfo.find('div',{'class':'t'})
        print(today_SK)
        test=today_SK.find('p',{'class':'time'})
        print(test)
            
        today_ZW=todayInfo.find('ul',{'class':'clearfix'})       
        li=today_ZW.find_all('li',recursive=False)
        for item in li:
            #print(item)
            #print(item.find('h1').string)
            #print(item.find('p',{'class':'wea'}).string)
            content+=item.find('h1').string
            content+=item.find('p',{'class':'wea'}).string
            p=item.find('p')
            for items in p:
                #print(items.find_next('p',{'class':'tem'}).span.string,"°C")
                #print(items.find_next('p',{'class':'win'}).span.string)
                #print(items.find_next('p',{'class':'sun'}).span.string)
                content+=str(items.find_next('p',{'class':'tem'}).span.string)
                content+=str(items.find_next('p',{'class':'win'}).span.string)
                content+=str(items.find_next('p',{'class':'sun'}).span.string)
                
        return content
class RETool():
    getBodyer = re.compile('<body>(.*?)</body>',re.S)
    removeStyle = re.compile('<style>.*</style>',re.S)  #//@"<script[^>]*?>.*?</script>" //去除所有脚本，中间部分也删除
    removeScript = re.compile('<script[^>]*?>.*?</script>',re.S)
    

    
spider = Spider()
page=spider.getPageCode()
content=NewBSTool.getTodayAll(page)
print(content)
#mail=MailPostfix()
#mail.sendEmail('小金天气预报',content)
