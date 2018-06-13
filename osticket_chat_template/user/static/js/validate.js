$(document).ready(function(){
    $("#register").click(function() {
        var filterEmail = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
        var filterPhone = /^\+?1?\d{9,15}$/;
        var filterUsername = /^[a-zA-Z0-9]+$/;
        var email = $.trim($("#email_").val());
        var phone = $.trim($("#phone").val());
        var username = $.trim($("#username_").val());
        var p1 = $.trim($("#p1").val());
        var p2 = $.trim($("#p2").val());
        // Validate bằng jquery trên Client
        var checkPass = true;
        var dem = 0;
        $('.inputText').each(function (){
            dem++;   
            if($.trim($(this).val()) == ''){
                $(this).next('div.invalid-msg').html('<em>not be empty</em>').css('color','red');
                return checkPass = false;
            }else{
                    $(this).next('div.invalid-msg').html('');
                    if (dem == 2)
                    {
                        if (!filterUsername.test(username)){
                            $(this).next('div.invalid-msg').html('<em>invalid username</em>').css('color','red');
                            return checkPass = false;
                        }else{
                            $(this).next('div.invalid-msg').html('');
                            }
                    }

                    if (dem == 3)
                    {
                        if (!filterEmail.test(email)){
                            $(this).next('div.invalid-msg').html('<em>email only</em>').css('color','red');
                            return checkPass = false;
                        }else{
                            $(this).next('div.invalid-msg').html('');
                            }
                    }

                    if (dem == 4)
                    {
                        if (!filterPhone.test(phone)){
                            $(this).next('div.invalid-msg').html('<em>phone number only</em>').css('color','red');
                            return checkPass = false;
                        }else{
                            $(this).next('div.invalid-msg').html('');
                            }
                    }

                    if (dem == 6)
                    {
                        if (p2 != p1){
                            $(this).next('div.invalid-msg').html('<em>re-password is in correct</em>').css('color','red');
                            return checkPass = false;
                        }else{
                            $(this).next('div.invalid-msg').html('');
                            }
                    }
                }
        });
        return checkPass;
    });    
});