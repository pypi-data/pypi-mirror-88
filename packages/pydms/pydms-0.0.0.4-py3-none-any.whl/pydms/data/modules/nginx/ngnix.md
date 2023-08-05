Nginx
---
高性能服务器，反向代理，负载均衡

### docker
```shell script
docker pull nginx
docker run -d -p 127.0.0.2:8080:80 --rm --name mynginx nginx
```
- 映射网页目录
```shell script
docker container run \
  -d \
  -p 127.0.0.2:8080:80 \
  --rm \
  --name mynginx \
  --volume "$PWD/html":/usr/share/nginx/html \
  nginx
```
- 映射配置
先拷贝配置
```shell script
docker container run \
  -d \
  -p 127.0.0.2:8080:80 \
  --rm \
  --name mynginx \
  --volume "$PWD/html":/usr/share/nginx/html \
  nginx
```
可以按需修改配置
最后映射配置目录
```shell script
docker container run \
  --rm \
  --name mynginx \
  --volume "$PWD/html":/usr/share/nginx/html \
  --volume "$PWD/conf":/etc/nginx \
  -p 127.0.0.2:8080:80 \
  -d \
  nginx
```

参考:[http://www.ruanyifeng.com/blog/2018/02/nginx-docker.html](http://www.ruanyifeng.com/blog/2018/02/nginx-docker.html)
