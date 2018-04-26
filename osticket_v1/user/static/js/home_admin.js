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
                    // window.location.reload();
                    $("#list_ticket").load(location.href + " #list_ticket");
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
                    // window.location.reload();
                    $("#list_ticket").load(location.href + " #list_ticket");
                }
           });
        }
    });
    $("#forward_ticket").click(function() {
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var list_agent = [];
        $('#topicModal input:checkbox').each(function() {
            if ($(this).is(":checked")){
                list_agent.push(this.name);
            }
        });
        var ticketid = $("input[name=ticketid]").val();
        $.ajax({
            type:'POST',
            url:location.href,
            data: {'list_agent[]': JSON.stringify(list_agent),'csrfmiddlewaretoken':token, 'ticketid': ticketid},
            success: function(){
                window.location.reload();
                // $("#list_ticket").load(location.href + "#list_ticket");
            }
        });
    });



    $("#topicModal").on('show.bs.modal', function(event){
        var button = $(event.relatedTarget);
        var title = button.data('title');
        if (title === 'forward'){
            var ticketid = button.attr('id');
            $("input[name=ticketid]").val(ticketid);
        }
    });
    
});