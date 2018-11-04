
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


    // 基本datatables
    // -----------------------------------------------------------------
    $('#demo-dt-basic').dataTable( {
        "responsive": true,
        "language": {
            "paginate": {
              "previous": '<i class="demo-psi-arrow-left"></i>',
              "next": '<i class="demo-psi-arrow-right"></i>'
            }
        }
    } );



    // 带有单行选择功能的datatables
    // -----------------------------------------------------------------
    var rowSelection = $('#demo-dt-selection').DataTable({
        "responsive": true,
        "language": {
            "paginate": {
              "previous": '<i class="demo-psi-arrow-left"></i>',
              "next": '<i class="demo-psi-arrow-right"></i>'
            }
        }
    });

    $('#demo-dt-selection').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            rowSelection.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );



    // 带有多行选择和选中删除功能的datatables（可用于制作多选删除功能）
    // -----------------------------------------------------------------
    var rowDeletion = $('#demo-dt-delete').DataTable({
        "responsive": true,
        "language": {
            "paginate": {
              "previous": '<i class="demo-psi-arrow-left"></i>',
              "next": '<i class="demo-psi-arrow-right"></i>'
            }
        },
        "dom": '<"toolbar">frtip'
    });
    $('#demo-custom-toolbar').appendTo($("div.toolbar"));

    $('#demo-dt-delete tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
    } );

    $('#demo-dt-delete-btn').click( function () {
        rowDeletion.row('.selected').remove().draw( false );
    } );



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

    $('#demo-dt-addrow-btn').on( 'click', addrow_button_click );

    $('#demo-dt-addrow').find('a').each(function () {
        if($(this).attr('button_type') == 'edit'){
            $(this).on('click', editrow_button_click);
        }
    })
});




// 修改数据相关功能的函数
// -----------------------------------------------------------------

// 为每个数据行的编辑按钮绑定事件
function editrow_button_click() {

    editrow_form = $('#dt-editrow-form');
    if (editrow_form.children().length == 0) {
        return;             // 其他行正在使用编辑模式，没有可用的表单标签，则点击编辑按钮无效
    }

    // 初始化表单内的数据
    // init_editform_data('#dt-editrow-form');

    var row_tr = $(this).parent().parent();
    var thead_th = $('#demo-dt-addrow').find('th');

    init_editform_format(editrow_form.children(), thead_th, row_tr.children());

    $(this).parent().children().hide();

    save_button = $('<a class="btn btn-warning btn-xs">保存</a>');        // 创建一个保存按钮
    $(this).before(save_button);
    // uri = $(this).attr('uri');            // 从原来的按钮中获取保存编辑内容的API
    uri = '/hostgroupadd/';                  // 暂时写死

    save_button_click_bind(row_tr, uri);     // 绑定事件的函数中不能嵌套其他绑定事件，所以save_button.on()不能直接在这里写，否则保存按钮的点击事件会在点击编辑按钮时触发
}

// 把编辑模式的标签替换到表格中
function init_editform_format(formArr, thArr, trArr) {
    formArr.each(function () {
        if($(this).prop('tagName') == 'INPUT'){
            labelstr = $(this).attr('label');
            that = $(this);
            for(i=0; i<=thArr.length-1; i++){
                if(thArr.eq(i).text() == labelstr){
                    tr_text = trArr.eq(i).text();
                    trArr.eq(i).html(that);
                    that.val(tr_text);
                }
            }

        } else if($(this).prop('tagName') == 'SELECT'){
            labelstr = $(this).attr('label');
            that = $(this);
            for(i=0; i<=thArr.length-1; i++){
                if(thArr.eq(i).text() == labelstr){
                    selectid = trArr.eq(i).attr('edit_id');        // 编辑模式下的下拉菜单需要value是id，不能是字符串
                    trArr.eq(i).text('');
                    div = that.next();
                    div.appendTo(trArr.eq(i));
                    div.before(that);
                    that.val(selectid);
                    that.trigger('chosen:updated');                // chosen组件给定value值后要手动更新
                }
            }
        }
    })
}

// 保存按钮的点击事件
function save_button_click_bind(row_tr) {
    save_button.on('click', function () {

        data = {};

        row_tr.find('input').each(function () {
            if ($(this).attr('name')) {
                data[$(this).attr('label')] = $(this).val();
            }
        });
        row_tr.find('select').each(function () {
            data[$(this).attr('label')] = $(this).val();
        });
        uri = $(this).attr('uri') + $(this).attr('row_id');

        console.log(JSON.stringify(data));
        ajax_data_send(JSON.stringify(data), uri, form_elements_return);
    } );
}

// 归还所有表单标签(现在因为刷新了页面，所以不归还也没有问题)
function form_elements_return() {
    console.log('a');
}




// 新增数据相关功能的函数
// -----------------------------------------------------------------

// 添加按钮的点击事件
function addrow_button_click() {
    // 初始化表单标签的层次关系
    init_addform_format('#dt-addrow-addform-hide > form');

    // 显示表单
    $('#dt-addrow-addform-hide').show();

    // 添加按钮转变成提交按钮
    addbutton_switch_to_submitbutton($(this));

    // 为提交按钮绑定事件
    $('#dt-submit-btn').on( 'click', function () {
        var submitto = $('#dt-addrow-addform-hide > form').attr('submitto');

        // 收集表单数据并发送给后台
        submitdata(submitto);
    })
}

// 初始化表单标签的层次关系
function init_addform_format(jqfilterrule) {
    $(jqfilterrule).children().each(function () {
        if ($(this).prop('tagName') == 'INPUT') {
            element_input_change($(this));
        } else if ($(this).prop('tagName') == 'SELECT' && ! $(this).attr('multiple')) {
            element_select_change($(this));
        } else if ($(this).prop('tagName') == 'SELECT' && $(this).attr('multiple')) {
            element_multipleselect_change($(this));
        }
    });
}

// 为input标签应用样式
function element_input_change(obj) {
    var labelname = obj.attr("label");

    var div1 = $("<div class='form-group'></div>");
    var label = $("<label class=\"col-md-3 control-label\"></label>").text(labelname);
    var div2 = $("<div class='col-md-6'></div>");

    obj.before(div1);
    label.appendTo(div1);
    label.after(div2);
    obj.appendTo(div2);
    obj.addClass("form-control");
}

// 为单选select标签应用样式
function element_select_change(obj) {
    var labelname = obj.attr("label");

    var div1 = $("<div class='form-group'></div>");
    var label = $("<label class=\"col-md-3 control-label\"></label>").text(labelname);
    var div2 = $("<div class='col-md-6'></div>");

    obj.before(div1);
    label.appendTo(div1);
    label.after(div2);
    chosen_select_div = obj.next('div');
    chosen_select_div.appendTo(div2);
    chosen_select_div.before(obj);
    obj.addClass("form-control");
}

// 为多选select标签应用样式
function element_multipleselect_change(obj) {
    var labelname = obj.attr("label");

    var div1 = $("<div class='form-group'></div>");
    var label = $("<label class=\"col-md-3 control-label\"></label>").text(labelname);
    var div2 = $("<div class='col-md-6'></div>");

    obj.before(div1);
    label.appendTo(div1);
    label.after(div2);
    chosen_select_multi_div = obj.next('div');
    chosen_select_multi_div.appendTo(div2);
    chosen_select_multi_div.before(obj);
    obj.addClass("form-control");
}

// 更改添加按钮的文本和ID
function addbutton_switch_to_submitbutton(obj) {
    obj.html('<i class="demo-pli-plus"></i> Submit');
    obj.attr('id', 'dt-submit-btn');
}

// 收集表单数据并发送给后台
function submitdata(submitto) {
    data = {};

    $('#dt-addrow-addform-hide > form').find('input').each(function () {
        if ($(this).attr('name')) {
            data[$(this).attr('label')] = $(this).val();
            $(this).val('');
        }
    });
    $('#dt-addrow-addform-hide > form').find('select').each(function () {
        data[$(this).attr('label')] = $(this).val();
        $(this).val('');
        $(this).trigger("chosen:updated");      // chosen组件设置完value属性后需要手动update
    });

    console.log(JSON.stringify(data));
    ajax_data_send(JSON.stringify(data), submitto, submitbutton_switch_to_addbutton);
}

// 更改提交按钮的文本和ID
function submitbutton_switch_to_addbutton() {
    $('#dt-submit-btn').off('click');       // 提交按钮解绑事件
    $('#dt-submit-btn').attr('id', 'demo-dt-addrow-btn');
    $('#dt-submit-btn').html('');
    $('#demo-dt-addrow-btn').html('<i class="demo-pli-plus"></i> Add Row');
    $('#demo-dt-addrow-btn').on('click', addrow_button_click);      // 为添加按钮重新绑定点击事件
    $('#dt-addrow-addform-hide').hide();            // 隐藏新增表单
}




// 公共函数
// -----------------------------------------------------------------

// ajax发送数据给后台
function ajax_data_send(data, submitto, success_callback) {
   $.ajax({
       url: submitto,
       data: data,
       type: "POST",
       success:function(){
           console.log('发送成功');
           success_callback();
           window.location.reload();    // 除了直接刷新页面，也可以通过datatables的API直接添加数据到表格中
       }
   })
}





