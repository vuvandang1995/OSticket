$(document).ready(function(){
    $('#i_submit').click( function() {
        var checkFile = true;
        var fsize = $('#i_file')[0].files[0].size;
        alert(fsize);
        if(fsize>10485760){
            $(this).next('div.invalid-msg').html('<em>file is too big</em>').css('color','red');
            return checkFile = false;
        }
        return checkPass;
    });
});