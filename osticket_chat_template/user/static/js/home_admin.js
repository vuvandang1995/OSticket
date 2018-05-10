$(document).ready(function(){

    $("#list_ticket").on('click', '.btn-primary', function(){
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

    // $(".close_ticket").click(function() {
    //     var id = $(this).attr('id');
    //     if(confirm("Are you sure ?")){
    //         alert(id);
    //     }
    // });

    // $(".conversation_user").click(function() {
    //     var id = $(this).attr('id');
    //     alert(id);
    // });

    $("#sound").click(function() {
        var x = document.getElementById("myAudio");
        x.play(); 
    });

    $("#list_ticket").on('click', '.btn-danger', function(){
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

    $("#list_ticket").on('click', '.forward_ticket', function(){
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var id = $(this).attr('id');
        var list_agent = [];
        $("#forward"+id+' input:checkbox').each(function() {
            if ($(this).is(":checked")){
                list_agent.push(this.name);
            }
        });
        $.ajax({
            type:'POST',
            url:location.href,
            data: {'list_agent[]': JSON.stringify(list_agent),'csrfmiddlewaretoken':token, 'ticketid': id},
            success: function(){
                // window.location.reload();
                $("#list_ticket").load(location.href + "#list_ticket");
            }
        });
    });



    // $('.fw').on('show.bs.modal', function(event){
    //     var button = $(event.relatedTarget);
    //     var title = button.data('title');
    //     if (title === 'forward'){
    //         var ticketid = button.attr('id');
    //         $("input[name=ticketid]").val(ticketid);
    //     }
    // });
    
});