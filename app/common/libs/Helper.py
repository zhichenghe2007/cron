# -*- coding: utf-8 -*-
from __future__ import division
import datetime

from sqlalchemy import true
from application import app
import requests, json, time
from apscheduler.schedulers.background import BackgroundScheduler
'''
定义函数返回值
'''


def get_return_json(code, err_message, data):
    return {"code": code, "msg": err_message, "data": data}


'''
获取get请求的json返回值
'''


def get_http_json(url):
    r = requests.get(url)
    return r.json()

def get_http_json_with_token(url, token):
    headers = {'PRIVATE-TOKEN': token}
    r = requests.get(url, headers=headers)
    return json.loads(r.text)

def post_http_json_with_token(url, token):
    headers = {'PRIVATE-TOKEN': token}
    r = requests.post(url, headers=headers)
    return json.loads(r.text)


'''
根据url地址获取正确的argoUrl地址信息
'''


def getUrl(argoUrl):
    if "dev" in argoUrl and "aliyun" in argoUrl:
        url = "http://argo.simulation-platform-dev.aliyun.simulation.deeproute.net"
    elif "prod" in argoUrl and "aliyun" in argoUrl:
        url = "http://argo.simulation-platform-prod.aliyun.simulation.deeproute.net"
    elif "staging" in argoUrl and "aliyun" in argoUrl:
        url = "http://argo.simulation-platform-staging.aliyun.simulation.deeproute.net"
    elif "staging" in argoUrl and "map" in argoUrl:
        url = "http://argo.simulation-platform-staging.maplocalization.simulation.deeproute.ai"
    elif "dev" in argoUrl and "map" in argoUrl:
        url = "http://argo.simulation-platform-dev.maplocalization.simulation.deeproute.ai"
    elif "prod" in argoUrl and "map" in argoUrl:
        url = "http://argo.simulation-platform-prod.maplocalization.simulation.deeproute.ai"
    elif "prod" in argoUrl and "map" not in argoUrl and "aliyun" not in argoUrl:
        url = "http://argo.simulation-platform-prod.simulation.deeproute.ai"
    elif "dev" in argoUrl and "map" not in argoUrl and "aliyun" not in argoUrl:
        url = "http://argo.simulation-platform-dev.simulation.deeproute.ai"
    elif "staging" in argoUrl and "map" not in argoUrl and "aliyun" not in argoUrl:
        url = "http://argo.simulation-platform-staging.simulation.deeproute.ai"
    else:
        url = ''
    return url


'''
根据url地址获取namespace信息
'''


def getNamespace(argoUrl):
    if "dev" in argoUrl:
        namespace = "simulation-platform-dev"
    elif "prod" in argoUrl:
        namespace = "simulation-platform-prod"
    elif "staging" in argoUrl:
        namespace = "simulation-platform-staging"
    else:
        namespace = ''
    return namespace


'''
获取飞书url
'''


def getFeiShuUrl(script):
    script_list = script.split("####")
    feishu_url = script_list[1] if len(
        script_list) > 1 else app.config["DEFAULT_FEISHU_URL"]
    return str(feishu_url)


'''
发送飞书url
'''


def sendFeiShu(message, url):
    payload_message = {"msg_type": "text", "content": {"text": message}}
    headers = {'Content-Type': 'application/json'}

    response = requests.request("POST",
                                url,
                                headers=headers,
                                data=json.dumps(payload_message))
    return response


'''
定义发起循环监控任务状态的类
'''


def submitNotify(jobname, notifyUrl, notifyOn):
    scheduler = BackgroundScheduler()
    scheduler.add_job(jobname,
                      'date',
                      next_run_time=(datetime.datetime.now() +
                                     datetime.timedelta(minutes=1)),
                      args=[notifyUrl, notifyOn])
    app.logger.info(scheduler.get_jobs())


'''
获取当前时间
'''


def getCurrentDate(format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(format)


'''
获取格式化的时间
'''


def getFormatDate(date=None, format="%Y-%m-%d %H:%M:%S"):
    if date is None:
        date = datetime.datetime.now()

    return date.strftime(format)


'''
根据一个字段获取一个dic出来
'''


def getDictFilterField(db_model, select_filed, key_fileld, id_list):
    ret = {}
    query = db_model.query
    if id_list and len(id_list) > 0:
        query = query.filter(select_filed.in_(id_list))

    list = query.all()
    if not list:
        return ret

    for item in list:
        if not hasattr(item, key_fileld):
            break

        ret[getattr(item, key_fileld)] = item
    return ret


'''
根据一组对象获取这个对象里面想要的相关字段列表信息
'''


def selectFilterObj(obj, field):
    ret = []
    for item in obj:
        if not hasattr(item, field):
            continue
        if getattr(item, field) in ret:
            continue
        ret.append(getattr(item, field))

    return ret


def getDictListFilterField(db_model, select_filed, key_field, id_list):
    ret = {}
    query = db_model.query
    if id_list and len(id_list) > 0:
        query = query.filter(select_filed.in_(id_list))

    list = query.all()
    if not list:
        return ret
    for item in list:
        if not hasattr(item, key_field):
            break
        if getattr(item, key_field) not in ret:
            ret[getattr(item, key_field)] = []

        ret[getattr(item, key_field)].append(item)
    return ret
