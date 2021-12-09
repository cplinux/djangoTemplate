本模板适用于Django3.2 + python 3.8.8环境，目的为了快速创建Django项目模板。

## 一：安装软件包

### 1.1：修改pip源

pip源尽量使用阿里云的

手动修改

```
# macOS pyenv pip.conf path
~/.config/pip/pip.conf

# other
~/.pip/pip.conf

# file content
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com

```

命令行修改

```
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip config set install.trusted-host mirrors.aliyun.com
```



### 1.2：安装相关软件包

```
pip install -r requirements.txt
```

### 1.3：安装时经常出现的错误

#### 1.3.1：clang问题

```
error: command 'clang' failed with exit status 1
```

原因为：MacOS系统需要的编译器环境不存在，安装xcode即可解决

```
xcode-select --install
```

#### 1.3.2：mysqlclient问题

在macOS上安装mysqlclient包需要依赖于mysqlclient，也就是需要安装mysql客户端

解决办法：去mysql官网下载一个mysql安装包

## 二：项目创建及配置

### 2.1：创建项目

```python
项目：django-admin startproject <project_name> .
app：python manage.py startapp <app_name>
# 创建完成app，记得去settings中注册
```

### 2.2：基本配置

```python
DEBUG = True # 开发时调试

# 其他基础配置
LANGUAGE_CODE = 'zh-Hans' # 'en-us'

TIME_ZONE = 'Asia/Shanghai' # 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
```



### 2.3：配置rest_framework

settings

```python
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',      # 注册jwt认证
    'rest_framework',                # 注册rest_framework
    'rest_framework_mongoengine',    # 注册mongoengine
]

# drf config
REST_FRAMEWORK = {
    # 全局拦截器
    'EXCEPTION_HANDLER': 'utils.exceptions.exception_handler',
    # JWT token认证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 设置权限策略
    'DEFAULT_PERMISSION_CLASSES': [
        # 设置所有连接都要经过认证
        'rest_framework.permissions.IsAuthenticated',  
        'utils.permissions.CrudModelPermission'
    ],
    # 设置分页配置
    'DEFAULT_PAGINATION_CLASS': 'utils.paginations.PageNumberPagination',
    'PAGE_SIZE': 5,
}
```

### 2.4：相关工具内容

utils/exceptions.py

作用：全局拦截器，自己处理异常，为了混淆http状态码和异常信息

https://raw.githubusercontent.com/cplinux/djangoTemplate/master/utils/exceptions.py



utils/paginations.py

作用：配置分页信息

https://raw.githubusercontent.com/cplinux/djangoTemplate/master/utils/paginations.py



utils/permissions.py

作用：管理对应models的方法权限

https://raw.githubusercontent.com/cplinux/djangoTemplate/master/utils/permissions.py



### 2.5：配置JWT认证

settings中配置

```python
# jwt configure
from datetime import timedelta
SIMPLE_JWT = {
    # jwt授权的token时效
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),  
}
```

login和刷新token的url配置

```python
在下方的“路由配置”中
```





## 三：数据库配置

### 3.1：mysql

mysql在Django中可以直接在settings中配置，然后在models中去通过模型类操作mysql数据库。



1. 配置Django连接数据库: 

settings中：

```
## Django mysql configure
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mammoth',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

2. 项目中的数据库操作

```
# 创建当前应用的迁移数据文件
python manage.py makemigratios <app_name>

# 生成数据库表
python manage.py migrate

#查看迁移文件生成的SQL语句
python manage.py sqlmigrete <app_name> 0001

#根据已有的数据库表反向生成Models
python manage.py inspectdb > <app_name>/models.py
```



### 3.2：mongodb

在settings中设置相关配置

```python
# mongodb config
MONGODB_DATABASES = {
    'name': 'test',
    'host': '127.0.0.1',
    'port': 27017,
    # 'password': 'test',
    # 'username': 'test',
    'tz_aware': True,
}
```



在相关app中配置连接（相当于app开机自启动配置）

<app_name>/apps.py

```python
from django.apps import AppConfig
from django.conf import settings
from mongoengine import connect

class CmdbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cmdb'

    def ready(self):
        print('cmdb 项目加载，建立mongodb连接')
        connect(**settings.MONGODB_DATABASES)
```



## 四：路由配置

一般采用2级路由。

一级：<project_name>/urls.py，作用是app分类

二级：<app_name>/urls.py，作用是直通views

相关配置：

```python
# 一级, 通过include来引用二级路由
from django.urls import path
from django.urls import include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # login
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 刷新token时效
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('app1/', include('app1.urls')),
    path('app2/', include('app2.urls'))
]
```



```python
# 二级, 通往views的路由
from django.urls import path
from .views import Temp1ViewSet, Temp2ViewSet, Custom
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

# 使用mongoengine时
# from rest_framework_mongoengine.routers import SimpleRouter
# router = SimpleRouter()

router.register('temp1', Temp1ViewSet) # ViewSet的路由
router.register('temp2', Temp2ViewSet)

urlpatterns = [
    path('custom/', Custom) # 自定义view的路由
] + router.urls
```



