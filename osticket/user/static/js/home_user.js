 //this function can remove a array element.
 Array.remove = function(array, from, to) {
    var rest = array.slice((to || from) + 1 || array.length);
    array.length = from < 0 ? array.length + from : from;
    return array.push.apply(array, rest);
};

//this variable represents the total number of popups can be displayed according to the viewport width
var total_popups = 0;

//arrays of popups ids
var popups = [];
var popups2 = [];

//this is used to close a popup
function close_popup(id)
{
    for(var iii = 0; iii < popups.length; iii++)
    {
        if(id == popups[iii])
        {
            Array.remove(popups, iii);

            document.getElementById(id).style.display = "none";
            
            calculate_popups();
            return;
        }
    }   
}

//displays the popups. Displays based on the maximum number of popups that can be displayed on the current viewport width
function display_popups()
{
    var right = 160;
    
    var iii = 0;
    for(iii; iii < total_popups; iii++)
    {
        if(popups[iii] != undefined)
        {
            var element = document.getElementById(popups[iii]);
            element.style.right = right + "px";
            right = right + 320;
            element.style.display = "block";
        }
    }
    
    for(var jjj = iii; jjj < popups.length; jjj++)
    {
        var element = document.getElementById(popups[jjj]);
        element.style.display = "none";
    }
}

// Check popup exits
function check_popup(id, list_popup){
    var x = false;
    for (var i = 0; i < list_popup.length; i++)
        if (list_popup[i] == id){
            x = true;
            break;
        }
    return x;
}


//creates markup for a new popup. Adds the id to popups array.
function register_popup(id, name)
{
    if (check_popup(id, popups) == false){
        if (check_popup(id, popups2)){
            popups.unshift(id);
            calculate_popups();
        }else{
            var element = '<div class="live-chat popup-box chat-popup" id="'+ id +'"><header class="clearfix header-chat"><div class="popup-head-right"><a class="chat-close" href="javascript:close_popup(\''+ id +'\');">&#10005;</a></div><div class="popup-head-left"><h4>'+ name +'</h4></div><span class="chat-message-counter">'+popups+'</span></header><div class="frame chat'+name+'"><ul></ul><div><div class="msj-rta macro"><div class="text text-r" style="background:whitesmoke !important"><input id="chat-message-input'+ name +'" class="mytext" placeholder="Type a message"/></div></div><div style="padding:10px;"><span id="chat-message-submit'+ name +'" class="glyphicon glyphicon-share-alt xxx"></span></div></div></div></div>';
            $("#info_user").append(element);
            popups.push(id);
            popups2.push(id);
                    
            calculate_popups();
        }
    }else{
        for(var iii = 0; iii < popups.length; iii++)
        {
            if(id == popups[iii])
            {
                Array.remove(popups, iii);
                popups.unshift(id);
                calculate_popups();
            }
        }
    }
    
}

//calculate the total number of popups suitable and then populate the toatal_popups variable.
function calculate_popups()
{
    var width = window.innerWidth;
    if(width < 380)
    {
        total_popups = 0;
    }
    else
    {
        width = width - 300;
        //320 is width of a single popup box
        total_popups = parseInt(width/320);
    }
    
    display_popups();
    
}

$(document).ready(function(){
});

function makeid() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  
    for (var i = 0; i < 5; i++)
      text += possible.charAt(Math.floor(Math.random() * possible.length));
  
    return text;
  }

//recalculate when window is loaded and also when window is resized.
window.addEventListener("resize", calculate_popups);
window.addEventListener("load", calculate_popups);

