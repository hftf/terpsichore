var audioContext = new AudioContext();
var audioInput = null,
    realAudioInput = null,
    inputPoint = null,
    audioRecorder = null;
var rafID = null;
var analyserContext = null;
var canvasWidth, canvasHeight;
var recIndex = 0;
var myId = 0;
var myToken = null;

function saveAudio() {
    audioRecorder.exportWAV( doneEncoding );
}

function doneEncoding( blob ) {
    Recorder.forceDownload( blob, "myRecording" + ((recIndex<10)?"0":"") + recIndex + ".wav" );
    recIndex++;
}

function toggleRecording( e ) {
    if (e.classList.contains("recording")) {
        // stop recording
        audioRecorder.stop();
        e.classList.remove("recording");

    } else {
        // start recording
        if (!audioRecorder)
            return;
        e.classList.add("recording");
        $.ajax({
            'type' : 'POST',
            'url' : '/record',
            'data' : {'flag' : ''},
            'success' : function(data) {
                channel = new goog.appengine.Channel(data.toString());

                socket = channel.open();
                myId = socket.applicationKey_;
                myToken = data.toString();
                console.log(myToken);

                socket.onopen = onOpened;
                socket.onmessage = onMessage;
                socket.onclose = onClose;
                socket.onerror = onError;

                audioRecorder.clear();
                audioRecorder.record();
               },
            'error' : function(jqXHR, textStatus, errorThrown) {
                alert('AJAX FAILED');
            }
        });
    }
}

function gotStream(stream) {
    inputPoint = audioContext.createGain();

    realAudioInput = audioContext.createMediaStreamSource(stream);
    audioInput = realAudioInput;
    audioInput.connect(inputPoint);

    audioRecorder = new Recorder( inputPoint );

    zeroGain = audioContext.createGain();
    zeroGain.gain.value = 0.0;
    inputPoint.connect( zeroGain );
    zeroGain.connect( audioContext.destination );

}

function initAudio() {
        if (!navigator.getUserMedia)
            navigator.getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
        if (!navigator.cancelAnimationFrame)
            navigator.cancelAnimationFrame = navigator.webkitCancelAnimationFrame || navigator.mozCancelAnimationFrame;
        if (!navigator.requestAnimationFrame)
            navigator.requestAnimationFrame = navigator.webkitRequestAnimationFrame || navigator.mozRequestAnimationFrame;

    navigator.getUserMedia({audio:true}, gotStream, function(e) {
            alert('Error getting audio');
            console.log(e);
        });
}

window.addEventListener('load', initAudio );