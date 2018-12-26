
// Tables-DataTables.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -

$(document).ready(function() {

    // DATA TABLES
    // =================================================================
    // Require Data Tables
    // -----------------------------------------------------------------
    // http://www.datatables.net/
    // =================================================================

    $.fn.DataTable.ext.pager.numbers_length = 5;

    // 带有数据新增功能的datatables
    // -----------------------------------------------------------------
    var t = $('#demo-dt-addrow').DataTable({
        "responsive": true,
        "language": {
            "paginate": {
              "previous": '<i class="demo-psi-arrow-left"></i>',
              "next": '<i class="demo-psi-arrow-right"></i>'
            }
        },
        "dom": '<"newtoolbar">frtip'
    });

    $('#demo-custom-toolbar2').appendTo($("div.newtoolbar"));

    // $('#demo-dt-addrow-btn').on('click', addrow_button_click);

    $('#demo-dt-addrow').find('a').each(function () {
        if($(this).attr('button_type') == 'edit'){                  // 为条目中的编辑按钮绑定事件
            $(this).on('click', editrow_button_click);
        }
        else if ($(this).attr('button_type') == 'delete'){          // 为条目中的删除按钮绑定事件
            $(this).on('click', deleterow_button_click);
        }
    });

    $('#demo-dt-addrow').find('tr').each(function () {
        progress_num = $(this).find('td').eq(2).text();
        $(this).find('td').eq(2).html('<div class="progress progress-striped active"><div style="width: 0%;" class="progress-bar progress-bar-primary"></div></div>');
    })
});









// 进度条 websocket
// -----------------------------------------------------------------








// 编辑数据相关功能的函数
// -----------------------------------------------------------------

// 为每个数据行的编辑按钮绑定事件
function editrow_button_click() {
    rowid = $(this).attr('rowid');

    editrow_form = $('#dt-editrow-form');
    if (editrow_form.children().length == 0) {
        return;             // 其他行正在使用编辑模式，没有可用的表单标签，则点击编辑按钮无效
    }

    var row_tr = $(this).parent().parent();
    var thead_th = $('#demo-dt-addrow').find('th');

    init_editform(editrow_form.children(), thead_th, row_tr.children(), rowid);         // 把编辑模式的标签替换到表格中

    $(this).parent().children().hide();
    save_button = $('<a class="btn btn-warning btn-xs">保存</a>');        // 创建一个保存按钮
    $(this).before(save_button);
    uri = $(this).attr('uri');               // 从原来的按钮中获取保存编辑内容的API
    console.log(uri);

    save_button_click_bind(row_tr, rowid, uri);     // 绑定事件的函数中不能嵌套其他绑定事件，所以save_button.on()不能直接在这里写，否则保存按钮的点击事件会在点击编辑按钮时触发
}

// 把编辑模式的标签替换到表格中
function init_editform(formArr, thArr, trArr, rowid) {
    formArr.each(function () {
        if($(this).prop('tagName') == 'INPUT'){
            labelstr = $(this).attr('label');
            that = $(this);
            for(i=0; i<=thArr.length-1; i++){
                if(thArr.eq(i).text() == labelstr){
                    tr_text = trArr.eq(i).text();
                    trArr.eq(i).html(that);
                    that.val(tr_text);                             // 把原本的字符串变成文本框的值
                }
            }

        } else if($(this).prop('tagName') == 'SELECT'){
            labelstr = $(this).attr('label');
            that = $(this);
            for(i=0; i<=thArr.length-1; i++){
                if(thArr.eq(i).text() == labelstr){
                    selected_list = trArr.eq(i).html().split(',');
                    init_select_data(that, rowid, selected_list);                 // 根据rowid完成下拉菜单的数据初始化

                    trArr.eq(i).text('');
                    div = that.next();
                    div.appendTo(trArr.eq(i));
                    div.before(that);
                    that.trigger('chosen:updated');                // chosen组件给定value值后要手动更新
                }
            }
        }
    })
}

// 初始化下拉菜单数据
function init_select_data(obj, rowid) {
    arr = [obj, selected_list];
    ajax_data_send({'rowid':rowid,'label':obj.attr('label'),'type':'editrow'}, 'datainit/', datahandler, arr);     // 返回的数据有两个部分，一个是选中项，一个是所有项
}

// 处理ajax返回的下拉菜单选项数据
function datahandler(data, arr) {
    obj = arr[0];
    selected_list = arr[1];

    data = JSON.parse(data);
    for(item in data){
        oOption = $('<option value=""></option>');
        oOption.prop('value', item);
        oOption.html(data[item]);
        for(id in selected_list){
            if(data[item] == selected_list[id]){
                oOption.prop('selected', true)
            }
        }
        oOption.appendTo(obj);
    }

    obj.trigger('chosen:updated');
}

// 保存按钮的点击事件
function save_button_click_bind(row_tr, rowid, uri) {
    save_button.on('click', function () {
        data = {'rowid': rowid};

        row_tr.find('input').each(function () {
            if ($(this).attr('name')) {
                data[$(this).attr('label')] = $(this).val();
            }
        });
        row_tr.find('select').each(function () {
            data[$(this).attr('label')] = $(this).val();
        });

        ajax_data_send(JSON.stringify(data), uri, form_elements_return);
    } );
}

// 归还所有表单标签(现在因为刷新了页面，所以不归还也没有问题)
function form_elements_return(data) {
    console.log(data);
    window.location.reload();
}









// 新增数据相关功能的函数
// -----------------------------------------------------------------


// 删除数据相关功能的函数
// -----------------------------------------------------------------

// 为每个数据行的编辑按钮绑定事件
function deleterow_button_click() {
    rowid = $(this).attr('rowid');
    uri_prefix = $(this).attr('uri');

    ajax_data_send({'rowid': rowid}, uri_prefix, deletecallback)
}

// 数据发送成功后的回调函数(本来是要调用tabledata的API，但因为刷新了页面，所以不写也没有关系)
function deletecallback(result) {
    console.log(result);
    window.location.reload();
}








// 公共函数
// -----------------------------------------------------------------

// ajax发送数据给后台
function ajax_data_send(data, submitto, success_callback, arr) {
    $.ajax({
        url: submitto,
        data: data,
        type: "POST",
        success:function(result){
            success_callback(result, arr);
        }
    })
}



