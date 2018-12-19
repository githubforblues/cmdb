from hostmanager import models
from django import forms

def configanalysis(config):

    # 获取表格表头
    thead_list = []
    for thead in config['table']:
        thead_list.append(thead['name'])
    if config['operation']:
        thead_list.append('操作')

    # 获取表格数据
    value_list = []
    for thead in config['table']:
        value_list.append(thead['field'])
    if config['operation']:
        value_list.append(config['operation'][0]['edit_flag'])          # 把要放到操作按钮里面的行ID也查出来
    modelname = getattr(models, config['model'])
    queryset = modelname.objects.all().values_list(*value_list)

    # 如果有字段合并功能，在这里处理
    for index, item in enumerate(config['table']):
        if item.get('merge', None):
            queryset = mergerow(index, queryset)

    # 如果有操作按钮，添加到表格数据每行的最后
    if config['operation']:
        queryset_list = []
        for row in queryset:
            row_list = []
            for field in row:
                row_list.append(field)
            row_list.append(operationbuttonhtml(config, row_list.pop(-1)))              # 行ID弹出，放到表示操作按钮的HTML中
            queryset_list.append(row_list)
    else:
        queryset_list = queryset

    # 生成编辑条目所需的djangoform
    if config['editrow']:
        autoform = {}
        for item in config['editrow']:
            if item['form_type'] == 'multi-select':
                autoform[item['form_name']] = forms.ModelMultipleChoiceField(
                    widget = forms.widgets.SelectMultiple(attrs={'label': item['name'], 'class': 'chosen-select-multi'}),
                    queryset = models.Empty.objects.all(),
                    to_field_name = 'id',)
            elif item['form_type'] == 'select':
                autoform[item['form_name']] = forms.ModelChoiceField(
                    widget=forms.widgets.Select(attrs={'label': item['name'], 'class': 'chosen-select'}),
                    queryset=models.Empty.objects.all(),
                    to_field_name='id', )
            elif item['form_type'] == 'text':
                autoform[item['form_name']] = forms.CharField(
                    max_length=100, required=True,
                    widget=forms.widgets.TextInput(attrs={'label': item['name']}))

        JSMeditForm = type('JSMeditForm', (forms.Form,), autoform)
        editformobj = JSMeditForm()

    else: editformobj = None

    # 生成添加条目所需的djangoform
    if config['addrow']:
        autoform = {}
        for item in config['addrow']:
            if item['form_type'] == 'multi-select':
                autoform[item['form_name']] = forms.ModelMultipleChoiceField(
                    widget=forms.widgets.SelectMultiple(attrs={'label': item['name'], 'class': 'chosen-select-multi'}),
                    queryset=models.Empty.objects.all(),
                    to_field_name='id', )
            elif item['form_type'] == 'select':
                autoform[item['form_name']] = forms.ModelChoiceField(
                    widget=forms.widgets.Select(attrs={'label': item['name'], 'class': 'chosen-select'}),
                    queryset=models.Empty.objects.all(),
                    to_field_name='id', )
            elif item['form_type'] == 'text':
                autoform[item['form_name']] = forms.CharField(
                    max_length=100, required=True,
                    widget=forms.widgets.TextInput(attrs={'label': item['name']}))

        JSMaddForm = type('JSMaddForm', (forms.Form,), autoform)
        addformobj = JSMaddForm()

    else:
        addformobj = None


    return thead_list, queryset_list, editformobj, addformobj




# 生成操作按钮的HTML字符串
def operationbuttonhtml(config, id):
    htmlstring = ''
    for i in config['operation']:
        button_type = i['button_type']
        if button_type == 'delete':
            cssclass = 'btn-danger'
        elif button_type == 'info':
            cssclass = 'btn-danger'
        elif button_type == 'edit':
            cssclass = 'btn-info'
        else: cssclass = 'btn-warning'
        htmlstring += '<a class="btn btn-xs {}" href="#" button_type="{}" uri="{}" rowid="{}">{}</a>'.format(cssclass, button_type, i['uri_prefix'], id, i['name'])

    return htmlstring
    # <a class="btn btn-danger btn-xs" href="#" button_type='delete' uri="/hostgroupdelete/" rowid="1">删除</a>


# 合并条目
def mergerow(index, queryset):
    tmpdata = []
    mergedata = {}

    for row in queryset:
        for idx, item in enumerate(row):
            if idx != index and idx < len(row) - 1:     # 这里减掉的1就是最后一个字段，行ID
                tmpdata.append(item)
            elif idx == index:
                mergefield = item
            elif idx == len(row) - 1:
                rowid = str(item)

        tmpstring = '``'.join(tmpdata)
        tmpdata = []

        if not mergedata.get(tmpstring, None):
            mergedata[tmpstring] = [[],[]]
            mergedata[tmpstring][0].append(mergefield)
            mergedata[tmpstring][1].append(rowid)
        else:
            mergedata[tmpstring][0].append(mergefield)
            mergedata[tmpstring][1].append(rowid)

    # print(mergedata)            # {'admin``test-apache': [['tomcat', 'root', 'devops'], [1, 2, 3]], 'zcy``test-apache': [['devops'], [4]]}

    queryset = []
    for k, v in mergedata.items():
        mergefield = ','.join(v[0])
        mergerowid = ','.join(v[1])
        row = list(k.split('``'))
        row.insert(index, mergefield)
        row.append(mergerowid)
        queryset.append(row)

    # print(queryset)             # [['zcy', 'test-apache', 'devops', '4'], ['admin', 'test-apache', 'tomcat,root,devops', '1,2,3']]

    return queryset








# 用于编辑和增加条目的djangoform的示例

# class HostGroupEditForm(forms.Form):
#     hostname = forms.CharField(
#         max_length=100, required = False,
#         widget=forms.widgets.TextInput(attrs={'label': '实例名'})
#     )

#     action = forms.ModelMultipleChoiceField(
#         queryset = models.HostAction.objects.all(),
#         to_field_name = 'id',
#         widget = forms.widgets.SelectMultiple(attrs={'label': '权限类型', 'class': 'chosen-select-multi'})
#     )

#     hostgroup = forms.ModelChoiceField(
#         queryset=models.HostGroup.objects.all(),
#         to_field_name = 'id',
#         widget = forms.widgets.Select(attrs={'label': '所属组', 'class': 'chosen-select'})
#     )





