$(document).ready(function(){
    $("#info_user").on('click', '.cancel_forward', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var date = formatAMPM(new Date());
        var receive = $('body #receive'+id).html();
        
        if(confirm("Are you sure ?")){
             $.ajax({
                 type:'POST',
                 url:location.href,
                 data: {'tkid':id, 'csrfmiddlewaretoken':token, 'forward': 'forward'},
                 success: function(){
                     $("body #info_user").load(location.href + " #info_user");
                     message = ['cancle_forward', receive]
                     group_agent_Socket.send(JSON.stringify({
                         'message' : message,
                         'time' : date
                     }));
                 }
             });
        }
    });
    $("#info_user").on('click', '.cancel_add', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var receive = $('body #receive_'+id).html();
        var date = formatAMPM(new Date());
        if(confirm("Are you sure ?")){
             $.ajax({
                 type:'POST',
                 url:location.href,
                 data: {'tkid':id, 'csrfmiddlewaretoken':token, 'add': 'add'},
                 success: function(){
                     $("body #info_user").load(location.href + " #info_user");
                     message = ['cancle_add', receive]
                     group_agent_Socket.send(JSON.stringify({
                         'message' : message,
                         'time' : date
                     }));
                 }
             });
        }
    });
});