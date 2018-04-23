$(document).ready(function(){
    $(".btn-primary").click(function() {
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var r = confirm('Are you sure?');
        if (r == true){
            $.ajax({
                type:'POST',
                url:location.href,
                data: {'close':id, 'csrfmiddlewaretoken':token},
                success: function(){
                    window.location.reload();
                    // $("#list_agent").load(location.href + "#list_agent");
                }
           });
        }
    });

    $(".btn-danger").click(function() {
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var r = confirm('Are you sure?');
        if (r == true){
            $.ajax({
                type:'POST',
                url:location.href,
                data: {'delete':id, 'csrfmiddlewaretoken':token},
                success: function(){
                    window.location.reload();
                    // $("#list_agent").load(location.href + "#list_agent");
                }
           });
        }
    });

    $("#addAgent").click(function() {
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var fullname = $("input[name=fullname]").val();
        var email = $("input[name=email]").val();
        var username = $("input[name=username]").val();
        var password = $("input[name=password]").val();
        var agentid = $("input[name=agentid]").val();
        $.ajax({
            type:'POST',
            url:location.href,
            data: {'add_agent': fullname, 'email': email, 'username': username, 'csrfmiddlewaretoken':token, 'agentid': agentid, 'password': password},
            success: function(){
                window.location.reload();
                // $("#list_agent").load(location.href + "#list_agent");
                // document.getElementById("add_agent_close").click();
            }
        });
    });



    $("#topicModal").on('show.bs.modal', function(event){
        var button = $(event.relatedTarget);
        var title = button.data('title');
        if (title === 'edit'){
            $('#title').html("Edit Agent")
            var agentid = button.attr('id');
            $("input[name=agentid]").val(agentid);

            var fullname = $("#full_name"+agentid).html();
            $("input[name=fullname]").val(fullname);

            var username = $("#user_name"+agentid).html();           
            $("input[name=username]").val(username);

            var email = $("#email_agent"+agentid).html();
            $("input[name=email]").val(email);

            $("input[name=password]").val("");
            $("input[name=password2]").val("");
            $('#pwd').hide();
        }else{
            $('#title').html("Add New Agent")
            $("input[name=agentid]").val(0);
            $("input[name=fullname]").val("");
            $("input[name=username]").val("");
            $("input[name=email]").val("");
            $('#pwd').show();
        }
    });
    
});