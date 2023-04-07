## 本地调试启动命令
```sh
export ops_config=local
nohup python3 manager.py runserver &
uwsgi --ini uwsgi.ini
```


## 生产环境部署
```
rm /data/cron/app/logs/*
rm /data/cron/work1/app.tar.gz
tar --exclude='*.pyc' -Pczvf work1/app.tar.gz app/ 
kubectl apply -f cron_deploy.yaml
kubectl apply -f cron_service.yaml
kubectl apply -f cron_ingress.yaml
````