# 创建网络
docker network create kong-net

# 安装postgres数据库
docker run -d --name kong-database \
--network=kong-net \
-p 5432:5432 \
-e "POSTGRES_USER=kong" \
-e "POSTGRES_DB=kong" \
-e "POSTGRES_PASSWORD=kong" \
postgres:11.7

#初始化kong数据库
docker run --rm \
--network=kong-net \
-e "KONG_DATABASE=postgres" \
-e "KONG_PG_HOST=kong-database" \
-e "KONG_PG_PASSWORD=kong" \
-e "KONG_CASSANDRA_CONTACT_POINTS=kong-database" \
kong:latest kong migrations bootstrap

#启动kong
docker run -d --name kong \
--network=kong-net \
-e "KONG_DATABASE=postgres" \
-e "KONG_PG_HOST=kong-database" \
-e "KONG_PG_PASSWORD=kong" \
-e "KONG_CASSANDRA_CONTACT_POINTS=kong-database" \
-e "KONG_PROXY_ACCESS_LOG=/dev/stdout" \
-e "KONG_ADMIN_ACCESS_LOG=/dev/stdout" \
-e "KONG_PROXY_ERROR_LOG=/dev/stderr" \
-e "KONG_ADMIN_ERROR_LOG=/dev/stderr" \
-e "KONG_ADMIN_LISTEN=0.0.0.0:8001, 0.0.0.0:8444 ssl" \
-p 80:8000 \
-p 443:8443 \
-p 8001:8001 \
-p 8444:8444 \
kong:latest

# 启动konga
docker run -d \
-p 1337:1337 \
--network kong-net \
-e "TOKEN_SECRET=kongtoken" \
-e "DB_ADAPTER=postgres" \
-e "DB_HOST=kong-database" \
-e "DB_USER=kong"  \
-e "DB_PASSWORD=kong" \
 --name konga \
pantsel/konga


#启动kong-dashboard/konga
docker run --rm -p 8080:8080 --network=kong-net \
pgbi/kong-dashboard  start --kong-url http://kong:8001



# 迁移konga数据表到pgsql
docker run --name konga --rm \
--network=kong-net \
pantsel/konga -c prepare -a postgres -u postgresql://kong:kong@kong-database:5432/kong
