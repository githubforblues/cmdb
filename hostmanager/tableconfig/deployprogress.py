config = {
    'model': 'ServiceDeployList',
    'table': [
        {
            'name': '服务名',
            'field': 'service_id__service_id__service_id__servicename',
        },
        {
            'name': '状态',
            'field': 'status',
        },
        {
            'name': '发布进度',
            'field': 'progress',
        },
    ],
    'operation': [
        {
            'name': '取消',
            'button_type': 'delete',
            'uri_prefix': '/deployprogress/delete/',
            'edit_flag': 'id',
        },
    ],

    'addrow': [],

    'editrow': [],
}




# 1. 时间戳识别



