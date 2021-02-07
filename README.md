# Restful API with Docker

应用的Restful API接口，使用Docker部署，配置了 uwsgi、nginx、sqlite。

整个项目是为某个命令或者工具封装RESTful接口的目录结构，或者大体框架。



## 使用

1. 构建镜像 `docker build -t app_name:v1.0 .`
2. 启动容器 `docker run -d --name app_rest -p 80:80 app_name:v1.0`
3. API Doc地址 `http://localhost/apidocs/`

