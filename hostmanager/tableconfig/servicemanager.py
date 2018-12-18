config = {
    'model': 'ServiceManager',
    'table': [
        {
            'name': '服务名',
            'field': 'servicename',
        },
        {
            'name': '服务所在节点',
            'field': 'inhost__hostinstancename',
        },
        {
            'name': '容器数量',
            'field': 'number',
        },
        {
            'name': '描述信息',
            'field': 'desc'
        },
    ],
    'operation': [
        {
            'name': '删除',
            'button_type': 'delete',                                # 指定按钮的类型，供前端获取并绑定事件
            'uri_prefix': '/servicemanager/delete/',                # 指定操作的API
            'edit_flag': 'id',                                      # 指定操作所依赖的ID
        },
        {
            'name': '编辑',
            'button_type': 'edit',
            'uri_prefix': '/servicemanager/edit/',
            'edit_flag': 'id',
        },
    ],
    'addrow': [
        {
            'name': '服务名',
            'form_name': 'servicename',
            'form_type': 'text',
        },
        {
            'name': '服务所在节点',
            'form_name': 'hostinstancename',
            'form_type': 'select',
            'model': 'EteamsHost',
            'field': 'hostinstancename',
        },
        {
            'name': '容器数量',
            'field': 'number',
            'form_name': 'number',
            'form_type': 'text',
        },
        {
            'name': '描述信息',
            'form_name': 'desc',
            'form_type': 'text',
        },

    ],
    'editrow':[
        {
            'name': '服务所在节点',
            'form_name': 'inhost',
            'form_type': 'select',
            'model': 'EteamsHost',
            'field': 'hostinstancename',
        },
        {
            'name': '路径',
            'form_name': 'path',
            'form_type': 'text',
        },
        {
            'name': '端口号',
            'form_name': 'port',
            'form_type': 'text',
        },
        {
            'name': '描述信息',
            'form_name': 'desc',
            'form_type': 'text',
        },
    ],
}









