"""cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from hostmanager import views
from apiserver import views as api_views
from scripts_execute_engine import views as scripts_views

urlpatterns = [

    url(r'^$', views.Login.as_view()),

    # 登陆
    url(r'^login/', views.Login.as_view()),
    url(r'^logout/', views.Logout.as_view()),

    # 总览
    url(r'^index/', views.Index.as_view()),

    # 主机管理
    url(r'^hostlist/', views.HostList.as_view()),
    url(r'^hostedit_(?P<hostname>.*)/', views.HostEdit.as_view()),
    url(r'^hostedit/', views.HostEdit.as_view()),

    # 自动发布，脚本执行接口
    url(r'^autodeploy/deploy/', scripts_views.autodeploy.as_view()),

    # 自动发布
    url(r'^autodeploy/delete/', views.ADdelete.as_view()),
    url(r'^autodeploy/edit/', views.ADedit.as_view()),
    url(r'^autodeploy/datainit/', views.ADdatainit.as_view()),
    url(r'^autodeploy/add/', views.ADadd.as_view()),
    url(r'^autodeploy/', views.AD.as_view()),

    # 发布配置，刷新，脚本执行接口https://blog.csdn.net/weixin_38956287/article/details/80423607
    url(r'^deployconfig/refresh/', scripts_views.deployconfigrefresh.as_view()),

    # 发布配置
    url(r'^deployconfig/delete/', views.DCdelete.as_view()),
    url(r'^deployconfig/edit/', views.DCedit.as_view()),
    url(r'^deployconfig/datainit/', views.DCdatainit.as_view()),
    url(r'^deployconfig/add/', views.DCadd.as_view()),
    url(r'^deployconfig/', views.DC.as_view()),

    # 发布进度
    url(r'^deployprogress/delete/', views.DPdelete.as_view()),
    url(r'^deployprogress/edit/', views.DPedit.as_view()),
    url(r'^deployprogress/datainit/', views.DPdatainit.as_view()),
    url(r'^deployprogress/add/', views.DPadd.as_view()),
    url(r'^deployprogress/', views.DP.as_view()),

    # 服务管理
    url(r'^servicemanager/delete/', views.SMdelete.as_view()),
    url(r'^servicemanager/edit/', views.SMedit.as_view()),
    url(r'^servicemanager/datainit/', views.SMdatainit.as_view()),
    url(r'^servicemanager/add/', views.SMadd.as_view()),
    url(r'^servicemanager/', views.SM.as_view()),

    # 主机组管理
    url(r'^hostgroupmanager/delete/', views.HGMdelete.as_view()),
    url(r'^hostgroupmanager/edit/', views.HGMedit.as_view()),
    url(r'^hostgroupmanager/datainit/', views.HGMdatainit.as_view()),
    url(r'^hostgroupmanager/add/', views.HGMadd.as_view()),
    url(r'^hostgroupmanager/', views.HGM.as_view()),

    # 文档库
    url(r'^documents/savedata/', views.DocSavedata.as_view()),
    url(r'^documents/deletedata/', views.DocDeletedata.as_view()),
    url(r'^documents/createdata/', views.DocCreatedata.as_view()),
    url(r'^documents/(?P<docnumber>.*)', views.Doc.as_view()),

    # 堡垒机API
    url(r'^api/jumpserver/auth/', api_views.JS_auth.as_view()),
    url(r'^api/jumpserver/accountget/', api_views.JS_accountget.as_view()),


    # url(r'^admin/', admin.site.urls),
]








