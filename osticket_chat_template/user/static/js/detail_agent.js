$(document).ready(function(){
    $("#changeuser").click(function() {
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var fullname = $("input[name=fullname]").val();
        var email = $("input[name=email]").val();
        var phone = $("input[name=phone]").val();
        var pwd_current = $("input[name=current_password]").val();
        var pwd1 = $("input[name=password]").val();
        var pwd2 = $("input[name=password2]").val();
        var authen_pwd = $("span[name=pwd_current]").attr('id');
        if (fullname == 'no'){
            if (pwd_current == authen_pwd){
                if (pwd1 == pwd2){
                    $.ajax({
                        type:'POST',
                        url:location.href,
                        data: {'csrfmiddlewaretoken':token, 'pwd': pwd1},
                        success: function(){
                            $("#info_user").load(location.href + " #info_user");
                            document.getElementById("change_user_close").click();
                        }
                    });
                }else{
                    alert('Mật khẩu mới không trùng khớp')
                }
            }else{
                alert('Mật khẩu hiện tại không đúng')
            }
        }else{
            var receive;
            if ($('#info input:checkbox').is(":checked")){
                receive = 1;
            }else {
                receive = 0;
            }
            $.ajax({
                type:'POST',
                url:location.href,
                data: {'fullname': fullname, 'email': email, 'phone': phone, 'receive': receive ,'csrfmiddlewaretoken':token},
                success: function(){
                    $("#info_user").load(location.href + " #info_user");
                    document.getElementById("change_user_close").click();
                }
            });
        }
    });

    $("#topicModal").on('show.bs.modal', function(event){
        var button = $(event.relatedTarget);
        var title = button.data('title');
        if (title === 'change'){
            $('#title').html("Edit User")

            var fullname = $("#full_name").html();
            $("input[name=fullname]").val(fullname);

            var email = $("#email_user").html();
            $("input[name=email]").val(email);

            var phone = $("#phone_user").html();
            $("input[name=phone]").val(phone);

            $('#info').show();
            $('#pwd').hide();
        }else if (title === 'change_pwd'){
            $('#title').html("Change your password")


            $("input[name=fullname]").val('no');

            $("input[name=current_password]").val("");

            $("input[name=password]").val("");

            $("input[name=password2]").val("");

            $('#info').hide();
            $('#pwd').show();
        }
    });

});