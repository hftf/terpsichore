var audio_context;
var recorder;

$(document).ready(function() {

	try {
		window.AudioContext = window.AudioContext || window.webkitAudioContext || window.;
		navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
		window.URL = window.URL || window.webkitURL;

		audio_context = new AudioContext;

		navigator.getUserMedia({audio:true}, startStream, function(e) {
			console.log('No audio input');
		});
	} catch (e) {
		alert('No web audio support in this browser!');
	}

	$('.record').click(function(){
		recorder && recorder.record();
		$(this).disabled = true;
		$('.stop').disabled = false;
		console.log('recording')

	});
	$('.stop').click(function(){
		recorder && recorder.stop();
		$(this).disabled = true;
		$('.record').disabled = false;
		console.log('stopped')
	});
	$('.download').click(function(){
		recorder && recorder.exportWAV(function(sound){
			var url = URL.createObjectURL(sound);
			console.log(url);
		});
	});
});

function startStream(stream) {
	var input = audio_context.createMediaStreamSource(stream);
	input.connect(audio_context.destination);
	recorder = new Recorder(input);
}