var csrf = $('input[name="csrfmiddlewaretoken"]').val();
var rnd = Math.random()

var get_local_file = function () {
    $.ajax({
        url: 'http://127.0.0.1:8500/file',
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

        },
        error: function (e) {
            alert('连接本地插件异常');
        },
    });
};

var update_tables = function () {
    var search_conditions = $('#search_condition').val();
    var search_key = $('#input_search_key').val();
    $.ajax({
        url: '/',
        type: 'get',
        data: {
            condition: search_conditions,
            keyword: search_key,
        },
        cache: 'false',
        dataType: 'html',
        success: function (data) {

            var table1 = $(data).find('#table_running').html();
            $("#table_running").html(table1);
            var table2 = $(data).find('#table_waiting').html();
            $("#table_waiting").html(table2);
            var table3 = $(data).find('#table_history').html();
            $("#table_history").html(table3);

        },
        error: function (e) {
            alert('与服务器连接异常: ' + e.message);
        },
    });
};


$('#btn_add_mission').on('click', function () {
    get_local_file()
});

$('#btn_add_mission_false').on('click', function () {
    $('#modal_login').modal();
});

$('#btn_search').on('click', function () {
    update_tables();
});

setInterval(function () {
    update_tables();
}, 20000);
