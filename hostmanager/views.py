from django.shortcuts import render, redirect, HttpResponse
from django import views
from hostmanager import models
from django.utils.decorators import method_decorator
from hostmanager import forms
from .tableconfig import servicemanager
from .tableconfig import hostgroupmanager
from .tableconfig import autodeploy
from .tableconfig import deployconfig
from .utils import configanalysis, dataget
from json import dumps, loads
from django.db.models import Q


# ------------------------------------------------- #

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
        result = [ models.ServiceManager.objects.filter(id=rowid).delete() for rowid in rowlist ]           # 删除功能暂时关闭
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
            data = {'number':item['容器数量'], 'inhost':item['服务所在节点'], 'desc':item['描述信息']}
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
            data = {'servicename':item['服务名'], 'number':item['容器数量'], 'inhost_id':item['服务所在节点'], 'desc':item['描述信息']}
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

# 发布
class AD(views.View):
    @method_decorator(auth_check)
    def get(self, request, *args, **kwargs):
        msg = {}
        user = request.session.get('user', '游客')
        msg.update({'user': user})

        thead_list, quertset, editformobj, addformobj = configanalysis.configanalysis(autodeploy.config)

        return render(request, 'autodeploy.html', {'msg': msg, 'thead_list': thead_list, 'oadd': addformobj, 'oedit': editformobj, 'hg':quertset})

# 发布，条目删除
class ADdelete(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        data = request.POST.get('rowid', None)
        rowlist = data.split(',')
        result = [ models.ServiceDeployStatus.objects.filter(id=rowid).delete() for rowid in rowlist ]           # 删除功能暂时关闭
        return HttpResponse('success')

# 发布，更改保存
class ADedit(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        for item in request.POST :          # 如果传递的ajax数据为内嵌列表的字典，就必须要这样处理
            item = loads(item)
            models.ServiceDeployStatus.objects.filter(id=item['rowid']).update(desc=item['描述信息'])
        return HttpResponse('success')

# 发布，菜单初始化数据获取
class ADdatainit(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        rowid = request.POST.get('rowid')
        label = request.POST.get('label')
        type = request.POST.get('type')
        data = dataget.dataget(autodeploy, type, label, rowid)
        return HttpResponse(dumps(dict(data)))

# 发布，新增数据
class ADadd(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        for item in request.POST :          # 如果传递的ajax数据为内嵌列表的字典，就必须要这样处理
            item = loads(item)
            ads = models.ServiceDeployStatus.objects.get_or_create(service_id=item['服务名'], status=False, desc=item['描述信息'])
        return HttpResponse('success')

# ------------------------------------------------- #

# 发布配置
class DC(views.View):
    @method_decorator(auth_check)
    def get(self, request, *args, **kwargs):
        msg = {}
        user = request.session.get('user', '游客')
        msg.update({'user': user})

        thead_list, quertset, editformobj, addformobj = configanalysis.configanalysis(deployconfig.config)

        return render(request, 'deployconfig.html', {'msg': msg, 'thead_list': thead_list, 'oadd': addformobj, 'oedit': editformobj, 'hg':quertset})

# 发布配置，条目删除
class DCdelete(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        data = request.POST.get('rowid', None)
        rowlist = data.split(',')
        result = [ models.ServiceDeployConfig.objects.filter(id=rowid).delete() for rowid in rowlist ]           # 删除功能暂时关闭
        return HttpResponse('success')

# 发布配置，更改保存
class DCedit(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        for item in request.POST :          # 如果传递的ajax数据为内嵌列表的字典，就必须要这样处理
            item = loads(item)
            models.ServiceDeployConfig.objects.filter(id=item['rowid']).update(desc=item['描述信息'], image_id=item['镜像名称'], project_id=item['项目名称'])
        return HttpResponse('success')

# 发布配置，菜单初始化数据获取
class DCdatainit(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        rowid = request.POST.get('rowid')
        label = request.POST.get('label')
        type = request.POST.get('type')
        data = dataget.dataget(deployconfig, type, label, rowid)
        return HttpResponse(dumps(dict(data)))

# 发布配置，新增数据
class DCadd(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        for item in request.POST :          # 如果传递的ajax数据为内嵌列表的字典，就必须要这样处理
            item = loads(item)
            ads = models.ServiceDeployConfig.objects.get_or_create(service_id=item['服务名'], image_id=item['镜像名称'], project_id=item['项目名称'], desc=item['描述信息'])
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
        result = [ models.Host2HostGroup.objects.filter(id=rowid).delete() for rowid in rowlist ]           # 删除功能暂时关闭
        return HttpResponse('success')

# 配置管理 - 主机组管理，条目编辑
class HGMedit(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        for item in request.POST :          # 如果传递的ajax数据为内嵌列表的字典，就必须要这样处理
            item = loads(item)
            hg = models.Host2HostGroup.objects.get(id=item['rowid'].split(',')[0]).hostgroupid_id
            models.Host2HostGroup.objects.filter(hostgroupid_id=hg).delete()
            for i in item['主机']:
                pass
                models.Host2HostGroup.objects.create(hostgroupid_id=hg, hostid_id=i)
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

# 配置管理 - 主机组管理，新增数据
class HGMadd(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        for item in request.POST :          # 如果传递的ajax数据为内嵌列表的字典，就必须要这样处理
            item = loads(item)
            hg = models.HostGroup.objects.get_or_create(hostgroupname=item['主机组'])
            for i in item['主机实例名']:
                models.Host2HostGroup.objects.get_or_create(hostgroupid_id=hg[0].id,hostid_id=int(i))
        return HttpResponse('success')

# ------------------------------------------------- #

# 文档库
class Doc(views.View):
    @method_decorator(auth_check)
    def get(self, request, docnumber, *args, **kwargs):
        msg = {}
        user = request.session.get('user', '游客')
        msg.update({'user': user})

        if not docnumber:
            docdir = models.DocumentDir.objects.filter()[0]
            doc = models.Documents.objects.filter(is_delete=False)[0]
            return redirect('/documents/{}-{}'.format(docdir.id, doc.id))

        docdirlist = models.DocumentDir.objects.filter()

        doc = []
        for i in docdirlist:
            doc.append([i, models.Documents.objects.filter(docdir=i, is_delete=False)])

        docview = models.Documents.objects.get(id=docnumber.split('-')[1])

        return render(request, 'document.html', {'msg': msg, 'docdirlist': docdirlist, 'doc': doc, 'docview': docview})

# 文档保存
class DocSavedata(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        doc = request.POST['doc']
        data = request.POST['data']

        models.Documents.objects.filter(id=doc).update(doc=data)

        return HttpResponse('success')

# 文档删除
class DocDeletedata(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        doc = request.POST['doc']
        models.Documents.objects.filter(id=doc).update(is_delete=True)
        return HttpResponse('success')

# 文档新增
class DocCreatedata(views.View):
    @method_decorator(auth_check)
    def post(self, request, *args, **kwargs):
        docname = request.POST['docname']
        docdirid = request.POST['docdirid']

        if docname:
            docid = models.Documents.objects.create(docname=docname, docdir_id=docdirid, auther_id='1').id
        return HttpResponse(docid)







