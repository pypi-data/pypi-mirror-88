

自动注册服务
自动识别正在运行中的docker container并注册为服务

```shell script
docker run -d --name=registrator --net=host --volume=/var/run/docker.sock:/tmp/docker.sock gliderlabs/registrator:latest consul://172.31.68.243:8500

```