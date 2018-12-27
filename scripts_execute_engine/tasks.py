from __future__ import absolute_import, unicode_literals
from celery import shared_task

import json
import time

@shared_task            # 表示多个APP下的任务可以互相共享
def add(x, y):
    return x + y

@shared_task
def mul(x, y):
    return x * y

@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def deploy(data):
    try:
        data = json.loads(data)
        for item in data:
            for i in range(item[4]):
                print('发布' + item[0] + '服务')
                time.sleep(1)
        return 0

    except Exception as e:
        print(e)
        return 1

