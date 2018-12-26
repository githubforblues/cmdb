config = {
    'model': 'ServiceDeployStatus',
    'table': [
        {
            'name': '待发布服务',
            'field': 'service_id__service_id__servicename',
        },
        {
            'name': '描述信息',
            'field': 'desc',
        },
        {
            'name': '上一次发布时间',
            'field': 'lastdeploytime',
        },
        {
            'name': '发布状态',
            'field': 'status',
        },
    ],
    'operation': [
        {
            'name': '删除',
            'button_type': 'delete',
            'uri_prefix': '/autodeploy/delete/',
            'edit_flag': 'id',
        },
        {
            'name': '编辑',
            'button_type': 'edit',
            'uri_prefix': '/autodeploy/edit/',
            'edit_flag': 'id',
        },
        {
            'name': '发布该服务',
            'button_type': 'deploy',
            'uri_prefix': '/autodeploy/deploy/',
            'edit_flag': 'id',
        },
    ],
    'addrow': [
        {
            'name': '待发布服务',
            'form_name': 'servicename',
            'form_type': 'select',
            'model': 'ServiceDeployConfig',
            'field': 'service_id__servicename',
        },
        {
            'name': '描述信息',
            'form_name': 'desc',
            'form_type': 'text',
        },
    ],
    'editrow':[
        {
            'name': '描述信息',
            'form_name': 'desc',
            'form_type': 'text',
        },
    ],
}




def service_data_distinct_get(modelobj):
    servicename = modelobj.objects.all().values_list('servicename').distinct()

    data = []
    for item in servicename:
        item = item[0]
        data.append(modelobj.objects.filter(servicename=item).values_list('id', 'servicename')[0])

    return data




