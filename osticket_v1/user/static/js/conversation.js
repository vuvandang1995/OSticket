$(document).ready(function(){
    $('#btn').click(function(){
		    var token = $("input[name=csrfmiddlewaretoken]").val();
			var content = $('#content').val();
			if($('#content').val() == '')return false;
			else{
                $.ajax({
                    type:'POST',
                    url:location.href,
                    data: {'content':content,'csrfmiddlewaretoken':token},
                    success: function(){
                         $("#list_comment").load(location.href + " #list_comment");
                    }
                });
                $('#content').val("");
			}
		});
	function reFresh(){
	  setInterval(function(){
	    $("#list_comment").load(location.href + " #list_comment");
	  },3000);
	}
	reFresh();
});