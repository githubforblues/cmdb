config = {
    'model': 'Host2HostGroup',
    'table': [
        {
            'name': '主机组',
            'field': 'hostgroupid__hostgroupname',
        },
        {
            'name': '主机',
            'field': 'hostid__hostinstancename',
            'merge': True,                                          # 如果该字段使用了合并且定义了editrow，则必须为多选下拉菜单；否则必须为单选下拉菜单
        },
    ],
    'operation': [
        {
            'name': '删除',
            'button_type': 'delete',                                # 指定按钮的类型，供前端获取并绑定事件
            'uri_prefix': '/configmanager/delete/',                 # 指定操作的API的前缀
            'edit_flag': 'id',                                      # 指定操作所依赖的ID
        },
        {
            'name': '编辑',
            'button_type': 'edit',
            'uri_prefix': '/configmanager/edit/',
            'edit_flag': 'id',
        },
    ],
    'addrow': [
        {
            'name': '主机实例名',
            'form_name': 'host',
            'form_type': 'multi-select',
            'model': 'EteamsHost',
            'field': 'hostinstancename',
        },
        {
            'name': '主机组',
            'form_name': 'hostgroup',
            'form_type': 'text',
        },
    ],
    'editrow':[
        {
            'name': '主机',
            'form_name': 'host',
            'form_type': 'multi-select',
            'model': 'EteamsHost',
            'field': 'hostinstancename',
        },
    ],
}






