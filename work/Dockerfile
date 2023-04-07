# Ubuntu+python3
#
# Authoer: zhichenghe

FROM deeproute-simulation-registry-registry.cn-shenzhen.cr.aliyuncs.com/simulation-platform/python3script:base1
COPY requirements.txt /data/
WORKDIR /data/

RUN apt-get update \
    && apt-get install -y libmysqld-dev python-dev nginx \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install -r requirements.txt