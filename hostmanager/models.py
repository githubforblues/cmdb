from django.db import models


class SystemUser(models.Model):                         # 用户表
    username = models.CharField(max_length = 64)        # 用户名
    password = models.CharField(max_length = 64)        # 密码
    is_admin = models.BooleanField(default = True)      # 是否管理员


class EteamsHost(models.Model):
    hostinstancename = models.CharField(max_length=100)               # 主机实例名，可以重复
    hostname = models.CharField(max_length=100, unique=True)          # 主机名
    hostipaddr = models.CharField(max_length=100)                     # 主机IP地址
    hosttype = models.IntegerField()                                  # 资产类型 1=物理机 2=ECS云服务器 3=KVM虚拟机
    hostdesc = models.CharField(max_length=500, null=True)            # 描述
    hoststatus = models.IntegerField()                                # 状态 1=上线 2=下线

    def __str__(self):
        return self.hostinstancename


# class ServerAccount(models.Model):
#     account = models.CharField(max_length= 64)          # 主机账号
#     password = models.CharField(max_length=64, default='123456')      # 主机账号的密码（在主机编辑页面中修改）
#     hostid = models.ForeignKey(EteamsHost)              # 主机ID
#
#
# class JumpServerAccountManager(models.Model):
#     userid = models.ForeignKey(SystemUser)              # 用户ID
#     serveraccount = models.ForeignKey(ServerAccount)    # 主机账号ID


class HostGroup(models.Model):                            # 主机组表
    hostgroupname = models.CharField(max_length=64)


class Host2HostGroup(models.Model):                       # 主机&主机组关系表
    hostid = models.ForeignKey(EteamsHost)
    hostgroupid = models.ForeignKey(HostGroup)


class Empty(models.Model):                                # 空表，用于条目编辑和条目新增的可选项填充
    empty = models.CharField(max_length=1)


class ServiceManager(models.Model):                       # 服务管理表
    servicename = models.CharField(max_length=64)
    port = models.CharField(max_length=64)
    path = models.CharField(max_length=64)
    number = models.IntegerField(default=0)
    desc = models.CharField(max_length=64)
    inhost = models.ForeignKey(EteamsHost)


class DocumentDir(models.Model):                          # 文档目录表
    dirname = models.CharField(max_length=256)


class Documents(models.Model):                            # 文档表
    docname = models.CharField(max_length=256)
    doc = models.TextField(max_length=4096)
    is_delete = models.BooleanField(default=False)        # 文档状态，false未删除，true已删除

    auther = models.ForeignKey(SystemUser)
    docdir = models.ForeignKey(DocumentDir)


class ServiceDeployStatus(models.Model):
    desc = models.CharField(max_length=256)
    status = models.BooleanField(default=True)            # 当前发布状态（系统异常时，需要人工介入处理该值的不正确情况）
    lastdeploytime = models.DateTimeField(null=True)      # 最近一次发布时间

    service = models.ForeignKey(ServiceManager)



