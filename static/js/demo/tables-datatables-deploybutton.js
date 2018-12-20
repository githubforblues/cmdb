$(document).ready(function() {

    $('#demo-dt-addrow').find('a').each(function () {
        if ($(this).attr('button_type') == 'deploy') {                  // 为条目中的编辑按钮绑定事件
            $(this).on('click', deploy_button_click);
        }
    })

});






// 发布按钮
// -----------------------------------------------------------------

function deploy_button_click() {
    uri = $(this).attr('uri');
    data = {'rowid': $(this).attr('rowid')};
    ajax_data_send(data, uri, deploy_callback);
}

function deploy_callback() {
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







