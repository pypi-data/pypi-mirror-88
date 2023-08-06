# -*- coding: utf-8 -*-
# !/usr/bin/python
# Create Date 2018/11/7 0007
__author__ = 'huohuo'
import os
import requests
import logging
import time
import socket
import zipfile
import shutil
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from JYAliYun.AliYunMNS.AliMNSServer import MNSServerManager

# "错误消息通知群"
# "霍佩佩专用机器人"
# "e61184c4450f33a3313dc5651f7e63ed64c1e2e1f4dd37b585ffda93e9e801ee",
# 前端测试 通知
# https://oapi.dingtalk.com/robot/send?access_token=f0e012537fb60ac5e37be4239e9380e574eb65574f36446f7160750db9f413fe
#! /usr/bin/env python
# coding: utf-8


def test_chinese(contents):
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    # 一个小应用，判断一段文本中是否包含简体中：
    match = zhPattern.search(contents)
    if match:
        a = zhPattern.findall(contents)
        ch_num = 0
        for i in a:
            ch_num += len(i)
        return ch_num
    return 0


def sex2str(sex):
    if sex == 0:
        return '未知'
    elif sex == 1:
        return '男'
    else:
        return '女'


def float2percent(p):
    f = str(p).strip()
    if f in [u'无', 'None', '']:
        return 'N/A'
    elif f == "<1%":
        return f.replace("<", "&lt;")
    elif f == ">99%":
        return f
    elif '%' in f:
        return f
    else:
        f = '%.2f%%' % float(f)
    return f


def int2ch(i):
    chs = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
    return chs[i]


def zip_dir(lodurl, dirname, zipfilename, fileList=None):

    file_list = fileList or []
    #Check input ...
    fulldirname = dirname
    fullzipfilename = os.path.join(lodurl, zipfilename)
    print "Start to zip %s to %s ..." % (fulldirname, fullzipfilename)
    if not os.path.exists(fulldirname):
        print "Dir/File %s is not exist, Press any key to quit..." % fulldirname
        inputStr = raw_input()
        return
    if os.path.isdir(fullzipfilename):
        tmpbasename = os.path.basename(dirname)
        fullzipfilename = os.path.normpath(os.path.join(fullzipfilename, tmpbasename))
    if os.path.exists(fullzipfilename):
        print "%s has already exist, are you sure to modify it ? [Y/N]" % fullzipfilename
        while 1:
            inputStr = raw_input()
            if inputStr == "N" or inputStr == "n" :
                return
            else:
                if inputStr == "Y" or inputStr == "y" :
                    print "Continue to zip files..."
                    break

    #Get file(s) to zip ...
    if os.path.isfile(dirname):
        file_list.append(dirname)
        dirname = os.path.dirname(dirname)
    elif os.path.isdir(dirname):
        #get all file in directory
        for filename in os.listdir(dirname):
            file_list.append(os.path.join(dirname, filename))

    #Start to zip file ...
    destZip = zipfile.ZipFile(fullzipfilename, "w")
    i = 0
    for eachfile in file_list:
        destfile = eachfile[len(dirname):]
        print "Zip file %s..." % destfile
        destZip.write(eachfile, destfile)
        i += 1
    destZip.close()
    if i == len(file_list):
        return 5
    return 3


def roman_to_int(s):
    #     1~10: I II III IV V VI VII VIII IX X
    #     11~20: XI XII XIII XIV XV XVI XVII XVIII XIX XX
    """
    :type s: str
    :rtype: int
    """

    if s == 'Ⅲ':
        return 3
    elif s == 'Ⅴ':
        return 5
    elif s == 'Ⅷ':
        return 8
    else:
        try:
            romanInt = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100,'D': 500,'M': 1000}
            num = romanInt[s[0]]
            for i in range(1,len(s)):
                if romanInt[s[i]] > romanInt[s[i - 1]]:
                    num += romanInt[s[i]] - 2 * romanInt[s[i - 1]]
                else:
                    num += romanInt[s[i]]
            return num
        except:
            try:
                return int(s)
            except:
                print s


def send_msg_by_mns(message, **kwargs):
    """
    消息类型为文本时，data 格式如下：
    data = {
        "msgtype": "text",
        "text": {
            "content": "错误日志通知测试2017-08-21 10:14"
        },
        "at": {
            "atMobiles": [
                "18612660303",
                "15538819853"
            ],
            "isAtAll": True # True 表示@ALL, False 表示只 @ atMobiles 中的
        }
    }
    :param message:
    :param type: 消息类型，默认 text
    :param kwargs: 备用参数: mobile_phone 手机号，表示通知人，
                            access_token 通知机器人值，表示用哪个机器人
    :return:
    """
    use_mns = False
    MNS_CONF_PATH = os.environ.get('MNS_CONF_PATH')
    if MNS_CONF_PATH is not None:
        if os.path.exists(MNS_CONF_PATH):
            use_mns = True
        else:
            message = '\n【MNS_CONF_FILE】： %s not exists.\n\n%s\n' % (MNS_CONF_PATH, message)

    if use_mns:
        message += '\n【时间】：%s' % format_time()
        mns_server = MNSServerManager(conf_path=MNS_CONF_PATH)
        mns_topic = mns_server.get_topic("JYWaring")
        mns_topic.publish_message(message, "前端错误", is_thread=False)
    else:
        send_msg_by_dd(message)


def send_msg_by_dd(message, **kwargs):
    """
    消息类型为文本时，data 格式如下：
    data = {
        "msgtype": "text",
        "text": {
            "content": "错误日志通知测试2017-08-21 10:14"
        },
        "at": {
            "atMobiles": [
                "18612660303",
                "15538819853"
            ],
            "isAtAll": True # True 表示@ALL, False 表示只 @ atMobiles 中的
        }
    }
    :param message:
    :param type: 消息类型，默认 text
    :param kwargs: 备用参数: mobile_phone 手机号，表示通知人，
                            access_token 通知机器人值，表示用哪个机器人
    :return:
    """
    access_token = '136f44ec383377d7980bb43e9b8acb1eac0c1f6a6b31d6ba3ba10d43923751f8'
    env = get_value(kwargs, 'env', '环境')
    mobile_phone = get_value(kwargs, 'mobile_phone', '15538819853')
    txt_data = {
        "msgtype": "text",
        "text": {"content": '【Env】: %s\n%s\n【时间】：%s' % (env, message.rstrip('\n'), format_time())},
        "at": {
            # "atMobiles": [mobile_phone],
            "isAtAll": False}
    }
    url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % access_token
    header = {"Content-Type": "application/json"}
    try:
        requests.post(url, json=txt_data, headers=header, timeout=2)
    except Exception, e:
        logging.error(e.args)


def format_time(t=None, frm="%Y-%m-%d %H:%M:%S"):
    if t is None:
        t = time.localtime()
    if type(t) == int:
        t = time.localtime(t)
    my_time = time.strftime(frm, t)
    return my_time


def get_host(web_port, print_msg=''):
    host_name = socket.gethostname()
    host = socket.gethostbyname(host_name)
    url = 'http://%s:%s' % (host, web_port)
    print 'ip: "%s", name: %s, port: %d' % (host, host_name, web_port)
    print url
    if len(print_msg) > 0:
        print print_msg
    return {'ip': host, 'name': host_name, 'port': web_port, 'url': url}


def killport(port):
    command='''''kill -9 $(netstat -nlp | grep :'''+str(port)+''''' | awk '{print $7}' | awk -F"/" '{ print $1 }')'''
    os.system(command)


def get_value(disease_item, key, null=None):
    if isinstance(disease_item, dict):
        if key in disease_item:
            value = disease_item[key]
            if value is None:
                return null
            if isinstance(value, unicode) or isinstance(value, str):
                if value.strip() == '':
                    return null
                return value.strip()
            return value
    return null


def get_first_name(data):
    double_surnames = u'''欧阳、太史、端木、上官、司马、东方、独孤、南宫、万俟、闻人、夏侯、诸葛、尉迟、公羊、赫连、澹台、皇甫、宗政、濮阳、公冶、太叔、申屠、公孙、慕容、仲孙、钟离、长孙、宇文、司徒、鲜于、司空、闾丘、子车、亓官、司寇、巫马、公西、颛孙、壤驷、公良、漆雕、乐正、宰父、谷梁、拓跋、夹谷、轩辕、令狐、段干、百里、呼延、东郭、南门、羊舌、微生、公户、公玉、公仪、梁丘、公仲、公上、公门、公山、公坚、左丘、公伯、西门、公祖、第五、公乘、贯丘、公皙、南荣、东里、东宫、仲长、子书、子桑、即墨、达奚、褚师、吴铭'''
    name = data.get('name')
    if name is None:
        name = data.get('patient_name')
    if name is None:
        name = 'None'
    else:
        sex = data.get('sex')
        if sex is None:
            sex = data.get('gender')
        if name[:2] in double_surnames:
            surname = name[:2]
        else:
            surname = name[:1]
        if sex in [1, u'男']:
            name = surname + u"先生"
        elif sex in [2, u'女']:
            name = surname + u"女士"
    return name


def tcm_api():
    # 配置文件
    conf = read_conf()
    ports = conf.get('ports')
    endpoint = conf.get('endpoint')
    env = conf.get('env')
    # 请求相关
    method = request.method
    data = request.args if method == 'GET' else request.json
    url = request.headers.get('API-URL')
    api_service = request.headers.get('API-SERVICE')
    success_status = request.headers.get('SUCCESS-STATUS')
    api_method = request.headers.get('API-METHOD')
    if api_method is not None:
        method = api_method
    auth = request.headers.get('Authorization')
    # start
    error_message = ''
    response_data = None
    status = None
    if isinstance(conf, str):
        error_message = conf
    if ports is None:
        error_message = 'No ports found in config.conf'
    elif api_service not in ports:
        error_message = u'暂无此服务：%s. 目前服务有：%s\n' % (api_service, ports.keys())
    else:
        api_url = endpoint + ':' + ports[api_service] + url
        request_params = {'json': data} if method != 'GET' else {'params': data}
        headers = {'Content-Type': 'application/json'}
        if auth:
            headers['Authorization'] = auth
        request_params['headers'] = headers
        try:
            response = requests.request(method, api_url, **request_params)
        except Exception, e:
            error_message = '%s\n' % str(e)
            response = None
        if response is not None:
            if response.status_code != 200:
                error_message = "%s %s %d %s\n" % (api_url, "POST", response.status_code, response.text)
            else:
                response_data = response.json()
                status = response_data.get('status')
        error_message += u'【请求服务】：%s\n' % api_service
        error_message += u'【api】：%s\n' % api_url
    error_message += u'【访问ip】：%s\n' % request.remote_addr
    error_message += u'【访问地址】：%s\n' % request.url
    error_message += u'【请求方式】：%s\n' % method
    error_message += u'【请求数据】：%s\n' % json.dumps(data)
    if status is not None:
        error_message += u'【状态码】:%d\n' % status
    error_message += u'【返回数据】：%s\n' % json.dumps(response_data)
    try:
        sss = base64.b64decode(auth).decode()
        error_message += u'【用户名】：%s\n' % sss.split(':')[0]
    except:
        error_message += ''
    # if self.is_print:
    #     print error_message
    if 'success' not in error_message.lower():
        try:
            send_msg_by_dd(error_message, env=env)
        except:
            print(error_message)
    return jsonify(response_data)


def del_file(path):
    if os.path.exists(path) is False:
        return 'path not exists, %s' % path
    if os.path.isfile(path):
        os.remove(path)
        return True
    try:
        shutil.rmtree(path)
    except:
        os.rmdir(path)



if __name__ == "__main__":
    send_msg_by_dd('sss')
    pass
    

