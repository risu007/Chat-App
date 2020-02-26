$(function() {
          $('#sendBtn').bind('click', function() {
                var msg=document.getElementById("msg")
                var value=msg.value
                msg.value=""
                console.log(value)
                $.getJSON('/send_messages',
                    {val:value},
                    function(data) {

                });

                return false;
        });
});


window.addEventListener("load",function(){
    var update_loop=setInterval(update,100);
    update()
});

function update(){
    fetch('/get_messages')
                    .then(function (response) {
                        return response.json();
                    }).then(function (text) {
                        var messages ="";
                        for(value of text["messages"])
                        {
                            messages=messages+value+"<br>";
                        }
                        document.getElementById("test").innerHTML=messages
        });
}






function validate(name){
    if(name.length>=2)
        return true;
    else
        return false;
}
