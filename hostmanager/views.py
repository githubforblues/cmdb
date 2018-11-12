from django.shortcuts import render, redirect, HttpResponse
from django import views
from hostmanager import models
from django.utils.decorators import method_decorator
from hostmanager import forms
from .tableconfig import servicemanager
from .tableconfig import hostgroupmanager
from .utils import configanalysis, dataget
from json import dumps, loads
from django.db.models import Q


# 用户登录
class Login(views.View):
    def get(self, request, *args, **kwargs):
        is_auth = request.session.get('is_auth', False)
        if is_auth:
            return redirect('/index')
        else:
            return render(request, "login.html", {'msg': ''})

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

        auth_data = {'username': username, 'password': password}
        auth_result = models.SystemUser.objects.filter(**auth_data).exists()

        if auth_result:
            request.session['is_auth'] = True
            request.session['user'] = username
            redirect_target = request.session.get('redirect_target', None)
            if redirect_target:
                return redirect(redirect_target)
            else:
                return redirect('/index')
        else:
            return render(request, "login.html", {'msg': '用户名或密码输入错误'})

# 用户注销
class Logout(views.View):
    def get(self, request, *args, **kwargs):
        request.session.clear()
        return redirect('/login')

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

# ------------------------------------------------- #

# 主页
class Index(views.View):
    @method_decorator(auth_check)
    def get(self, request, *args, **kwargs):
        user = request.session.get('user', '游客')
        msg = {'user': user}
        return render(request, 'index.html', {'msg': msg})

# 主机列表
class HostList(views.View):
    @method_decorator(auth_check)
    def get(self, request, *args, **kwargs):
        msg = {}
        user = request.session.get('user', '游客')
        msg.update({'user': user})

        allhost = models.EteamsHost.objects.all()
        msg.update({'allhost': allhost})

        return render(request, 'hostlist.html', {'msg': msg})

# 主机编辑
class HostEdit(views.View):
    @method_decorator(auth_check)
    def get(self, request, *args, hostname=None, **kwargs):
        msg = {}
        user = request.session.get('user', '游客')
        msg.update({'user': user})
        is_admin = models.SystemUser.objects.filter(username=user).values('is_admin')[0].get('is_admin')
        msg.update({'is_admin':is_admin})     # 如果是管理员，则在主机编辑页面内可以看到删除按钮

        host = models.EteamsHost.objects.filter(hostname=hostname)[0]
        if not host:
            return HttpResponse("<h1>error, host not found</h1>")
        else:
            row_dict = {
                'hostinstancename':host.hostinstancename,
                'hostname':host.hostname,
                'hostname_hide':host.hostname,
                'hostipaddr':host.hostipaddr,
                'hosttype':host.hosttype,
                'hostdesc':host.hostdesc,
                'hoststatus':host.hoststatus,
            }
            obj = forms.HostForm(initial=row_dict)          # 初始化编辑页面
            return render(request, "hostedit.html", {'msg':msg, 'oo':obj})

    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        msg = {}
        user = request.session.get('user', '游客')
        msg.update({'user': user})

        obj = forms.HostForm(request.POST)
        if obj.is_valid():
            value_dict = obj.clean()
            hostname = value_dict['hostname_hide']
            value_dict.pop('hostname')
            value_dict.pop('hostname_hide')
            value_dict.update({'hostname':hostname})        # 把hostname_hide中的主机名替换到hostname字段中
            models.EteamsHost.objects.filter(hostname=hostname).update(**value_dict)
            return redirect('/hostlist')
        else:
            print(obj.errors)
            return render(request, 'hostedit.html', {'msg':msg, 'oo':obj})

# ------------------------------------------------- #

# 服务管理
class SM(views.View):
    @method_decorator(auth_check)
    def get(self, request, *args, **kwargs):
        msg = {}
        user = request.session.get('user', '游客')
        msg.update({'user': user})

        thead_list, quertset, editformobj, addformobj = configanalysis.configanalysis(servicemanager.config)

        return render(request, 'servicemanager.html', {'msg': msg, 'thead_list': thead_list, 'oadd': addformobj, 'oedit': editformobj, 'hg':quertset})

# 服务管理，条目删除
class SMdelete(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        data = request.POST.get('rowid', None)
        rowlist = data.split(',')
        # result = [ models.ServiceManager.objects.filter(id=rowid).delete() for rowid in rowlist ]           // 删除功能暂时关闭
        return HttpResponse('success')

# 服务管理，更改保存
class SMedit(views.View):
    @method_decorator(auth_check)
    # def post(self, request, *args, **kwargs):
    #     for item in request.POST :          # 如果传递的ajax数据为内嵌列表的字典，就必须要这样处理
    #         item = loads(item)
    #         row_id = item.get('rowid').split(',')[0]         # 在合并数据中，行ID用于查询用户名和主机名，所以只要第一个即可
    #         account_list = item.get('主机账号')
    #
    #     querydata = models.JumpServerAccountManager.objects.filter(id=row_id).values('userid', 'serveraccount__hostid')[0]
    #     userid = querydata.get('userid')
    #     hostid = querydata.get('serveraccount__hostid')
    #
    #     ServerAccountID_quertset = models.ServerAccount.objects.filter(hostid=hostid).values('id')          # 先查出某个主机的所有账号
    #     ServerAccountID_list = []
    #     [ ServerAccountID_list.append(item.get('id')) for item in ServerAccountID_quertset ]
    #
    #     models.JumpServerAccountManager.objects.filter(Q(userid=userid), Q(serveraccount__in=ServerAccountID_list)).delete()            # 查出某个用户所具有的某个主机的账号，全部删除
    #     [ models.JumpServerAccountManager.objects.create(userid_id=userid, serveraccount_id=account) for account in account_list ]      # 根据下拉菜单的选择项，给用户增加新账号
    #     return HttpResponse('success')

    def post(self, request, *args, **kwargs):
        for item in request.POST:
            item = loads(item)
            data = {'path':item['路径'], 'port':item['端口号'], 'inhost':item['服务所在节点'], 'desc':item['描述信息']}
            models.ServiceManager.objects.filter(id=item['rowid']).update(**data)
        return HttpResponse('success')

# 服务管理，菜单初始化数据获取
class SMdatainit(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        rowid = request.POST.get('rowid')
        label = request.POST.get('label')
        type = request.POST.get('type')
        data = dataget.dataget(servicemanager, type, label, rowid)
        return HttpResponse(dumps(dict(data)))

# 服务管理，新增数据
class SMadd(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        for item in request.POST :          # 如果传递的ajax数据为内嵌列表的字典，就必须要这样处理
            item = loads(item)
            data = {'servicename':item['服务名'], 'path':item['路径'], 'port':item['端口号'], 'inhost_id':item['服务所在节点'], 'desc':item['描述信息']}
            models.ServiceManager.objects.create(**data)
        # account = models.ServerAccount.objects.filter(hostid_id=item.get('主机实例名'), account=item.get('主机账号'))
        # if not account :
        #     print('create1')
        #     account = models.ServerAccount.objects.create(hostid_id=item.get('主机实例名'), account=item.get('主机账号'))        # 如果要添加的账号已经存在，则获取；没有则创建
        # else:
        #     account = account[0]
        #
        # jamrow = models.JumpServerAccountManager.objects.filter(userid_id=item.get('用户名'), serveraccount_id=account.id)
        # if not jamrow:
        #     models.JumpServerAccountManager.objects.create(userid_id=item.get('用户名'), serveraccount_id=account.id)

        return HttpResponse('success')

# ------------------------------------------------- #

# 配置管理 - 主机组管理
class HGM(views.View):
    @method_decorator(auth_check)
    def get(self, request, *args, **kwargs):
        msg = {}
        user = request.session.get('user', '游客')
        msg.update({'user': user})

        thead_list, quertset, editformobj, addformobj = configanalysis.configanalysis(hostgroupmanager.config)

        return render(request, 'hostgroupmanager.html', {'msg': msg, 'thead_list': thead_list, 'oadd': addformobj, 'oedit': editformobj, 'hg':quertset})

# 配置管理 - 主机组管理，条目删除
class HGMdelete(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        data = request.POST.get('rowid', None)
        rowlist = data.split(',')
        # result = [ models.JumpServerAccountManager.objects.filter(id=rowid).delete() for rowid in rowlist ]           // 删除功能暂时关闭
        return HttpResponse('success')

class HGMedit(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        return HttpResponse('success')

# 配管管理，菜单初始化数据获取
class HGMdatainit(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        rowid = request.POST.get('rowid')
        label = request.POST.get('label')
        type = request.POST.get('type')
        data = dataget.dataget(hostgroupmanager, type, label, rowid)
        return HttpResponse(dumps(dict(data)))

class HGMadd(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        return HttpResponse('success')










