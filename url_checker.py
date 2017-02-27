#!/usr/bin/python
#run success on py2.7
#-*-coding:utf-8 -*-
'''
Created on 2017-1-9
@author: wjt
Description:
'''
import httplib
#用类来包装线程对象
import threading
import time,datetime
import smtplib 
def http_open(url):
    try:
        conn = httplib.HTTPConnection(url)
        conn.request("GET", "/")
        r=conn.getresponse()
        return r.status  
    except Exception,e:
        return e
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate 
#server['host'], server['user'], server['passwd']
def send_mail(text): 
    msg = MIMEMultipart() 
    msg['From'] = "myqq@qq.com"
    msg['Subject'] = u"检测异常" 
    msg['To'] = COMMASPACE.join("myqq@qq.com")
    msg['Date'] = formatdate(localtime=True) 
    msg.attach(MIMEText(text,'html','GBK')) 
    smtp = smtplib.SMTP("smtp.qq.com",465) 
    smtp.login("myqq@qq.com", "******") 
    smtp.sendmail("myqq@qq.com", "myqq@qq.com", msg.as_string()) 
    smtp.close()
    
class check(threading.Thread): 
    def __init__(self, url ,interval):
        threading.Thread.__init__(self)
        self.interval = interval
        self.url=url
    def run(self): #Overwrite run() method, put what you want the thread do here
        status = http_open(self.url)
        if status not in (200,302):
            print u"站点[%s]响应异常，状态为：%s。"%(self.url,status)
        
#        if status==200:
#            print u"站点[%s]响应正常，状态为：%s"%(self.url,status)
#        elif status==302:
#            print u"站点[%s]响应正常，状态为：%s"%(self.url,status)
#        else:
#            print u"站点[%s]响应异常，状态为：%s"%(self.url,status)
#            send_mail(u"站点[%s]响应异常，状态为：%s"%(self.url,status))
        time.sleep(self.interval)
def main():
    urls=["www.baoan.edu.cn",
          "jy.baoan.gov.cn",
          "jcpt.baoan.edu.cn",
#         ......
          "sywmxx.baoan.edu.cn"
          ]
    thread_list =[]
    print u"****************************"
    print u"Python网站监控"
    print u"****************************"
    #print u"共检测%s个网站"%len(urls)
    while(True):
        print u"Python网站监控报告，共检测%s个网站。"%len(urls)
        print u"执行时间:%s"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        for url in urls:
            thread = check(url,10)
            thread.start()
            thread_list.append(thread)
        time.sleep(60)
        print "\n\n"     
if __name__ == "__main__":
    main()
