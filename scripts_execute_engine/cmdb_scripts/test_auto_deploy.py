from .. import tasks
import json
from hostmanager import models
from celery.result import AsyncResult

def main(rowid):
    id = models.ServiceDeployStatus.objects.get(id=rowid).service_id
    configinfo = models.ServiceDeployConfig.objects.get(id=id)
    hostinfo = models.ServiceManager.objects.filter(servicename=configinfo.service.servicename).values_list('inhost_id__hostname', 'number')

    tmplist = [configinfo.service.servicename, configinfo.image.imagename, configinfo.project.projectname,]

    data = []
    for item in hostinfo:
        tmplist1 = tmplist[:]
        tmplist1.append(item[0]);tmplist1.append(item[1])
        data.append(tmplist1)

    res = tasks.deploy.delay(json.dumps(data))                # 同一个服务中的多个docker容器需要串行执行，灰度发布模式
    taskid = res.id

    while True:
        res = AsyncResult(id=taskid)                          # 在任务完成之前会阻塞
        print(res.get())
        if res.get() == 0:
            models.ServiceDeployStatus.objects.filter(id=rowid).update(status=False)
            print('false')
            return 0
        else:
            return 1




