$(document).ready(function () {
    
    $('.text').textillate({
        loop: true,
        sync: true,
        in:{
            effect:"bounceIn",
        },
        out:{
            effect:"bounceOut",
        },
    });
    //siri wave configuration
    var siriWave = new SiriWave({
container: document.getElementById('siri-container'),
width: 850,
height: 200,
style: 'ios9',
speed: 0.2,
amplitude: 1,
autostart: true
});
//siri message animation
$('.siri-message').textillate({
        loop: true,
        sync: true,
        in:{
            effect:"fadeInUp",
            sync:true,
        },
        out:{
            effect:"fadeOutUp",
            sync:true,
        },
    });

    //micbutton click event
    $("#MicBtn").click(function () { 
        eel.playAssistantSound()
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()()
        
    });

    function doc_keyUp(e) {
        if(e.key === 'j' && e.metaKey) {
            eel.playAssistantSound()
            $("#Oval").attr("hidden",true);
            $("#SiriWave").attr("hidden",false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    function PlayAssistant(message) {

        if (message != "") {
            
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("");
            $("#MicBtn").attr("hidden", false);
            $("#SendBtn").attr("hidden", true);
        }
    }

function ShowHideButton(message) {
    if (message.length == 0) {
        $("#MicBtn").attr('hidden', false);
        $("#SendBtn").attr('hidden', true);
    } 
    else {
        $("#MicBtn").attr('hidden', true);
        $("#SendBtn").attr('hidden', false);
    }
}

$("#chatbox").keyup(function () {

    let message = $("#chatbox").val();
    ShowHideButton(message);
});

$("#SendBtn").click(function () {
    let message = $("#chatbox").val();
    PlayAssistant(message);
});


$(" #chatbox").keypress(function (e) {
  let key = e.which;
  if (key == 13) {
      let message = $("#chatbox").val();
      PlayAssistant(message);
  }
});

});