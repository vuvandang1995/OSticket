$(document).ready(function(){
    $("body").on('click', '.accept_forward', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        if(confirm("Are you sure ?")){
             var sender = $('body #sender'+id).html();
             var date = formatAMPM(new Date());
             message = fullname+' agreed your ticket you forwarding +'+sender;
             group_agent_Socket.send(JSON.stringify({
                 'message' : message,
                 'time' : date
             }));

             var userName = $('#user'+id).val();
             var Socket1 = new WebSocket(
                 'ws://' + window.location.host +
                 '/ws/user/' + userName + '/');

             message = 'process' 
             Socket1.onopen = function (event) {
                 setTimeout(function(){
                     Socket1.send(JSON.stringify({
                         'message' : message,
                         'time' : date
                     }));
                 }, 1000);
             };

             $.ajax({
                 type:'POST',
                 url:location.href,
                 data: {'tkid':id, 'csrfmiddlewaretoken':token, 'forward': 'forward', 'agree': 'agree'},
                 success: function(){
                     $("body #info_user").load(location.href + " #info_user");
                    //  Socket1.close();
                 }
             });
        }
    });

    $("body").on('click', '.deny_forward', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        if(confirm("Are you sure ?")){
             var sender = $('body #sender'+id).html();
             var date = formatAMPM(new Date());
             message = 'Your ticket you forwarding refused by '+fullname+' +'+sender;
             group_agent_Socket.send(JSON.stringify({
                 'message' : message,
                 'time' : date
             }));

             $.ajax({
                 type:'POST',
                 url:location.href,
                 data: {'tkid':id, 'csrfmiddlewaretoken':token, 'forward': 'forward', 'deny': 'deny'},
                 success: function(){
                     $("body #info_user").load(location.href + " #info_user");
                 }
             });
        }
    });

    $("body").on('click', '.accept_add', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        if(confirm("Are you sure ?")){
             var sender = $('body #sender_'+id).html();
             var date = formatAMPM(new Date());
             message = fullname+' agreed your ticket you adding +'+sender;
             group_agent_Socket.send(JSON.stringify({
                 'message' : message,
                 'time' : date
             }));

             var userName = $('#user'+id).val();

             var Socket1 = new WebSocket(
                 'ws://' + window.location.host +
                 '/ws/user/' + userName + '/');

             message = 'process' 
             Socket1.onopen = function (event) {
                 setTimeout(function(){
                     Socket1.send(JSON.stringify({
                         'message' : message,
                         'time' : date
                     }));
                 }, 1000);
             };
             
             $.ajax({
                 type:'POST',
                 url:location.href,
                 data: {'tkid':id, 'csrfmiddlewaretoken':token, 'add': 'add', 'agree': 'agree'},
                 success: function(){
                     $("body #info_user").load(location.href + " #info_user");
                    //  Socket1.close();
                 }
             });
        }
    });
    $("body").on('click', '.deny_add', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        if(confirm("Are you sure ?")){
             var sender = $('body #sender_'+id).html();
             var date = formatAMPM(new Date());
             message = 'Your ticket you adding refused by '+fullname+' +'+sender;
             group_agent_Socket.send(JSON.stringify({
                 'message' : message,
                 'time' : date
             }));

             $.ajax({
                 type:'POST',
                 url:location.href,
                 data: {'tkid':id, 'csrfmiddlewaretoken':token, 'add': 'add', 'deny': 'deny'},
                 success: function(){
                     $("body #info_user").load(location.href + " #info_user");
                 }
             });
        }
    });
});