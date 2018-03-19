#coding:utf-8
import requests
import time
import json
import re
from bs4 import BeautifulSoup

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

    def getPage(self,proxy,url,data):
        FAILTIME = 0 #访问失败次数
        try:
            result = requests.post(url,headers=self.headers,proxies=proxy,data=data)
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

    def getJob(self,proxy,url,data):
        p = Proxy()
        result = p.getPage(proxy,url,data)
        result.encoding = 'utf-8'
        result_dict = result.json()

        try:
            job_info = result_dict['content']['positionResult']['result']
            for info in job_info:
                print(info)
            return job_info
        except :
            print('发生解析错误')



class ProxyIp(object):
    """docstring for testProxyIp"""
    def __init__(self):
        self.headers = {
            'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTczMWYzZjZhNWRkYzNkM2IxNGVjNGEzNmQwZDZjN2MyBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUJxMDVqUFkvS054bDRtdUxQZ0c1N3RjNmthbmljNGgrUjRHcWxyb2VkMm89BjsARg%3D%3D--35e5819e4f54b49e8c10114bc3e14607474f9d75; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1521076608,1521079303,1521080191,1521113992; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1521116316',
            'If-None-Match':'W/"cfbbf20bb114a3944ad3e851b55a7963"',
            'Upgrade-Insecure-Requests':'1',
            'Connection':'keep-alive',
            'Referer':'http://www.xicidaili.com/nn/',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }

    def getIp(self,url_ip):
        
        proxies = [
            {'http': 'http://218.15.25.153:808'},
        ]

        
            
        Ips = requests.get(url=url_ip,headers=self.headers).text
        soup = BeautifulSoup(Ips,'lxml')
        
        tag = soup.td
        # print(soup.td.contents)
        
        #选取一条记录 进行摘取，这里只拿了 访问方式，ip 和端口号
        IpPool = soup.select('.odd')
        for x in range(0,49):
            Ip = IpPool[x].select('td')
    
            # print(Ip[5].string)
            p_ip = Ip[1].string
            p_port = Ip[2].string
            p_http = Ip[5].string.lower()
            proxies.append({p_http:"%s://%s:%s" %(p_http,p_ip,p_port)})

        return proxies
    
        
        # for x in range(0,len(proxies)):
        #     print(proxies[x])
        
    def testIp(*ip_list):
        test_url = 'http://www.163.com/'
        net_headers = {
            'Cookie':'_ntes_nnid=b8f9714c845357ecc443cf1cd3f22992,1511920104761; _ntes_nuid=b8f9714c845357ecc443cf1cd3f22992; P_INFO=wengfe@126.com|1513821635|0|mail126|00&12|zhj&1513816565&mail126#zhj&330300#10#0#0|158321&0|mail126|wengfe@126.com; __e_=1514018335096; usertrack=ezq0plpDX0gMbWV0A/pPAg==; _ga=GA1.2.1076171521.1514364852; __f_=1517299364260; KAOLA_ACC=yd.f5b52e7ccb694709a@163.com; vjuids=-727c3f8f.1621962fc7e.0.d6630977664cb; ne_analysis_trace_id=1521008496313; s_n_f_l_n3=c39735d0e679206d1521008496476; vinfo_n_f_l_n3=c39735d0e679206d.1.2.1513560956178.1520844483770.1521008569271; NTES_YD_SESS=a.IpQFDyGmhFJzxDsTCpEphqJ6unVqSrXbE6XFFHtVmMd3GbdnHABw4iDaKroZAfE1ZKOiVaX1rCgxaKW96obLFEJxXGHVOL7xM6WXj4w7Wg0nxVN200P112ow2EWaQOPMteeaRRghxHweSknPp049SZ9sBqUPkKgVg5viKNe829Xi6z721IYmZVkp5AkffSRGxANphEer0JS56Tc_7im.rQUrcSWw5TR; NTES_YD_PASSPORT=4F2bMdMRObvRJ2amcH.JeimhxK98w7w6VWIG0ou_5WfL68YH69PjrGlFz3CeW0jhub0CyFL3gbejYETzh.91NeGYQSy_oui6hyt6a7PzF65eUA.WMsMaQCPKXCofMZf4.KFGrNSsgUKIcnV_yQyi3oEIwmuxhgtbklwuFGJKNODSHwMLjCkgRj4h6waHPjMl3QxT2UZ8TxUaG; NNSSPID=2bd6e3000f3a49d99554eae64fb97d75; NTES_hp_textlink1=old; vjlast=1520844340.1521080447.11',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
        #取 10 条 ip
        # 测试代理 ip 是否联通
        ip_list_real = []
        for num in range(2,len(ip_list)):
            proxies = ip_list[num]
            
            #不可用 ip 代理
            # proxies = {
            #     'http': 'http://218.15.25.153:808'
            #     }
            try:
                result = requests.get(url=test_url,headers=net_headers,proxies=proxies,timeout=1).text
            except :
                print(ip_list[num],'不可用')
                continue
            else:
                ip_list_real.append(proxies)
            # if len(result) > 2000:
            #     ip_list_real.append(proxies)
            # else :
            #     print(ip_list[num],'不可用')
            #     continue

            if len(ip_list_real) >= 10:
                print('已获得10个可用的代理 IP')
                break

        return ip_list_real

        

        # print(str(IpPool[0]))
        # # print(type(IpPool[0]))
        # re_Ip = re.compile(r'((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))')

        # re_port = re.compile(r'')

        # Ip = re_Ip.search(str(IpPool))
        # print(Ip.group())
        #-------------
        #    从原始文件中提取全部ip到list中
        # Ip = re_Ip.finditer(str(IpPool))
        # for ip in Ip:
        #     print(ip.group())
        #-------------

        # print(Ip.group())
        # print(Ips)



if __name__ == '__main__':
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%9D%AD%E5%B7%9E&needAddtionalResult=false&isSchoolJob=0'
    
    
    ip = ProxyIp()
    ip_list = []
    #爬取前三页 IP 进行校验
    for page in range(1,4):
        url = 'http://www.xicidaili.com/nn/{}'.format(page)
        ip_list.extend(ip.getIp(url))

    ip_real = ip.testIp(*ip_list)


    print(ip_real)



    # print(ip_list)

    



    # 爬取 拉勾网 数据
    # job = Job()
    # all_page_info = []
    # for x in range(1,7):
    #     data = {
    #         "first":"false",
    #         "pn":x,
    #         "kd":'python'
    #     }
    #     proxy_url = "122.114.31.177:808"
    #     proxy = {
    #         "http": proxy_url
    #     }

    #     current_page_info=job.getJob(proxy,url,data)
    #     all_page_info.extend(current_page_info)
    #     print('第 %d 页已经爬取成功\n' %x)
    #     print('****'*20)
    #     time.sleep(5)

