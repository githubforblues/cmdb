from django.db import models


class SystemUser(models.Model):
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


class ServerAccount(models.Model):
    account = models.CharField(max_length= 64)          # 主机账号
    password = models.CharField(max_length=64, default='123456')      # 主机账号的密码（在主机编辑页面中修改）
    hostid = models.ForeignKey(EteamsHost)              # 主机ID


class JumpServerAccountManager(models.Model):
    userid = models.ForeignKey(SystemUser)              # 用户ID
    serveraccount = models.ForeignKey(ServerAccount)    # 主机账号ID


class HostGroup(models.Model):
    hostgroupname = models.CharField(max_length=64)


class Host2HostGroup(models.Model):
    hostid = models.ForeignKey(EteamsHost)
    hostgroupid = models.ForeignKey(HostGroup)


class Empty(models.Model):
    empty = models.CharField(max_length=1)

