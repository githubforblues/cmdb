config = {
    'model': 'ServiceDeployConfig',
    'table': [
        {
            'name': '服务名',
            'field': 'service_id__servicename',
        },
        {
            'name': '描述信息',
            'field': 'desc'
        },
        {
            'name': '镜像名称',
            'field': 'image_id__imagename',
        },
        {
            'name': '项目名称',
            'field': 'project_id__projectname',
        },
        {
            'name': '最近一次代码打包时间',
            'field': 'project_id__lastpackagetime',
        },
    ],
    'operation': [
        {
            'name': '删除',
            'button_type': 'delete',
            'uri_prefix': '/deployconfig/delete/',
            'edit_flag': 'id',
        },
        {
            'name': '编辑',
            'button_type': 'edit',
            'uri_prefix': '/deployconfig/edit/',
            'edit_flag': 'id',
        },
        {
            'name': '刷新',
            'button_type': 'refresh',
            'uri_prefix': '/deployconfig/refresh/',
            'edit_flag': 'id',
        },
    ],
    'addrow': [
        {
            'name': '服务名',
            'form_name': 'servicename',
            'form_type': 'select',
            'model': 'ServiceManager',
            'field': 'servicename',
            'datasource_extra': 'service_data_distinct_get',
        },
        {
            'name': '描述信息',
            'form_name': 'desc',
            'form_type': 'text',
        },
        {
            'name': '镜像名称',
            'form_name': 'imagename',
            'form_type': 'select',
            'model': 'ImageList',
            'field': 'imagename',
        },
        {
            'name': '项目名称',
            'form_name': 'projectname',
            'form_type': 'select',
            'model': 'ProjectPackage',
            'field': 'projectname',
        },
    ],
    'editrow':[
        {
            'name': '描述信息',
            'form_name': 'desc',
            'form_type': 'text',
        },
        {
            'name': '镜像名称',
            'form_name': 'imagename',
            'form_type': 'select',
            'model': 'ImageList',
            'field': 'imagename',
        },
        {
            'name': '项目名称',
            'form_name': 'projectname',
            'form_type': 'select',
            'model': 'ProjectPackage',
            'field': 'projectname',
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





# 1. 时间戳识别






