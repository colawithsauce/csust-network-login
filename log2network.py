#!/usr/bin/env python3
# coding=utf-8

import sys
import os
import socket
import datetime
import re
import argparse
import getpass
import time
import json
import base64
import platform
import requests


def exitProgram(exit_code):
    sysstr = platform.system()
    if sysstr == "Windows":
        input("程序执行完毕，按回车键退出...")
    sys.exit(exit_code)


def yes_or_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        print(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def deviceOnline():
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


def loginNetwork(name, passwd):
    "Simulate login"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_file = open(dir_path + "/login.log", "a")
    stdout_backup = sys.stdout
    sys.stdout = log_file
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

        post_url = 'http://192.168.7.221:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=192.168.7.221&iTermType=1&wlanuserip={wlanuserip}&wlanacip={wlanacip}&wlanacname={wlanacname}&mac={wlanusermac}&ip={wlanuserip}&enAdvert=0&queryACIP=0&loginMethod=1'.format(
            wlanusermac=wlanusermac,
            wlanacip=wlanacip,
            wlanacname=wlanacname,
            wlanuserip=wlanuserip)

        # Login
        log_data = {
            "DDDDD": ",0," + name,
            "upass": passwd,
            "0MKKey": "123456",
            "R1": "0",
            "R2": "0",
            "R3": "0",
            "R6": "0",
            "para": "00"
        }
        result = requests.post(post_url, data=log_data)

        # Check success_if
        # TODO: Get login error from server and show
        # print(result.text)
        if deviceOnline():
            print("[00] {} Login successed".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        else:
            print("[01] {} Login failed".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    except:
        print("[02] {} Error when Login".format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    finally:
        sys.stdout = stdout_backup
        log_file.close()


def get_login_data(use_new_account, config_file_name):
    "Get login datas"
    # base64 它的参数是byte类型，返回的值也是byte类型，所以需要在存储的时候对string进行byte编码，在读取的时候对byte解码。
    # 写入json文件的时候也是只能写入string而不能写入byte，所以在base64编码之后还要将其string化。
    if not use_new_account:
        # Read config from file, if did not exist, create one.
        try:
            config_file = open(config_file_name, "r")
            config = json.load(config_file)
            uname = config['uname']
            passwd = base64.b64decode(config['passwd'].encode()).decode()
            config_file.close()

        except:
            # File not found or file exist but have wrong keys.
            # Create config file
            config_file = open(config_file_name, "w+")
            # Read values from user input
            if not uname:
                uname = input("Enter the Student ID:")
            if not passwd:
                passwd = getpass.getpass(
                    "Enter the password (for security no echo):")
            # Write file
            config = {
                "uname": uname,
                "passwd": base64.b64encode(passwd.encode()).decode()
            }
            json.dump(config, config_file)
            # Close file
            config_file.close()

    else:
        uname = input("Enter the Student ID:")
        passwd = getpass.getpass("Enter the Password (for security no echo):")
        write_if = yes_or_no("Write data to the configuration file?")
        if write_if:
            config_file = open(config_file_name, "w+")
            # Write file
            config = {
                "uname": uname,
                "passwd": base64.b64encode(passwd.encode()).decode()
            }
            json.dump(config, config_file)
            # Close file
            config_file.close()

    return [uname, passwd]


def login(uname, passwd, times):
    "Try to login network TIMES times, with uname and passwd."
    for i in range(times):
        print("Trying the {}_th time".format(i + 1))
        loginNetwork(uname, passwd)
        if deviceOnline():
            print("Login Successed!")
            return 0
    print("{} login attempts all failed，Check if the connection to\
    csust-(dx|bg|lt) well, or if the password is correct".format(times))
    return 1


if __name__ == "__main__":
    # DONE: json store, base64 decode, and add argument --no-config-file
    # DONE: Surpport read and write with json
    parser = argparse.ArgumentParser(
        description="CSUST campus network login script",
        epilog=
        "The default configuration file which reads the user name and password to log in, if the configuration file does not exist or missing items, read user input from"
    )

    parser.add_argument(
        '-c',
        '--config-file',
        action="store",
        default="loginData.json",
        help="Specify the configuration file, 'loginData.json' by default")
    parser.add_argument(
        '-n',
        '--new-account',
        action="store_true",
        help=
        "Reading user data from the keyboard, rather than configuration file")
    parser.add_argument('--ensure',
                        action="store_true",
                        help="Ensure login state, prevent user offline")

    options = parser.parse_args()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_file_name = os.path.join(dir_path, options.config_file)
    # 当配置文件尚不存在的时候就必然是需要 new_login 的
    use_new_account = True if not os.path.exists(config_file_name) else options.new_account
    ensure_login_flag = options.ensure
    [uname, passwd] = get_login_data(use_new_account, config_file_name)

    # Only run when offline
    if deviceOnline():
        print("Already connected to the Internet")
        if not ensure_login_flag:
            exitProgram(0)

    if not ensure_login_flag:
        print("Trying to log in...")
        EXITSTATE = login(uname, passwd, 3)
        exitProgram(EXITSTATE)
    else:
        print("Ensureing your network connection.")
        while True:
            if not deviceOnline():
                print("Device had off line! Reconnecting ...")
                login(uname, passwd, 3)
            time.sleep(3)
