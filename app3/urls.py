from django.urls import path
# from .views import Temp1ViewSet, Temp2ViewSet, Custom
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

# 使用mongoengine时
# from rest_framework_mongoengine.routers import SimpleRouter
# router = SimpleRouter()

# router.register('temp1', Temp1ViewSet) # ViewSet的路由
# router.register('temp2', Temp2ViewSet)

urlpatterns = [
    # path('custom/', Custom) # 自定义view的路由
] + router.urls