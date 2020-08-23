var csrf = $('input[name="csrfmiddlewaretoken"]').val();
var rnd = Math.random();
// var user_name = $('#input_name').val();

var get_local_file = function () {
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
            $('#exampleModal').modal();
            $('#input_local_file').val(data.path);
            $('#host_name').val(data.host_name);
            $('#local_ip').val(data.local_ip);
            $('#cpu_left').val(data.cpu_left);
            var main_app = $('#select_main_app').val();
            $('#select_' + main_app).show();
            $('#label_' + main_app).show();
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
            }

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

$('#btn_add_mission').on('click', function () {
    get_local_file()
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