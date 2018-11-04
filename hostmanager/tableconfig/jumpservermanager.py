config = {
    'model': 'JumpServerAccountManager',
    'table': [
        {
            'name': '用户名',
            'field': 'userid__username',
        },
        {
            'name': '主机实例名',
            'field': 'serveraccount__hostid__hostinstancename',
        },
        {
            'name': '主机账号',
            'field': 'serveraccount__account',
            'merge': True,                                          # 如果该字段使用了合并且定义了editrow，则必须为多选下拉菜单；否则必须为单选下拉菜单
        },
    ],
    'operation': [
        {
            'name': '删除',
            'button_type': 'delete',                                # 指定按钮的类型，供前端获取并绑定事件
            'uri_prefix': '/jumpserveraccountmanager/delete/',      # 指定操作的API的前缀
            'edit_flag': 'id',                                      # 指定操作所依赖的ID
        },
        {
            'name': '编辑',
            'button_type': 'edit',
            'uri_prefix': '/jumpserveraccountmanager/edit/',
            'edit_flag': 'id',
        },
    ],
    'addrow': [
        {
            'name': '用户名',
            'form_name': 'user',
            'form_type': 'select',
            'model': 'SystemUser',
            'field': 'username',
        },
        {
            'name': '主机实例名',
            'form_name': 'hostinstancename',
            'form_type': 'select',
            'model': 'EteamsHost',
            'field': 'hostinstancename',
        },
        {
            'name': '主机账号',
            'form_name': 'account',
            'form_type': 'text',
        },
    ],
    'editrow':[
        {
            'name': '主机账号',
            'form_name': 'account',
            'form_type': 'multi-select',
            'datasource_extra': 'account_data_get',             # 需要自己给定下拉菜单的选项数据
        },
    ],
}



from hostmanager import models

def account_data_get(rowid_list):
    hostid = models.JumpServerAccountManager.objects.filter(id=rowid_list[0]).values('serveraccount__hostid')[0].get('serveraccount__hostid')
    return models.ServerAccount.objects.filter(hostid=hostid).values_list('id', 'account')







