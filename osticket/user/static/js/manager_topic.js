$(document).ready(function(){
    $("#list_topic").on('click', '.close_', function(){
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
                    $("#list_topic").load(location.href + " #list_topic");
                }
           });
        }
    });

    $("#list_topic").on('click', '.btn-danger', function(){
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
                    $("#list_topic").load(location.href + " #list_topic");
                }
           });
        }
    });

    $("#addTopic").click(function() {
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var topicname = $("input[name=topicname]").val();
        var description = $("input[name=description]").val();
        var topicid = $("input[name=topicid]").val();
        var department = document.getElementById("mySelect").value;
        var list_agent = [];
        $('#topicModal input:checkbox').each(function() {
            if ($(this).is(":checked")){
                list_agent.push(this.name);
            }
        });
        $.ajax({
            type:'POST',
            url:location.href,
            data: {'add_topic': topicname, 'description': description, 'csrfmiddlewaretoken':token, 'topicid': topicid, 'list_agent[]': JSON.stringify(list_agent), 'department': department},
            success: function(){
                // window.location.reload();
                $("#list_topic").load(location.href + " #list_topic");
                document.getElementById("add_topic_close").click();
            }
        });
    });



    $("#topicModal").on('show.bs.modal', function(event){
        var button = $(event.relatedTarget);
        var title = button.data('title');
        if (title === 'edit'){
            $('#title').html("Edit Topic")
            var topicname = button.data('name');
            var topicid = button.attr('id');
            $("input[name=topicname]").val(topicname);

            var description = $("#description_topic"+topicid).html();
            $("input[name=description]").val(description);

            if ($('#type_send'+topicid).html() == 'All'){
                $('#topicModal input:checkbox').prop('checked', true);
            }else{
                $('#topicModal input:checkbox').prop('checked', false);
            }

            $("input[name=topicid]").val(topicid);
        }else{
            $('#title').html("Add New Topic")
            $("input[name=topicid]").val(0);
            $('#topicModal input:checkbox').prop('checked', false);
            $("input[name=topicname]").val("");
            $("input[name=description]").val("");
        }
    });
    
});