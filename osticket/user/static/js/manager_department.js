$(document).ready(function(){
    $("#list_dm").on('click', '.btn-danger', function(){
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
                    $("#list_dm").load(location.href + " #list_dm");
                }
           });
        }
    });

    $("#addDepartment").click(function() {
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var addname = $("input[name=name]").val();
        var adddescription = $("input[name=des]").val();
        var dmid = $("input[name=dmid]").val();
        $("#add_name_error").html("");
        $("#add_des_error").html("");
        if (addname==''){
            $("#add_name_error").html("not null");
        }
        else if(adddescription==''){
            $("#add_des_error").html("not null");
        }else{
            $.ajax({
                type:'POST',
                url:location.href,
                data: {'addname': addname, 'adddescription': adddescription, 'csrfmiddlewaretoken':token , 'dmid':dmid},
                success: function(){
                    // window.location.reload();
                    document.getElementById("add_department_close").click();
                    $("#list_dm").load(location.href + " #list_dm");
                }
            });
        }
    });

    $("#departmentModal").on('show.bs.modal', function(event){
        var button = $(event.relatedTarget);
        var title = button.data('title');
        if (title === 'edit'){
            $('#title').html("Edit Department")
            var dmid = button.attr('id');
            $("input[name=dmid]").val(dmid);
            var name = $("#name"+dmid).html();
            $("input[name=name]").val(name);
            var des = $("#des"+dmid).html();
            $("input[name=des]").val(des);
        }
        else{
            $("input[name=dmid]").val("");
            $("input[name=name]").val("");
            $("input[name=des]").val("");
        }
    });
});