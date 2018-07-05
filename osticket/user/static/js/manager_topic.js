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
        var department_name = $("#mySelect option[value='"+department+"']").html();
        $("#nameerr").html("");
        $("#deserr").html("");
        if (topicname==''){
            $("#nameerr").html("not null");
        }
        else if(description==''){
            $("#deserr").html("not null");
        }else{
            $.ajax({
                type:'POST',
                url:location.href,
                data: {'add_topic': topicname, 'description': description, 'csrfmiddlewaretoken':token, 'topicid': topicid, 'list_agent[]': JSON.stringify(list_agent), 'department': department},
                success: function(){
                    // window.location.reload();
                    $("#list_topic").load(location.href + " #list_topic");
                    document.getElementById("add_topic_close").click();
                    var date = formatAMPM(new Date());
                    list_agent.unshift('admin_add_department');
                    list_agent.unshift(department_name);
                    group_agent_Socket.send(JSON.stringify({
                        'message' : list_agent,
                        'time' : date
                    }));
                }
            });
        }
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

            var department = $("#department_topic"+topicid).html();
            $("#mySelect option[name='"+department+"']").prop("selected", true);

            $('.dpm').each(function() {
                var dm = $(this).children('input').val();
                if (dm == department){
                    $(this).show();
                }else{
                    $(this).hide();
                }
            });

            var hd = $("#hd_topic"+topicid).html().split("<br>");
            $('#topicModal input:checkbox').each(function() {
                for (i = 0; i < hd.length-1; i++) {
                    if (this.name == hd[i].replace(/\s/g,'')){
                        $(this).prop('checked', true);
                    }
                }
            });
            

            $("input[name=topicid]").val(topicid);
        }else{
            var x = $('#mySelect option:selected').html();
            $('.dpm').each(function() {
                var dm = $(this).children('input').val();
                if (dm == x){
                    $(this).show();
                }else{
                    $(this).hide();
                }
            });
            $('#title').html("Add New Topic")
            $("input[name=topicid]").val(0);
            $('#topicModal input:checkbox').prop('checked', false);
            $("input[name=topicname]").val("");
            $("input[name=description]").val("");
        }
    });
    
});