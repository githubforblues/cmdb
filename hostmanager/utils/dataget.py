from hostmanager import models

def dataget(tableconfig, exterkeyname, interkeyname, rowid):
    if rowid != -1 and exterkeyname == 'editrow':
        for item in tableconfig.config[exterkeyname]:
            if item['name'] == interkeyname:
                if item.get('datasource_extra', None):
                    handler = getattr(tableconfig, item['datasource_extra'])          # 获取自定义方法
                    data = handler(rowid.split(','))
                    return data
                else:                                                                 # 如果没有自定义方法，则直接从数据库中获取数据
                    table = getattr(models, item.get('model'))
                    data = table.objects.all().values_list('id', item.get('field'))
                    return data

    elif rowid == -1 or exterkeyname == 'addrow':               # 这里有问题，暂时用or
        for item in tableconfig.config[exterkeyname]:
            if item['name'] == interkeyname:
                if item.get('datasource_extra', None):
                    pass
                else:
                    table = getattr(models, item.get('model'))
                    data = table.objects.all().values_list('id', item.get('field'))
                    return data

