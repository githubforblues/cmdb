from django.shortcuts import render, redirect, HttpResponse
from django import views
from hostmanager import models
from django.utils.decorators import method_decorator
import json


# 堡垒机用户认证（数据写死，仅用于测试）
class JS_auth(views.View):
    def post(self, request, *args, **kwargs):
        hostlist = [('apache1', 'centos6', 'develop'),
                    ('rabbitmq_cluster_node1', 'centos6', 'rabbbitmq_admin'),
                    ('develop_test3', 'ubuntu', 'root'), ]
        return HttpResponse(json.dumps(hostlist))

# 堡垒机获取远程主机连接信息（数据写死，仅用于测试）
class JS_accountget(views.View):
    def post(self, request, *args, **kwargs):
        account = [('192.168.0.22', '22', 'root', '123456')]
        return HttpResponse(json.dumps(account))






