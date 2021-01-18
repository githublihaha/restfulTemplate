# Apache Bench Restful API with Docker

Apache Bench的Restful API接口，使用Docker部署，配置了 uwsgi、nginx、sqlite。

## 使用

1. 构建镜像 `docker build -t ab:v1.0 .`
2. 启动容器 `docker run -d --name abrest -p 80:80 ab:v1.0`
3. API Doc地址 `http://localhost/apidocs/`

