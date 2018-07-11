$(document).ready(function(){

    $('#list_ticket_processing').DataTable({
        "columnDefs": [
            { "width": "5%", "targets": 0 },
            { "width": "25%", "targets": 1 },
            { "width": "15%", "targets": 2 },
            { "width": "5%", "targets": 3 },
            { "width": "15%", "targets": 4 },
            { "width": "35%", "targets": 5 },
        ],
        "ajax": {
            "type": "GET",
            "url": location.href +"data",
            "contentType": "application/json; charset=utf-8",
            "data": function(result){
                return JSON.stringify(result);
            }
        },
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
        "order": [[ 0, "desc" ]],
    });

    $('body').on('click', '.fw_agent', function(){
        var tkid = $(this).attr('id');
        var topic = $("#tp"+tkid).text();
        $('.tpic').each(function() {
            var dm = $(this).children('input').val();
            if (dm == topic){
                $(this).show();
            }else{
                $(this).hide();
            }
        });
        $("body input[name=ticketid]").val(tkid);
        $("body #content").val('');
        $('body #title').html("Forward ticket no."+tkid+" to agents")
        var array = $('body #hd'+tkid).html().split(",");
        var list_agent = [];
        $('body #forward_add input:checkbox').each(function() {
            list_agent.push(this.name);
            $(this).parent().show();
            
        });
        for (i = 0; i < array.length-1; i++) {
            var value = $.inArray(array[i].replace(/\s/g,''), list_agent)
            if (value > -1){
                $('div[id='+array[i].replace(/\s/g,'')+']').hide();
            }
        }
        
    });

    $('body').on('click', '.add_agent', function(){
        var tkid = $(this).attr('id');
        var topic = $("#tp"+tkid).text();
        $('.tpic').each(function() {
            var dm = $(this).children('input').val();
            if (dm == topic){
                $(this).show();
            }else{
                $(this).hide();
            }
        });
        $("body input[name=ticketid]").val(tkid);
        $("body #content").val('');
        $('body #title').html("Add ticket no."+tkid+" to agents")
        var array = $('body #hd'+tkid).html().split(",");
        var list_agent = [];
        $('body #forward_add input:checkbox').each(function() {
            list_agent.push(this.name);
            $(this).parent().show();
        });
        for (i = 0; i < array.length-1; i++) {
            var value = $.inArray(array[i].replace(/\s/g,''), list_agent)
            if (value > -1){
                $('div[id='+array[i].replace(/\s/g,'')+']').hide();
            }
        }
    });

    $('body').on('click', '#fw_add', function(){
        var title = $('body #title').html();
        var content = $("body #content").val();
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var tkid = $("body input[name=ticketid]").val();
        var list_agent = [];
        $('body #forward_add input:checkbox').each(function() {
            if ($(this).is(":checked")){
                list_agent.push(this.name);
            }
        });
        if (title.includes('Forward')){
            $.ajax({
                type:'POST',
                url:location.href,
                data: {'list_agent[]': JSON.stringify(list_agent),'csrfmiddlewaretoken':token, 'ticketid': tkid, 'content': content, 'type': 'forward_agent'},
                success: function(){
                    var date = formatAMPM(new Date());
                    document.getElementById("close_fw_add").click();
                    list_agent.push('forward_new');
                    group_agent_Socket.send(JSON.stringify({
                        'message' : list_agent,
                        'time' : date
                    }));
                            }
            });
        }else{
            $.ajax({
                type:'POST',
                url:location.href,
                data: {'list_agent[]': JSON.stringify(list_agent),'csrfmiddlewaretoken':token, 'ticketid': tkid, 'content': content, 'type': 'add_agent'},
                success: function(){
                    var date = formatAMPM(new Date());
                    document.getElementById("close_fw_add").click();
                    list_agent.push('add_new');
                    group_agent_Socket.send(JSON.stringify({
                        'message' : list_agent,
                        'time' : date
                    }));
                }
            });
        }
    });




    $("body").on('click', '.handle_done', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        if(confirm("Are you sure ?")){

             $.ajax({
                 type:'POST',
                 url:location.href,
                 data: {'tkid':id, 'csrfmiddlewaretoken':token, 'stt': 2, 'type': 'process_done'},
                 success: function(){
                     var date = formatAMPM(new Date());
                     $("#list_ticket_processing").DataTable().ajax.reload();

                     var userName = $('#user'+id).val();

                     var Socket1 = new WebSocket(
                         'ws://' + window.location.host +
                         '/ws/user/' + userName + '/');

                     message = 'Ticket '+id+' is done!' 
                     Socket1.onopen = function (event) {
                         setTimeout(function(){
                             Socket1.send(JSON.stringify({
                                 'message' : message,
                                 'time' : date
                             }));
                             Socket1.close();
                         }, 1000);
                     };

                    // con thong bao toi agent khac, load lai trang cua agent va admin
                    list_agent = [];
                    var date = formatAMPM(new Date());
                    var array = $('body #hd'+id).html().split("<br>");
                    for (i = 0; i < array.length-1; i++) {
                        if (agentName !=  array[i].replace(/\s/g,'')){
                            list_agent.push(array[i].replace(/\s/g,'')+'+');
                        }
                    }

                    list_agent.unshift(message);
                    list_agent.unshift(id);
                    list_agent.unshift(agentName);
                    group_agent_Socket.send(JSON.stringify({
                        'message' : list_agent,
                        'time' : date
                    }));
                         
                 }
             });
         }
     });


     $("body").on('click', '.handle_processing', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        if(confirm("Are you sure ?")){
             $.ajax({
                 type:'POST',
                 url:location.href,
                 data: {'tkid':id, 'csrfmiddlewaretoken':token, 'stt': 1, 'type': 'process_done'},
                 success: function(){
                     var date = formatAMPM(new Date());
                     $("#list_ticket_processing").DataTable().ajax.reload();

                     var userName = $('#user'+id).val();

                     var Socket1 = new WebSocket(
                         'ws://' + window.location.host +
                         '/ws/user/' + userName + '/');

                     message = 'Ticket '+id+' is re-process!' 
                     Socket1.onopen = function (event) {
                         setTimeout(function(){
                             Socket1.send(JSON.stringify({
                                 'message' : message,
                                 'time' : date
                             }));
                             Socket1.close();
                         }, 1000);
                     };

                     // con thong bao toi agent khac, load lai trang cua agent va admin
                    list_agent = [];
                    var date = formatAMPM(new Date());
                    var array = $('body #hd'+id).html().split("<br>");
                    for (i = 0; i < array.length-1; i++) {
                        if (agentName !=  array[i].replace(/\s/g,'')){
                            list_agent.push(array[i].replace(/\s/g,'')+'+');
                        }
                    }

                    list_agent.unshift(message);
                    list_agent.unshift(id);
                    list_agent.unshift(agentName);
                    group_agent_Socket.send(JSON.stringify({
                        'message' : list_agent,
                        'time' : date
                    }));
                         
                 }
             });
        }
    });
    
    $("body").on('click', '.give_up', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        if(confirm("Are you sure ?\n*You can't give up when there is only you handle this ticket.")){
             $.ajax({
                 type:'POST',
                 url:location.href,
                 data: {'tkid':id, 'csrfmiddlewaretoken':token, 'type': 'give_up'},
                 success: function(){
                     // window.location.reload();
                     $("#list_ticket_processing").DataTable().ajax.reload();

                     var userName = $('#user'+id).val();
                     var Socket1 = new WebSocket(
                         'ws://' + window.location.host +
                         '/ws/user/' + userName + '/');

                     message = 'give up'
                     var date = formatAMPM(new Date());
                     Socket1.onopen = function (event) {
                         setTimeout(function(){
                             Socket1.send(JSON.stringify({
                                 'message' : message,
                                 'time' : date
                             }));
                             Socket1.close();
                         }, 1000);
                     };
                     // con thong bao toi agent khac, load lai trang cua agent va admin
                     list_agent = [];
                     var date = formatAMPM(new Date());
                     var array = $('body #hd'+id).html().split("<br>");
                     for (i = 0; i < array.length-1; i++) {
                         if (agentName !=  array[i].replace(/\s/g,'')){
                             list_agent.push(array[i].replace(/\s/g,'')+'+');
                         }
                     }

                     list_agent.unshift('give_up');
                     list_agent.unshift(id);
                     list_agent.unshift(agentName);
                     group_agent_Socket.send(JSON.stringify({
                         'message' : list_agent,
                         'time' : date
                     }));
                 }
             });
         }
    });

     $("body").on('click', '#chat_with_user', function(){
         var tkid = $(this).children('input').val();
         $("body .noti_chat"+tkid).hide();
         $('body .chat'+tkid).show();
         $("body .mytext").focus();
         

         if (dict_ws[tkid] == undefined){
             dict_ws[tkid] = new WebSocket(
             'ws://' + window.location.host +
             '/ws/' + tkid + '/');
         }

         var me = {};
         me.avatar = "https://cdn2.iconfinder.com/data/icons/perfect-flat-icons-2/512/User_man_male_profile_account_person_people.png";

         var you = {};
         you.avatar = "https://cdn2.iconfinder.com/data/icons/rcons-users-color/32/support_man-512.png";      

         //-- No use time. It is a javaScript effect.
         function insertChat(who, text, time){
             if (time === undefined){
                 time = 0;
             }
             var control = "";
             var date = time;
             
             if (who == "me"){
                 control = '<li style="width:100%">' +
                                 '<div class="msj macro">' +
                                 '<div class="avatar"><img class="img-circle" style="width:100%;" src="'+ me.avatar +'" /></div>' +
                                     '<div class="text text-l">' +
                                         '<p>'+ text +'</p>' +
                                         '<p><small>'+date+'</small></p>' +
                                     '</div>' +
                                 '</div>' +
                             '</li>';                    
             }else{
                 control = '<li style="width:100%;">' +
                                 '<div class="msj-rta macro">' +
                                     '<div class="text text-r">' +
                                         '<p>'+text+'</p>' +
                                         '<p><small>'+date+'</small></p>' +
                                     '</div>' +
                                 '<div class="avatar" style="padding:0px 0px 0px 10px !important"><img class="img-circle" style="width:100%;" src="'+you.avatar+'" /></div>' +                                
                         '</li>';
             }
             setTimeout(
                 function(){                        
                     $("body #chat"+tkid+" .frame > ul").append(control).scrollTop($("body #chat"+tkid+" .frame > ul").prop('scrollHeight'));
                 }, time);
             
         }

         
         dict_ws[tkid].onmessage = function(e) {
             var data = JSON.parse(e.data);
             var message = data['message'];
             var who = data['who'];
             var time = data['time'];
             insertChat(who, message, time);
         };

         
     });
    

});