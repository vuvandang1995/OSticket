$(document).ready(function(){
    $("#info_user").on('click', '.unblock', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        if(confirm("Are you sure ?")){
             $.ajax({
                 type:'POST',
                 url:location.href,
                 data: {'tkid':id, 'csrfmiddlewaretoken':token, 'stt': 1},
                 success: function(){
                    //  $("body .stt"+id).empty();
                    //  $("body #stt"+id).load(location.href + " #stt"+id);
                    //  $("body #button"+id).load(location.href + " #button"+id);
                    $("body #example23").load(location.href + " #example23");
                    load_js();
                 }
             });
        }
    });
    $("#info_user").on('click', '.block', function(){
        var id = $(this).attr('id');
        var token = $("input[name=csrfmiddlewaretoken]").val();
        if(confirm("Are you sure ?")){
             $.ajax({
                 type:'POST',
                 url:location.href,
                 data: {'tkid':id, 'csrfmiddlewaretoken':token, 'stt': 0},
                 success: function(){
                    //  $("body #xx").load(location.href + " #xx");
                    // $("body #stt"+id).empty();
                    // $("body #stt"+id).load(location.href + " #stt"+id);
                    // $("body #button"+id).load(location.href + " #button"+id);
                    $("body #example23").load(location.href + " #example23");
                    load_js();
                 }
             });
        }
    });
});