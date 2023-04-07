## 生产环境部署
```
cd /data/cron
rm /data/cron/app/logs/*
rm /data/cron/work1/app.tar.gz
tar --exclude='*.pyc' -Pczvf work1/app.tar.gz app/
cd work1/ 
````


## 构建镜像
```sh
sudo docker build . --no-cache -t reg.deeproute.ai/deeproute-simulation-services/cron:v2.1
```


## 推送到公司仓库
``` sh
sudo docker push reg.deeproute.ai/deeproute-simulation-services/cron:v2.1
```

## 生产环境部署
```
cd work1/ 
kubectl apply -f cron_deploy.yaml
kubectl apply -f cron_service.yaml
kubectl apply -f cron_ingress.yaml
````