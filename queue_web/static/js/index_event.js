var csrf = $('input[name="csrfmiddlewaretoken"]').val();
var rnd = Math.random()
$('#btn_add_mission').on('click', function () {
    $.ajax({
        url: 'http://127.0.0.1:8500/file',
        type: 'get',
        cache: 'false',
        data: { rnd: rnd },
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
    return false;
});
setInterval(function () {
    replace_tables();
}, 20000);

$('#btn_add_mission_false').on('click', function () {
    $('#modal_login').modal();
});

var replace_tables = function () {
    $.ajax({
        url: '/',
        type: 'get',
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
        },
    });
};
