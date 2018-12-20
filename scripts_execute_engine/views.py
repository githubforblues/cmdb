from django.shortcuts import render, redirect, HttpResponse
from django import views
from hostmanager import models
from django.utils.decorators import method_decorator
from json import loads
import os
import subprocess


# 脚本存放目录
SCRIPTS_DIR = 'scripts_execute_engine/cmdb_scripts/'


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

        script_name = 'auto_deploy.py'
        out = subprocess.check_output("cd {}; python {}".format(SCRIPTS_DIR, script_name), stderr=subprocess.STDOUT, shell=True).strip()

        models.ServiceDeployStatus.objects.filter(id=rowid).update(status=True)

        return HttpResponse('success')









