# -*- coding: utf-8 -*-
import requests,time
from application import app
from sqlalchemy import true
from common.libs.Helper import get_http_json_with_token, sendFeiShu

class MonitorService():
    def __init__(self, url=None, namespace=None, id=None):
        self.url = url
        self.namespace = namespace
        self.id = id

    def monitor_argo_job(self, notifyUrl, notifyOn):
        uid_url = str(self.url) + "/api/v1/archived-workflows/" + str(self.id)
        while true:
            r = requests.get(uid_url)
            if r.status_code == 404:
                time.sleep(180)
                app.logger.info("workflow not archived")
                app.logger.info(r.status_code)
            elif r.status_code != 200:
                app.logger.info("get uid_url have issue")
                app.logger.info(r.status_code)
                break
            else:
                app.logger.info("workflow archived success")
                app.logger.info(r.status_code)
                break
        if r.status_code == 200:
            r_json = r.json()
            node_dict = r_json["status"]["nodes"]
            faild_job_count = 0
            for node in node_dict.values():
                job_id = node["id"]
                job_phase = node["phase"]
                job_type = node["type"]
                job_url = str(self.url) + "/archived-workflows/" + str(
                    self.namespace) + "/" + "?nodeId=" + str(job_id)
                if "Pod" in job_type:
                    if job_phase == "Failed":
                        faild_job_count = faild_job_count + 1
                        if "Failed" in notifyOn or "all" in notifyOn:
                            message1 = app.config["FAILED_ARGO_JOB_TITLE"]
                            url = notifyUrl
                            sendFeiShu(message1, url)
                            message2 = job_url
                            sendFeiShu(message2, url)
                            app.logger.info(message2)
            if faild_job_count == 0:
                if "Succeed" in notifyOn or "all" in notifyOn:
                    message1 = app.config["SUCCEED_ARGO_JOB_TITLE"]
                    url = notifyUrl
                    sendFeiShu(message1, url)
                    workflowUrl = self.url + "/archived-workflows/" + self.namespace + "/" + str(
                        self.id)
                    sendFeiShu(workflowUrl, url)
                    app.logger.info(workflowUrl)
            return 1
        else:
            return 0

    def monitor_gitlab_job(self, notifyUrl, notifyOn):
        gitlab_monitor_url = str(self.url)
        token = str(self.id)
        app.logger.info(gitlab_monitor_url)
        while true:
            try:
                r = get_http_json_with_token(gitlab_monitor_url, token)
            except Exception as e:
                result = 0
                app.logger.info(e)
                break
            break_info = 0
            app.logger.info(r)
            for x in r:
                if x["status"] not in ["created", "pending", "running"]:
                    break_info = 1
                    app.logger.info(x["status"])
            app.logger.info(break_info)
            if break_info:
                result = 1
                break
            else:
                time.sleep(180)
        if result == 0:
            return result
        if r:
            faild_job_count = 0
            for x in r:
                job_status = x["status"]
                job_url = x["web_url"]
                if job_status not in ["success"]:
                    faild_job_count = faild_job_count + 1
                    if "Failed" in notifyOn or "all" in notifyOn:
                        message1 = app.config["FAILED_GITLAB_JOB_TITLE"]
                        url = notifyUrl
                        sendFeiShu(message1, url)
                        message2 = job_url
                        sendFeiShu(message2, url)
                        app.logger.info(message2)
            if faild_job_count == 0:
                if "Succeed" in notifyOn or "all" in notifyOn:
                    message1 = app.config["SUCCEED_GITLAB_JOB_TITLE"]
                    url = notifyUrl
                    sendFeiShu(message1, url)
                    pipelineUrl = str(self.namespace)
                    sendFeiShu(pipelineUrl, url)
                    app.logger.info(pipelineUrl)
            return 1
        else:
            return 0