from django.shortcuts import render, redirect, HttpResponse
from django import views
from hostmanager import models
from django.utils.decorators import method_decorator
from json import loads
import os
import subprocess

from scripts_execute_engine.cmdb_scripts import test_auto_deploy



# 登陆验证装饰器
def auth_check(func):
    def inner(request, *args, **kwargs):
        is_auth = request.session.get('is_auth', False)
        if not is_auth:
            request.session['redirect_target'] = request.path
            return redirect("/login")
        else:
            return func(request, *args, **kwargs)
    return inner


# 自动发布脚本执行
class autodeploy(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        rowid = request.POST['rowid']

        status = models.ServiceDeployStatus.objects.get(id=rowid).status
        if status:
            pass
        else:
            models.ServiceDeployStatus.objects.filter(id=rowid).update(status=True)
            models.ServiceDeployList.objects.create(service_id=rowid, status='wait', progress=0)

            # 调用脚本开始发布
            # auto_deploy.main()
            test_auto_deploy.main(rowid)

        return HttpResponse('success')


# 镜像列表和项目打包列表刷新
class deployconfigrefresh(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        script_name = 'deploy_config_refresh.py'
        # out = subprocess.check_output("cd {}; python {};".format(SCRIPTS_DIR, script_name), stderr=subprocess.STDOUT, shell=True).strip()

        return HttpResponse('success')




