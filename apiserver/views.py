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


# 自动发布，条目获取
class ADrowget(views.View):
    def get(self, request, *args, **kwargs):
        rowcount = models.ServiceDeployList.objects.count()
        if rowcount:
            row = models.ServiceDeployList.objects.values_list('id', 'service_id__service_id__service_id__servicename')[0]
            models.ServiceDeployList.objects.filter(id=row[0]).delete()
            return HttpResponse(json.dumps(row))
        else:
            return HttpResponse('empty')


# 自动发布，停止脚本
class ADscriptdelete(views.View):
    def get(self, request, *args, **kwargs):
        scriptname = request.get_full_path().split('?')[1].split('=')[1]

        models.ScriptsExecStatus.objects.filter(scriptname=scriptname).delete()
        return HttpResponse('success')






