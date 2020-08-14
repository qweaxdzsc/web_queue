var auth = '';
var event_login = function(){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var name = $('#input_name').val();
    var pwd = $('#input_pwd').val();
    $.ajax({
        url:'/login/',
        type:'post',
        cache: 'false',
        data: {name: name, pwd:pwd, csrfmiddlewaretoken:csrf},
        datatype: 'json',
        success: function(data) {
            console.log(data);
            if(data.pass){
               auth = data.authorization
               window.location.reload()
            }
            else {
                console.log($('#login_tip'));
                $('#login_tip').text(data.error_info);
                $('#login_tip').css('visibility','visible');


            };
        },
        error:function(e){
            alert('连接异常');
       },
    });
};

$('#btn_login_submit').on('click', function(){
    event_login()
});