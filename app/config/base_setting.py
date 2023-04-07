#!/usr/bin/env python3
# -*- coding: utf-8 -*-
SERVER_PORT = 8081
DEBUG = False
SQLALCHEMY_ECHO = False
DEFAULT_FEISHU_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/88a0213c-6d6a-422d-bc74-cb1110df12ba"
SUCESS_TITLE = '【通知】cron平台定时job运行成功，详细job信息如下：'
JOB_FAILED_TITLE = '【!!!!异常!!!】cron平台定时job运行失败，详细job信息如下：'
FAILED_LAUNCH_TITLE = '【!!!!异常!!!】cron平台定时job调用失败，详细job信息如下：'

FAILED_ARGO_JOB_TITLE = '【!!!!异常!!!】argo job运行失败，详细job信息如下：'
SUCCEED_ARGO_JOB_TITLE = '【通知】argo job运行成功，详细workflow信息如下：'


FAILED_GITLAB_JOB_TITLE = '【!!!!异常!!!】gitlab 流水线运行失败，详细job信息如下：'
SUCCEED_GITLAB_JOB_TITLE = '【通知】gitlab 流水线运行成功，详细流水线信息如下：'

NOTIFY_JOB_INTERVAL = 5
