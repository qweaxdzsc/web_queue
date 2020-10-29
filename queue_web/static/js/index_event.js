var csrf = $('input[name="csrfmiddlewaretoken"]').val();
var rnd = Math.random();
var delete_id = '';
// var user_name = $('#input_name').val();


var new_mission_dialog = function () {
    $('#new_mission_model').modal();
    var main_app = $('#select_main_app').val();
    $('.select_extend').hide();
    $('#select_' + main_app).show();
    $('#label_' + main_app).show();
};

var show_delete_icon = function () {
    var dm = $('.delete_mission');
    $.each(dm, function (index, domEle){
        email = domEle.parentElement.className;
        name = email.split('.')[0];
        user_name = $('.user_info').text();

        if (user_name.indexOf(name) != -1 ) {
            $(this).show();
        } else {
            $(this).hide();

        };

    });
};

var get_local_file = function (success_doing) {
    $.ajax({
        url: 'http://localhost:37171/file',
        type: 'get',
        cache: 'false',
        data: {
            rnd: rnd
        },
        datatype: 'json',
        success: function (data) {
            console.log(data);
            $('#input_local_file').val(data.path);
            $('#host_name').val(data.host_name);
            $('#local_ip').val(data.local_ip);
            $('#total_cores').val(data.total_cores);
            var recommend_app = data.recommend_app
            console.log(recommend_app);
            if (recommend_app == 'none') {
                alert('没有找到推荐的流程，请确认是否是正确的文件格式');
            } else {
                $('#select_main_app').val(recommend_app);
            }
            success_doing();
        },
        error: function (e) {
            alert('连接本地插件异常');
        },
    });
};

var update_tables = function () {
    var search_conditions = $('#search_condition').val();
    var search_key = $('#input_search_key').val();
    var current_user = $('#btn_filter_user').is('.active');
    $.ajax({
        url: '/search_list',
        type: 'get',
        data: {
            condition: search_conditions,
            keyword: search_key,
            current_user: current_user,
        },
        cache: 'false',
        dataType: 'html',
        success: function (data) {
            var search_error = $(data).find('#search_error').text();
            if (search_error.length > 0) {
                alert('搜索错误：' + search_error);
            } else {
                var table1 = $(data).find('#table_running').html();
                $("#table_running").html(table1);
                var table2 = $(data).find('#table_waiting').html();
                $("#table_waiting").html(table2);
                var table3 = $(data).find('#table_history').html();
                $("#table_history").html(table3);
                show_delete_icon();
            };

        },
        error: function (e) {
            alert('与服务器连接异常: ' + e.message);
        },
    });
};


var change_app = function () {
    $('.select_extend').hide();
    var main_app = $('#select_main_app').val();
    $('#select_' + main_app).show();
    $('#label_' + main_app).show();
};


$('.delete_mission').on('click', function () {
    delete_id = $(this)[0].id;
    console.log(delete_id);
    $('#delete_confirm_modal').modal();
    $
});


$('#delete_confirm').on('click', function () {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    split_list = delete_id.split('-');
    var exec_app = split_list[0];
    var order_id = split_list[1];
    console.log(exec_app, order_id);
    $.ajax({
        url:'/test/',
        type:'post',
        cache: 'false',
        data: {exec_app: exec_app, order_id: order_id, csrfmiddlewaretoken:csrf},
        datatype: 'json',
        success: function (data) {
            location.reload();
        },
        error: function (e) {
            alert('异常，删除失败');
        },
    });
});


$('#btn_pause').on('click', function () {
    var paused = $('#btn_pause').is('.active');
    console.log(Number(paused));
    $.ajax({
        url: '/pause',
        type: 'get',
        data: { pause: Number(paused) },
        success: function (data) {
            if (paused == false) {
                $('#btn_pause').addClass('active');
                $('#btn_pause').removeClass('text-muted');
            } else {
                $('#btn_pause').removeClass('active');
                $('#btn_pause').addClass('text-muted');
            };
        },
        error: function (e) {
            alert('连接异常');
        },
    });
});


$('#btn_add_mission').on('click', function () {
    get_local_file(new_mission_dialog);
});

$('#btn_local_file').on('click', function () {
    function replace_new_address() {
    };
    get_local_file(replace_new_address);
});

$('#btn_add_mission_false').on('click', function () {
    $('#modal_login').modal();
});

$('#btn_filter_user').on('click', function () {
    var choosen = $('#btn_filter_user').is('.active');
    if (choosen == false) {
        $('#btn_filter_user').addClass('active');
    } else {
        $('#btn_filter_user').removeClass('active');
    };
    update_tables();
});

$('#btn_filter_user_false').on('click', function () {
    $('#modal_login').modal();
});

$('#btn_search').on('click', function () {
    update_tables();
});

$('#select_main_app').on('change', function () {
    change_app();
});

setInterval(function () {
    update_tables();
}, 20000);


show_delete_icon();

// setInterval(function () {
//     show_delete_icon();

// }, 10000);


// $(window).scroll(function() {
//     var srollPos = $(window).scrollTop(); 
//     totalheight = parseFloat($(window).height()) + parseFloat(srollPos);
//     console.log(totalheight);
//     if(($(document).height() - 0) <= totalheight && num != maxnum) {
//     //把要添加的数据写到下面函数中，即可实现滚动添加
//     console.log('scroll')
//     //num++;
//     }
//   }); 
// function scroll(){
//     //console.log("打印log日志");实时看下效果
//     console.log("开始滚动！");
// }

// var scrollFunc = function (e) {  
//     e = e || window.event;  
//     if (e.wheelDelta) {  //第一步：先判断浏览器IE，谷歌滑轮事件               
//         if (e.wheelDelta > 0) { //当滑轮向上滚动时  
//             console.log("滑轮向上滚动");  
//         }  
//         if (e.wheelDelta < 0) { //当滑轮向下滚动时  
//             console.log("滑轮向下滚动");  
//         }  
//     } else if (e.detail) {  //Firefox滑轮事件  
//         if (e.detail> 0) { //当滑轮向上滚动时  
//             console.log("滑轮向上滚动");  
//         }  
//         if (e.detail< 0) { //当滑轮向下滚动时  
//             console.log("滑轮向下滚动");  
//         }  
//     }  
// }
// //给页面绑定滑轮滚动事件  
// if (document.addEventListener) {//firefox  
//     document.addEventListener('DOMMouseScroll', scrollFunc, false);  
// }  
// //滚动滑轮触发scrollFunc方法  //ie 谷歌  
// window.onmousewheel = document.onmousewheel = scrollFunc;
