import requests
import time
import json


class Proxy():
    """docstring for Proxy"""
    def __init__(self):
        self.MAX = 5 #最大嗅探次数
        self.headers = {
            "User-Agent":"User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Referer":"https://www.lagou.com/jobs/list_python?city=%E6%9D%AD%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput=",
            "X-Anit-Forge-Code":"0",
            "X-Anit-Forge-Token":"None",
            "X-Requested-With":"XMLHttpRequest"
        }

    def getPage(self,url,data):
        FAILTIME = 0 #访问失败次数
        try:
            result = requests.post(url,headers=self.headers,data=data)
            result.encoding = 'utf-8'
            return result
        except :
            FAILTIME += 1
            if FAILTIME == self.MAX:
                print('访问错误')
                return ''


class Job(object):
    """docstring for Job"""
    def __init__(self):
        self.datalist = []

    def getJob(self,url,data):
        p = Proxy()
        result = p.getPage(url,data)
        result.encoding = 'utf-8'
        result_dict = result.json()

        try:
            job_info = result_dict['content']['positionResult']['result']
            for info in job_info:
                print(info)
            return job_info
        except :
            print('发生解析错误')

if __name__ == '__main__':
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%9D%AD%E5%B7%9E&needAddtionalResult=false&isSchoolJob=0'
    job = Job()
    all_page_info = []
    for x in range(1,7):
        data = {
            "first":"false",
            "pn":x,
            "kd":'python'
        }
        current_page_info=job.getJob(url,data)
        all_page_info.extend(current_page_info)
        print('第 %d 页已经爬取成功\n' %x)
        print('****'*20)
        time.sleep(5)

