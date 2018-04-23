$(document).ready(function(){
    $("#changeuser").click(function() {
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
                            window.location.reload();
                            // $("#list_agent").load(location.href + "#list_agent");
                            // document.getElementById("add_agent_close").click();
                        }
                    });
                }else{
                    alert('Mật khẩu mới không trùng khớp')
                }
            }else{
                alert('Mật khẩu hiện tại không đúng')
            }
        }else{
            $.ajax({
                type:'POST',
                url:location.href,
                data: {'change_user': fullname, 'email': email, 'phone': phone, 'csrfmiddlewaretoken':token, 'userid': userid},
                success: function(){
                    window.location.reload();
                    // $("#info_user").load(location.href + "#info_user");
                    // document.getElementById("change_user_close").click();
                }
            });
        }
    });


    
    $("#topicModal").on('show.bs.modal', function(event){
        var button = $(event.relatedTarget);
        var title = button.data('title');
        if (title === 'change'){
            $('#title').html("Edit User")
            var userid = button.attr('id');
            $("input[name=userid]").val(userid);

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

            var userid = button.attr('id');
            $("input[name=userid]").val(userid);

            $("input[name=fullname]").val('no');

            $("input[name=current_password]").val("");

            $("input[name=password]").val("");

            $("input[name=password2]").val("");

            $('#info').hide();
            $('#pwd').show();
        }
    });
    
});