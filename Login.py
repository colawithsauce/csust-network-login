#!/usr/bin/env python
import socket
import datetime
import re
import requests


def checkAccessWAN():
    "Check whether the connection to the WAN"
    s = socket.socket()
    s.settimeout(3)
    try:
        status = s.connect_ex(("www.baidu.com", 443))
        if status == 0:
            s.close
            return True
        return False
    except:
        return False


def login(name, password):
    "Simulate login"
    if not checkAccessWAN():
        print("[01] {} Device offline.".format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        # Get Login Page
        url = 'http://1.1.1.1/?isReback=1'
        try:
            # 获取登陆页面网址
            a = requests.get(url=url, allow_redirects=False, timeout=5)
            url2 = a.headers['Location']

            # TODO: 试图使用更加好的方法来直接替换
            b = str(url2).split('&')
            wlanuserip = ''
            wlanacname = ''
            wlanacip = ''
            wlanusermac = ''

            for i in b:
                if 'wlanuserip' in i:
                    wlanuserip = i.split('=')[-1]
                elif 'wlanacip' in i:
                    wlanacip = i.split('=')[-1]
                elif 'wlanacname' in i:
                    wlanacname = i.split('=')[-1]
                elif 'wlanusermac' in i:
                    wlanusermac = i.split('=')[-1][:12]
                    wlanusermac = re.findall(r'\w{1,2}', wlanusermac)
                    wlanusermac = '-'.join(wlanusermac)

            print("路由器网关地址:" + wlanuserip)
            print("连接路由器型号:" + wlanacname)
            print("用户IP地址:" + wlanacip)
            print("路由器MAC地址:" + wlanusermac)
            post_url = 'http://192.168.7.221:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=192.168.7.221&iTermType=1&wlanuserip={wlanuserip}&wlanacip={wlanacip}&wlanacname={wlanacname}&mac={wlanusermac}&ip={wlanuserip}&enAdvert=0&queryACIP=0&loginMethod=1'.format(
                wlanusermac=wlanusermac,
                wlanacip=wlanacip,
                wlanacname=wlanacname,
                wlanuserip=wlanuserip)

            # Login
            log_data = {
                "DDDDD": ",0," + name,
                "upass": password,
                "0MKKey": "123456",
                "R1": "0",
                "R2": "0",
                "R3": "0",
                "R6": "0",
                "para": "00"
            }
            result = requests.post(post_url, data=log_data)
            print(result.text)

        except:
            print("[03] {} Error Login".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    else:
        print("[00] {} Device login".format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
