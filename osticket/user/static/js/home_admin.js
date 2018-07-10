$(document).ready(function(){
    $('#list_ticket_leader').DataTable({
        "columnDefs": [
            { "width": "5%", "targets": 0 },
            { "width": "20%", "targets": 1 },
            { "width": "15%", "targets": 2 },
            { "width": "5%", "targets": 3 },
            { "width": "10%", "targets": 4 },
            { "width": "5%", "targets": 5 },
            { "width": "40%", "targets": 6 },
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
        "displayLength": 25,
    });
    $("#list_ticket_leader").on('click', '.btn-primary', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var r = confirm('Are you sure?');
        var array = $('#hd'+id).html().split("<br>");
        var stt = $('#leader'+id).html();
        var date = formatAMPM(new Date());
        var array2 = [];
        for (i = 0; i < array.length-1; i++) {
            array2.push(array[i].replace(/\s/g,''));
        }
        if (r == true){
            $.ajax({
                type:'POST',
                url:location.href,
                data: {'close':id, 'csrfmiddlewaretoken':token},
                success: function(){
                    $('#list_ticket_leader').DataTable().ajax.reload();
                    if (stt != 'closed'){
                        array2.push('admin_close_ticket');
                        array2.push(id);
                        var sender = $('#sender'+id).html();
                        group_agent_Socket.send(JSON.stringify({
                            'message' : array2,
                            'time' : date,
                        }));

                        var Socket1 = new WebSocket(
                        'ws://' + window.location.host +
                        '/ws/user/' + sender + '/');

                        message = 'Ticket '+id+' is closed by admin!'
                        Socket1.onopen = function (event) {
                            setTimeout(function(){
                                Socket1.send(JSON.stringify({
                                    'message' : message,
                                    'time' : date,
                                }));
                                Socket1.close();
                            }, 1000);
                        };
                    }else{
                        array2.push('admin_open_ticket');
                        array2.push(id);
                        group_agent_Socket.send(JSON.stringify({
                            'message' : array2,
                            'time' : date,
                        }));
                        var sender = $('#sender'+id).html();
                        var Socket1 = new WebSocket(
                        'ws://' + window.location.host +
                        '/ws/user/' + sender + '/');

                        message = 'Ticket '+id+' is opened by admin!'
                        Socket1.onopen = function (event) {
                            setTimeout(function(){
                                Socket1.send(JSON.stringify({
                                    'message' : message,
                                    'time' : date,
                                }));
                                Socket1.close();
                            }, 1000);
                        };
                    }
                }
           });
        }
    });


    $("#list_ticket_leader").on('click', '.btn-danger', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var array = $('#hd'+id).html().split("<br>");
        var array2 = [];
        for (i = 0; i < array.length-1; i++) {
            array2.push(array[i].replace(/\s/g,''));
        }
        var date = formatAMPM(new Date());
        var r = confirm('Are you sure?');
        if (r == true){
            $.ajax({
                type:'POST',
                url:location.href,
                data: {'delete':id, 'csrfmiddlewaretoken':token},
                success: function(){
                    // window.location.reload();
                    array2.push('admin_delete_ticket');
                    array2.push(id);
                    group_agent_Socket.send(JSON.stringify({
                        'message' : array2,
                        'time' : date,
                    }));

                    $('#list_ticket_leader').DataTable().ajax.reload();
                    var sender = $('#sender'+id).html();
                    var Socket1 = new WebSocket(
                    'ws://' + window.location.host +
                    '/ws/user/' + sender + '/');
    
                    message = 'Ticket '+id+' is deleted by admin!' 
                    Socket1.onopen = function (event) {
                        setTimeout(function(){
                            Socket1.send(JSON.stringify({
                                'message' : message,
                                'time' : date,
                            }));
                            Socket1.close();
                        }, 1000);
                    };
                }
           });
        }
    });

    $(".forward_ticket").click(function(){
        $('.loading').show();
        $(this).prop('disabled', true);
        $(".inputText").prop('disabled', true);
        //$(".closefd").prop('disabled', true);
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var id = $("input[name=ticketid]").val();
        
        var list_agent = [];
        var date = formatAMPM(new Date());
        $('#forward_modal input:checkbox').each(function() {
            if ($(this).is(":checked")){
                list_agent.push(this.name);
            }
        });
        $.ajax({
            type:'POST',
            url:location.href,
            data: {'list_agent[]': JSON.stringify(list_agent),'csrfmiddlewaretoken':token, 'ticketid': id},
            success: function(){
                document.getElementById("forward_ticket_close").click();
                $('#list_ticket_leader').DataTable().ajax.reload();
                list_agent.push('leader_forward');
                list_agent.push(id);
                group_agent_Socket.send(JSON.stringify({
                    'message' : list_agent,
                    'time' : date,
                }));
                $(".loading").hide();
                $(".forward_ticket").prop('disabled', false);
                $(".inputText").prop('disabled', false);
                $(".closefd").prop('disabled', false);
                var sender = $('#sender'+id).html();
                var Socket1 = new WebSocket(
                'ws://' + window.location.host +
                '/ws/user/' + sender + '/');

                message = 'Ticket '+id+' is processing by admin!' 
                Socket1.onopen = function (event) {
                    setTimeout(function(){
                        Socket1.send(JSON.stringify({
                            'message' : message,
                            'time' : date,
                        }));
                        Socket1.close();
                    }, 1000);
                };
            }
        });
    });



    $('#forward_modal').on('show.bs.modal', function(event){
        var button = $(event.relatedTarget);
        var ticketid = button.attr('id');
        var topic = $("#tp"+ticketid).text();
        $('.tpic').each(function() {
            var dm = $(this).children('input').val();
            if (dm == topic){
                $(this).show();
            }else{
                $(this).hide();
            }
        });
        $("input[name=ticketid]").val(ticketid);
        var array = $('#hd'+ticketid).html().split("<br>");
        var list_agent = [];
        $('#forward_modal input:checkbox').each(function() {
            list_agent.push(this.name);
            $(this).prop('checked', false);
        });
        for (i = 0; i < array.length-1; i++) {
            var value = $.inArray(array[i].replace(/\s/g,''), list_agent)
            if (value > -1){
                $('input[name='+array[i].replace(/\s/g,'')+']').prop('checked', true);
            }
        }
        
    });
    
});