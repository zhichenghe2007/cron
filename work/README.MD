## 构建镜像
```sh
sudo docker build . --no-cache -t reg.deeproute.ai/deeproute-simulation-services/python-flask:v1.3
```


## 推送到腾讯云镜像仓库
``` sh
sudo docker push reg.deeproute.ai/deeproute-simulation-services/python-flask:v1.3
```