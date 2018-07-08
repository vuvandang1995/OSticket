$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
    $("body").on('click', '.assign_ticket', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        if(confirm("Are you sure ?")){
            var userName = document.getElementById('user_name'+id).value;
            var chatSocket1 = new WebSocket(
                'ws://' + window.location.host +
                '/ws/user/' + userName + '/');

            var date = formatAMPM(new Date());
            message = 'Ticket '+id+' is processing!';
            chatSocket1.onopen = function (event) {
                chatSocket1.send(JSON.stringify({
                    'message' : message,
                    'time' : date,
                }));
            };

            group_agent_Socket.send(JSON.stringify({
                'message' : 'ticket da duoc xu ly',
                'time' : date,
            }));

            $.ajax({
                type:'POST',
                url:location.href,
                data: {'tkid':id, 'csrfmiddlewaretoken':token},
                success: function(){
                    chatSocket1.close();
                }
            });
        }
    });
});