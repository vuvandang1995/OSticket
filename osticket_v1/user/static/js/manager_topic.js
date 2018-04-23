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
                    // $("#list_topic").load(location.href + "#list_topic");
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
                    // $("#list_topic").load(location.href + "#list_topic");
                }
           });
        }
    });

    $("#addTopic").click(function() {
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var topicname = $("input[name=topicname]").val();
        var topicid = $("input[name=topicid]").val();
        $.ajax({
            type:'POST',
            url:location.href,
            data: {'add_topic': topicname, 'csrfmiddlewaretoken':token, 'topicid': topicid},
            success: function(){
                window.location.reload();
                // $("#list_topic").load(location.href + "#list_topic");
                // document.getElementById("add_topic_close").click();
                // $("#topicModal").modal({"backdrop": "static"});
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
            $("input[name=topicid]").val(topicid);
        }else{
            $('#title').html("Add New Topic")
            $("input[name=topicid]").val(0);
            $("input[name=topicname]").val("");
        }
    });
    
});