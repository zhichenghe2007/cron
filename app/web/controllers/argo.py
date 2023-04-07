# -*- coding: utf-8 -*-
import json, requests
from re import sub
from application import app
from flask import Blueprint, request, jsonify
from common.libs.Helper import get_return_json, getNamespace, getUrl
from common.libs.MonitorService import MonitorService

route_argo = Blueprint('route_argo', __name__)


@route_argo.route("/create", methods=["POST"])
def argo_create():
    resp = get_return_json(200, 'success', {})
    req = request.json
    argoUrl = req['argoUrl'] if 'argoUrl' in req else ''
    workflowTemplateName = req[
        'workflowTemplateName'] if 'workflowTemplateName' in req else ''
    workflowParameters = req[
        'workflowParameters'] if 'workflowParameters' in req else ''
    notifyUrl = req['notifyUrl'] if 'notifyUrl' in req else ''
    notifyOn = req['notifyOn'] if 'notifyOn' in req else 'argoJobFailed'
    if not argoUrl:
        resp['code'] = -1
        resp['msg'] = "donn't have argoUrl"
        return jsonify(resp)
    if not workflowTemplateName:
        resp['code'] = -1
        resp['msg'] = "donn't have workflowTemplateName"
        return jsonify(resp)
    if not workflowParameters:
        resp['code'] = -1
        resp['msg'] = "donn't have workflowParameters"
        return jsonify(resp)
    workflowParameters_new = workflowParameters.replace("'", "\"")
    workflowParameters_obj = json.loads(workflowParameters_new)
    result = submit_argo(argoUrl, workflowTemplateName, workflowParameters_obj)
    app.logger.info(result)
    resp['msg'] = result['msg']
    resp['data'] = result['data']
    if result['code'] != 0:
        resp['code'] = -1
        return jsonify(resp)
    if not notifyUrl:
        resp[
            'msg'] = "submit to argo success, but no notifyUrl, so can not report job status to y!"
        return jsonify(resp)
    job = result['data']['jobClassInstance'].monitor_argo_job
    if 'jobClassInstance' in resp['data']:
        del resp['data']['jobClassInstance']
    job_result = job(notifyUrl, notifyOn)
    if job_result == 0:
        resp['msg'] = "submit to argo success, but monitor argo status failed!"
        return jsonify(resp)
    else:
        return jsonify(resp)


def submit_argo(argoUrl, workflowTemplateName, workflowParameters_obj):
    namespace = getNamespace(argoUrl)
    url = getUrl(argoUrl)
    if not namespace:
        result = get_return_json(1, 'argoNamespace is wrong', {})
        return result
    if not url:
        result = get_return_json(2, 'argoUrl is wrong', {})
        return result
    submit_workflow_url = url + "/api/v1/workflows/{}/submit".format(namespace)
    parameters = []
    for key, value in workflowParameters_obj.items():
        if isinstance(value, str) and isinstance(key, str):
            item = key + "=" + value
            parameters.append(item)
        elif isinstance(value, list) and isinstance(key, str):
            item = key + "=" + json.dumps(value, separators=(",", ":"))
            parameters.append(item)
        else:
            result = get_return_json(3, 'the argo parameters is wrong', {})
            return result
    try:
        submit_workflow_response = requests.post(submit_workflow_url,
                                                 json={
                                                     "resourceKind":
                                                     "WorkflowTemplate",
                                                     "resourceName":
                                                     workflowTemplateName,
                                                     "submitOptions": {
                                                         "parameters":
                                                         parameters
                                                     }
                                                 })
        submit_workflow_response.raise_for_status()
    except Exception as e:
        result = get_return_json(4, 'failed to submit argo', {"erroInfo": e})
        app.logger.info(e)
        return result
    workflowName = submit_workflow_response.json()["metadata"]["name"]
    workflowUid = submit_workflow_response.json()["metadata"]["uid"]
    workflowUrl = url + "/archived-workflows/" + namespace + "/" + workflowUid
    app.logger.info(workflowName)
    app.logger.info(workflowUrl)
    argoMonitorService = MonitorService(url, namespace, workflowUid)
    result = get_return_json(
        0,
        'submit to argo success, the job status will report to your notifyUrl after job finish!',
        {
            "workflowName": workflowName,
            "workflowUrl": workflowUrl,
            "jobClassInstance": argoMonitorService
        })
    return result
