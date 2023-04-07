# -*- coding: utf-8 -*-
from application import app
from flask import Blueprint, request, jsonify
from common.libs.Helper import getFeiShuUrl, sendFeiShu, get_return_json

route_notify = Blueprint('route_notify', __name__)

@route_notify.route("/cron", methods=["POST"])
def notify_cron():
    resp = get_return_json(200, 'sucess', {})
    req = request.json
    params = req['params'] if 'params' in req else ''
    if params:
        script = params['script'] if 'script' in params else ''
    if script:
       feishu_url = getFeiShuUrl(script)
    else:
        resp['code'] = -1
        resp['msg'] = "no script input!"
        return jsonify(resp)      
    text = req['text'] if 'text' in req else ''
    if not text:
        resp['code'] = -1
        resp['msg'] = "no text input!"
        return jsonify(resp)          
    if 'Job completed' in text:
        title = app.config['SUCESS_TITLE']
        # r = sendFeiShu(title, feishu_url)
        # r = sendFeiShu(str(text), feishu_url)
    elif 'Job failed' in text:
        title = app.config['JOB_FAILED_TITLE']
        r = sendFeiShu(title, feishu_url)
        r = sendFeiShu(str(text), feishu_url)
    elif 'Failed to launch' in text:
        title = app.config['FAILED_LAUNCH_TITLE']
        r = sendFeiShu(title, feishu_url)
        r = sendFeiShu(str(text), feishu_url)
    # app.logger.info(script)
    # app.logger.info(feishu_url)
    # app.logger.info(text)
    return jsonify(resp)


@route_notify.route("/feishu", methods=["POST"])
def notify_feishu():
    resp = get_return_json(200, 'sucess', {})
    req = request.json
    # app.logger.info(req)
    feishu = req['feishu'] if 'feishu' in req else ''
    message = req['message'] if 'message' in req else ''
    if not feishu:
        resp['code'] = -1
        resp['msg'] = "donn't have feishu url"
        return jsonify(resp)
    if not message:
        resp['code'] = -1
        resp['msg'] = "donn't have message to send"
        return jsonify(resp)

    sendFeiShu(message, feishu)
    return jsonify(resp)