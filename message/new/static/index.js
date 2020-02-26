async function get_date(){
  var date=new Date();
  var x=date.getDate()+"-"+date.getMonth()+"-"+date.getFullYear()
  x=x+" "+date.getHours()+":"+date.getMinutes()+":"+date.getSeconds()
  return x
}


async function load_name(){
  return await fetch('/get_name').
    then(async function(response){
       return response.json();
    }).then(async function(text){
      return text["name"];
  })
}

var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on( 'connect',async function() {

    var name=await load_name()
    let user_time= await get_date();
    if(name!=""){
        socket.emit( 'my event', {
            name: name,
           msg: ' connected to the server!!!',
           time: user_time,
           connect: "start"
       },function(){
        return false
       }
       )
    }

    var frm=$('#sendBtn').on('click',async function(e){
        e.preventDefault();
        let user_name = await load_name();
        let user_input = $('#msg' ).val();
        let user_time= await get_date();
        $('#msg' ).val('');
        socket.emit('my event',{
          name: user_name,
          msg: user_input,
          time: user_time
        })
    })
} )
async function add_message( data ) {
  var name=await load_name()
  console.log(data)
  if(typeof data.connect!=='undefined')
  {
    console.log(data.connect)
    var txt="<div class=\"container "+data.connect+" text-center\"><b>"+data.name+"</b><span>"+data.msg+"</span><br><small class=\"text-muted\">"+data.time+"</small></div>"
  }
  else if(name==data.name)
  {
    var txt="<div class=\"container text-right\"><span>"+data.msg+"</span><br><small class=\"text-muted\">"+data.time+"</small></div>"
  }
  else
  {
    var txt="<div class=\"container darker text-left\"><b>"+data.name+" : </b><span>"+data.msg+"</span><br><small class=\"text-muted\">"+data.time+"</small></div>"
  }
  document.getElementById("print").innerHTML+=txt;
  $('#print').animate({ scrollTop: $("#print").height() }, 1000);
}


socket.on('left',async function(data){
  data["time"]=await get_date()
  data["connect"]="leave"
  add_message(data)
})

socket.on( 'message pass',async function(data){

  await add_message(data)
})


$('.crss').on('click',function(){
  $('#log1').hide();
  $('#log2').hide();
})


