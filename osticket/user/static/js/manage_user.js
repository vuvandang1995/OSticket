$(document).ready(function(){
    $("#info_user").on('click', '.unblock', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        if(confirm("Are you sure ?")){
             $.ajax({
                 type:'POST',
                 url:location.href,
                 data: {'tkid':id, 'csrfmiddlewaretoken':token, 'stt': 1},
                 success: function(){
                     $("body #info_user").load(location.href + " #info_user");
                 }
             });
        }
    });
    $("#info_user").on('click', '.block', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        if(confirm("Are you sure ?")){
             $.ajax({
                 type:'POST',
                 url:location.href,
                 data: {'tkid':id, 'csrfmiddlewaretoken':token, 'stt': 0},
                 success: function(){
                     $("body #info_user").load(location.href + " #info_user");
                 }
             });
        }
    });
});