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

    $(".forward_ticket").click(function(){
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var id = $("input[name=ticketid]").val();
        var list_agent = [];
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
                // window.location.reload();
                document.getElementById("forward_ticket_close").click();
                $("#list_ticket").load(location.href + " #list_ticket");
                // $('#list_ticket'+' #forward'+id+' #forward_ticket_close').click();
            }
        });
    });



    $('#forward_modal').on('show.bs.modal', function(event){
        var button = $(event.relatedTarget);
        var ticketid = button.attr('id');
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
                // $('#forward input:checkbox').prop('checked', true);
            }
        }
        
    });
    
});