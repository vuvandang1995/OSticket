$(document).ready(function(){
    $('body').on('click', '.info_agent', function(){
        var userid = $(this).attr('id');
        $('body #title').html("Edit User")
        $("body input[name=userid]").val(userid);

        var fullname = $("body #full_name").html();
        $("body input[name=fullname]").val(fullname);

        var email = $("body #email_user").html();
        $("body input[name=email]").val(email);

        var phone = $("body #phone_user").html();
        $("body input[name=phone]").val(phone);

        if ($('body #rc_email').html() == 'Yes'){
            $('body #topicModal input:checkbox').prop('checked', true);
        }else{
            $('body #topicModal input:checkbox').prop('checked', false);
        }

        $('body #info').show();
        $('body #pwd').hide();
        
    });

    $('body').on('click', '.pwd_agent', function(){
        var userid = $(this).attr('id');
        $('body #title').html("Change your password")

        $("body input[name=userid]").val(userid);

        $("body input[name=fullname]").val('no');

        $("body input[name=current_password]").val("");

        $("body input[name=password]").val("");

        $("body input[name=password2]").val("");

        $('body #info').hide();
        $('body #pwd').show();
    });

    $('body').on('click', '#changeuser', function(){
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var fullname = $("input[name=fullname]").val();
        var email = $("input[name=email]").val();
        var phone = $("input[name=phone]").val();
        var pwd_current = $("input[name=current_password]").val();
        var userid = $("input[name=userid]").val();
        var pwd1 = $("input[name=password]").val();
        var pwd2 = $("input[name=password2]").val();
        var authen_pwd = $("span[name=pwd_current]").attr('id');
        
        if (fullname == 'no'){
            if (pwd_current == authen_pwd){
                if (pwd1 == pwd2){
                    $.ajax({
                        type:'POST',
                        url:location.href,
                        data: {'csrfmiddlewaretoken':token, 'userid': userid, 'pwd': pwd1},
                        success: function(){
                            document.getElementById("change_user_close").click();
                            $("#info-user").load(location.href + " #info-user");
                        }
                    });
                }else{
                    alert('Mật khẩu mới không trùng khớp')
                }
            }else{
                alert('Mật khẩu hiện tại không đúng')
            }
        }else{
            var receive_mail;
            if ($('#topicModal input:checkbox').is(":checked")){
                receive_mail = 1;
            }else {
                receive_mail = 0;
            }
            $.ajax({
                type:'POST',
                url:location.href,
                data: {'change_user': fullname, 'email': email, 'phone': phone, 'csrfmiddlewaretoken':token, 'userid': userid, 'receive_mail': receive_mail},
                success: function(){
                    // window.location.reload();
                    document.getElementById("change_user_close").click();
                    $("#info-user").load(location.href + " #info-user");
                }
            });
        }
    });
});