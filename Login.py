#!/usr/bin/env python
import socket
import datetime
import re
import argparse
import requests
import getpass


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

            # 使用浏览器调试的时候知道，登陆数据不是直接传给url2的，而是传给
            # post_url的，192.168.7.221的801口的 eportal，且格式也是更改了的，
            # eportal可能是后端API吧，就是那种将再在服务器上另外开发的方法，而不
            # 是在后端中处理。
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


if __name__ == "__main__":
    # TODO: add surpport read from json
    parser = argparse.ArgumentParser(description="CSUST campus network login")

    parser.add_argument('username', action="store", help="Your School ID你的学号")
    parser.add_argument(
        '-p',
        '--password',
        action="store",
        help=
        """
        (optional) Your Internet password. Can also set from input invisibly.
        (可选)你的密码，可以稍后从输入用不显示的方法读取"""
    )

    options = parser.parse_args()
    password = options.password
    username = options.username

    if not password:
        passwd = getpass.getpass("Input your password:")

    if username:
        login(username, password)
