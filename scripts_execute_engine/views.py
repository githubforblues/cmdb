from django.shortcuts import render, redirect, HttpResponse
from django import views
from hostmanager import models
from django.utils.decorators import method_decorator
from json import loads
import os

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

        # 将发布配置中的状态更改为"正在发布"
        models.ServiceDeployStatus.objects.filter(id=rowid).update(status=True)

        # 在发布列表中新增条目
        models.ServiceDeployList.objects.create(service_id=rowid, status='wait', progress=0)

        # 调用脚本开始发布
        # script_name = 'auto_deploy.py'
        script_name = 'test_auto_deploy.py'

        try:
            models.ScriptsExecStatus.objects.get(scriptname=script_name, status=1)
        except:
            models.ScriptsExecStatus.objects.filter(scriptname=script_name).update(status=1)
            models.ScriptsExecStatus.objects.get_or_create(scriptname=script_name, status=1)

            test_auto_deploy.main()
        else:
            pass

        return HttpResponse('success')


# 镜像列表和项目打包列表刷新
class deployconfigrefresh(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        script_name = 'deploy_config_refresh.py'
        out = subprocess.check_output("cd {}; python {};".format(SCRIPTS_DIR, script_name), stderr=subprocess.STDOUT, shell=True).strip()

        return HttpResponse('success')




