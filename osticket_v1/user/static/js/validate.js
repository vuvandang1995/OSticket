$(document).ready(function(){
    $("#register").click(function() {
        var filter = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
        var email = $.trim($("#email_").val());
        var p1 = $.trim($("#p1").val());
        var p2 = $.trim($("#p2").val());
        // Validate bằng jquery trên Client
        var checkPass = true;
        var dem = 0;
        $('.inputText').each(function (){
            dem++;   
            if($.trim($(this).val()) == ''){
                $(this).next('div.invalid-msg').html('<em>Vui lòng không được để trống</em>').css('color','red'); 
                return checkPass = false;
            }else{
                    $(this).next('div.invalid-msg').html('');
                    if (dem == 3)
                    {
                        if (!filter.test(email)){
                            $(this).next('div.invalid-msg').html('<em>Vui lòng nhập đúng định dạng email</em>').css('color','red');
                            return checkPass = false;
                        }else{
                            $(this).next('div.invalid-msg').html('');
                            }
                    }       
                    
                    if (dem == 5)
                    {
                        if (p2 != p1){
                            $(this).next('div.invalid-msg').html('<em>Mật khẩu không trùng khớp</em>').css('color','red');
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