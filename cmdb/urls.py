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

urlpatterns = [
    url(r'^$', views.Login.as_view()),
    url(r'^login/', views.Login.as_view()),
    url(r'^logout/', views.Logout.as_view()),

    url(r'^index/', views.Index.as_view()),
    url(r'^hostlist/', views.HostList.as_view()),
    url(r'^hostedit_(?P<hostname>.*)/', views.HostEdit.as_view()),
    url(r'^hostedit/', views.HostEdit.as_view()),

    url(r'^servicemanager/delete/', views.SMdelete.as_view()),
    url(r'^servicemanager/edit/', views.SMedit.as_view()),
    url(r'^servicemanager/datainit/', views.SMdatainit.as_view()),
    url(r'^servicemanager/add/', views.SMadd.as_view()),
    url(r'^servicemanager/', views.SM.as_view()),

    url(r'^hostgroupmanager/delete/', views.HGMdelete.as_view()),
    url(r'^hostgroupmanager/edit/', views.HGMedit.as_view()),
    url(r'^hostgroupmanager/datainit/', views.HGMdatainit.as_view()),
    url(r'^hostgroupmanager/add/', views.HGMadd.as_view()),
    url(r'^hostgroupmanager/', views.HGM.as_view()),

    url(r'^documents/savedata/', views.DocSavedata.as_view()),
    url(r'^documents/(?P<docnumber>.*)', views.Doc.as_view()),

    url(r'^api/jumpserver/auth/', api_views.JS_auth.as_view()),
    url(r'^api/jumpserver/accountget/', api_views.JS_accountget.as_view()),

    url(r'^admin/', admin.site.urls),
]



