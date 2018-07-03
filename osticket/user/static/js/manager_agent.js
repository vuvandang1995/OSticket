$(document).ready(function(){
    $("#mnag").on('click', '.close_', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var r = confirm('Are you sure?');
        if (r == true){
            $.ajax({
                type:'POST',
                url:location.href,
                data: {'close':id, 'csrfmiddlewaretoken':token},
                success: function(){
                    // window.location.reload();
                    $("body #tb1").load(location.href + " #tb1");
                }
           });
        }
    });


    $("#mnag").on('click', '.btn-danger', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var r = confirm('Are you sure?');
        if (r == true){
            $.ajax({
                type:'POST',
                url:location.href,
                data: {'delete':id, 'csrfmiddlewaretoken':token},
                success: function(){
                    // window.location.reload();
                    $("body #tb1").load(location.href + " #tb1");
                }
           });
        }
    });

    $("#addAgent").click(function() {
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var fullname = $("input[name=fullname]").val();
        var email = $("input[name=email]").val();
        var phone = $("input[name=phone]").val();
        var username = $("input[name=username]").val();
        var password = $("input[name=password]").val();
        var agentid = $("input[name=agentid]").val();
        var department = document.getElementById("mySelect").value;
        $.ajax({
            type:'POST',
            url:location.href,
            data: {'add_agent': fullname, 'email': email, 'username': username, 'phone': phone, 'csrfmiddlewaretoken':token, 'agentid': agentid, 'password': password, 'department': department},
            success: function(){
                $("body #tb1").load(location.href + " #tb1");
                $("body #ct"+agentid).load(location.href + " #ct"+agentid);
                document.getElementById("add_agent_close").click();
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

            var phone = $("#phone_agent"+agentid).val();           
            $("input[name=phone]").val(phone);

            var email = $("#email_agent"+agentid).val();
            $("input[name=email]").val(email);

            var department = $("#department"+agentid).html();
            $("#mySelect option[name='"+department+"']").attr("selected", true);

            $("input[name=username]").val("");
            $("input[name=password]").val("");
            $("input[name=password2]").val("");
            $('#user_agent').hide();
            $('#pwd').hide();
        }else{
            $('#title').html("Add New Agent")
            $("input[name=agentid]").val(0);
            $("input[name=fullname]").val("");
            $("input[name=phone]").val("");
            $("input[name=username]").val("");
            $("input[name=email]").val("");
            $("input[name=password]").val("");
            $("input[name=password2]").val("");
            $('#user_agent').show();
            $('#pwd').show();
        }
    });
    
});