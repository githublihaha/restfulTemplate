# Restful API with Docker

应用的Restful API接口，使用Docker部署，配置了 uwsgi、nginx、sqlite。

整个项目是为某个命令或者工具封装RESTful接口的目录结构，或者大体框架。

## 目录结构说明
```
.
├── Dockerfile
├── README.md
└── yourappname_app
    ├── app
    │   ├── __init__.py
    │   ├── libs
    │   │   ├── database.py
    │   │   ├── extract_file.py
    │   │   ├── get_arg_list.py
    │   │   └── __init__.py
    │   ├── models
    │   │   ├── __init__.py
    │   │   └── taskModel.py
    │   └── resources
    │       ├── __init__.py
    │       ├── specs
    │       │   └── openapi.yml
    │       └── tasks.py
    ├── main.py
    ├── requirements.txt
    ├── run.py
    └── venv

```
+ Dockerfile
   构建Docker镜像的文件，文件中需要改的地方就是：安装上需要的命令或者工具
+ yourappname_app
   存放写的web代码的地方
+ yourappname_app/app
   主要的web代码，libs中是一些依赖脚本，models中是数据库模板，resources中是写利用flask_restful实现主要业务逻辑的地方，其中的specs文件夹下是存放SwaggerUI使用的openapi.yml文件的地方
+ yourappname_app/main.py
   定义app，添加 restful resources的地方
+ yourappname_app/run.py
   本地运行、调试用的启动脚本。本地运行直接`python run.py`即可
+ yourappname_app/venv
   虚拟python环境目录

## 使用 Docker 部署服务

1. 构建镜像 `docker build -t app_name:v1.0 .`
2. 启动容器 `docker run -d --name app_rest -p 80:80 app_name:v1.0`
3. API Doc地址 `http://localhost/apidocs/`

