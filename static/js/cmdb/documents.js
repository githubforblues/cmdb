$(document).ready(function() {

    // 初始化显示状态
    uri = window.location.href;
    len = uri.split('/').length;
    docnumber = uri.split('/')[len-1];
    docnumber_dir = docnumber.split('-')[0];
    docnumber_doc = docnumber.split('-')[1];

    $('.docdirbox ul li a').each(function () {
        if ($(this).attr('id') == docnumber_dir) {
            $(this).parent().addClass('doc-dir-active');
        }
    });

    $('.docbox ul').each(function () {
        if ($(this).attr('id') == docnumber_dir) {
            $(this).css('display', 'block');

            $(this).find('a').each(function () {
                if ($(this).attr('id') == docnumber_doc) {
                    $(this).parent().addClass('doc-active');
                }
            })
        }
    });


    // 点击不同目录切换显示文件列表
    $('.docdirbox ul li a').each(function () {
        $(this).on('click', function () {
            $(this).parent().parent().children().each(function () {
                $(this).removeClass('doc-dir-active');
            });

            $(this).parent().addClass('doc-dir-active');

            docnumber_dir = $(this).attr('id');

            docdir_id = $(this).attr('id');
            $('.docbox ul').each(function () {
               if ($(this).attr('id') == docdir_id) {
                   $(this).css('display', 'block')
               }
               else {
                   $(this).css('display', 'none')
               }
            });
        })
    });


    // 保存功能
    $('#savebuttom').on('click', function () {
        data = {'doc': docnumber_doc, 'data': $('textarea').val()};
        ajax_data_send(data, '/documents/savedata/', after_save_data)
    });


    // 删除功能
    $('#deletebuttom').on('click', function () {
        docnumber_doc = docnumber.split('-')[1];
        data = {'doc': docnumber_doc};
        alert('确认删除');
        ajax_data_send(data, '/documents/deletedata/', after_delete_data)
    });


    // 新建功能
    $('#createbuttom').on('click', function () {
        $('#creatediv').prependTo('body');
        $('#creatediv').css('display','block');
        $('#creatediv').css('left', $(window).width()/2-$('#creatediv').width()/2);
        $('#creatediv').css('top', '150px');

        $('#creatediv_mask').prependTo('body');
        $('#creatediv_mask').css('display','block');
        $('#creatediv_mask').css('width', $(window).width());
        $('#creatediv_mask').css('height', $(window).height());

        $('#creatediv_mask').on('click', function () {
            $(this).css('display', 'none');
            $('#creatediv').css('display', 'none');
        })
    });

    $('#creatediv button').on('click', function () {
        docnumber = $(this).prev().val();
        data = {'docname': docnumber, 'docdirid': docnumber_dir};
        ajax_data_send(data, '/documents/createdata/', after_create_data)
    })

});



function after_save_data() {
    window.location.reload();
}

function after_create_data(result) {
    window.location.replace('/documents/'+docnumber_dir+'-'+result);
}

function after_delete_data() {
    window.location.replace('/documents/');
}

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








