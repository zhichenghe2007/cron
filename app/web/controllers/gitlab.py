# -*- coding: utf-8 -*-
import json, requests
from re import sub
from application import app
from flask import Blueprint, request, jsonify
from common.libs.Helper import get_return_json, post_http_json_with_token
from common.libs.MonitorService import MonitorService
route_gitlab = Blueprint('route_gitlab', __name__)


@route_gitlab.route("/create", methods=["POST"])
def gitlab_create():
    resp = get_return_json(200, 'success', {})
    req = request.json
    token = req['token'] if 'token' in req else ''
    projectId = req['projectId'] if 'projectId' in req else ''
    brancheName = req['brancheName'] if 'brancheName' in req else ''
    variables = req['variables'] if 'variables' in req else ''
    notifyUrl = req['notifyUrl'] if 'notifyUrl' in req else ''
    notifyOn = req['notifyOn'] if 'notifyOn' in req else 'gitlabJobFailed'
    app.logger.info(req)
    if not token:
        resp['code'] = -1
        resp['msg'] = "donn't have token"
        return jsonify(resp)
    if not projectId:
        resp['code'] = -1
        resp['msg'] = "donn't have projectId"
        return jsonify(resp)
    if not brancheName:
        resp['code'] = -1
        resp['msg'] = "donn't have brancheName"
        return jsonify(resp)
    if variables:
        variables_new = variables.replace("'", "\"")
        variables_obj = json.loads(variables_new)
        if not isinstance(variables_obj,list):
            resp['code'] = -1
            resp['msg'] = "the variables which you put is wrong!"
            return jsonify(resp)
    result = submit_gitlab(token, projectId, brancheName, variables_obj)
    app.logger.info(result)
    resp['msg'] = result['msg']
    resp['data'] = result['data']
    if result['code'] != 0:
        resp['code'] = -1
        return jsonify(resp)
    if not notifyUrl:
        resp[
            'msg'] = "submit to gitlab success, but no notifyUrl, so can not report job status to y!"
        return jsonify(resp)
    job = result['data']['jobClassInstance'].monitor_gitlab_job
    if 'jobClassInstance' in resp['data']:
        del resp['data']['jobClassInstance']
    job_result = job(notifyUrl, notifyOn)
    if job_result == 0:
        resp['msg'] = "submit to gitlab success, but monitor gitlab status failed!"
        return jsonify(resp)
    else:
        return jsonify(resp)


def submit_gitlab(token, projectId, brancheName, variables_obj):
    if variables_obj:
        app.logger.info(variables_obj)
        var_list = []
        for item in variables_obj:
            item_str = "variables[][key]={0}&variables[][value]={1}".format(item['key'], item['value'])        
            var_list.append(item_str)
        var_str = '&'.join(var_list)
        gitlabUrl = "https://code.deeproute.ai/api/v4/projects/{0}/pipeline?ref={1}&{2}".format(int(projectId), str(brancheName), var_str)
    else:
        gitlabUrl = "https://code.deeproute.ai/api/v4/projects/{0}/pipeline?ref={1}".format(int(projectId), str(brancheName))
    app.logger.info(gitlabUrl)
    try:
        r = post_http_json_with_token(gitlabUrl, token)
    except Exception as e:
        result = get_return_json(1, 'failed to submit gitlab', {"erroInfo": e})
        app.logger.info(e)
        return result
    app.logger.info(r)
    pipelineId = r["id"]
    pipelineUrl = r["web_url"]
    if not pipelineId:
        result = get_return_json(2, 'can not get pipelineId from response', {})
        return result
    if not pipelineUrl:
        result = get_return_json(3, 'can not get pipelineUrl from response', {})
        return result    
    app.logger.info(pipelineId)
    app.logger.info(pipelineUrl)
    gitlab_monitor_url = "https://code.deeproute.ai/api/v4/projects/{0}/pipelines/{1}/jobs".format(projectId, pipelineId)
    gitlabMonitorService = MonitorService(gitlab_monitor_url, pipelineUrl, token)
    result = get_return_json(
        0,
        'submit to gitlab success, the job status will report to your notifyUrl after job finish!',
        {
            "pipelineUrl": pipelineUrl,
            "jobClassInstance": gitlabMonitorService
        })
    return result
