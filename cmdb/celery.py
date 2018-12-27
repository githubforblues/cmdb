from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmdb.settings')                # 这里文件名必须是"Django项目名.settings"
app = Celery('celery_tasks')                                                    # 指定celery任务的名称
app.config_from_object('django.conf:settings', namespace='CELERY')              # 表示celery的配置如果写到django配置文件中，必须以"CELERY_"为前缀开头
app.autodiscover_tasks()



