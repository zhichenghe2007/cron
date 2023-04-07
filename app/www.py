#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from application import app
'''
所有蓝图url配置
'''
from web.controllers.notify import route_notify
from web.controllers.argo import route_argo
from web.controllers.gitlab import route_gitlab

import json

app.register_blueprint(route_notify, url_prefix="/notify")
app.register_blueprint(route_argo, url_prefix="/cron_service/api/v1/argo")
app.register_blueprint(route_gitlab, url_prefix="/cron_service/api/v1/gitlab")


@app.route("/heartbeat")
def heartbeat():
    return json.dumps({"status": "healthy"})
