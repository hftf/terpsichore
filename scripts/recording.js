$(document).ready(function(){
	var constraints = {
		audio: true,
		video: false
	};

	var audioStream; 
	var recorder;
	var audio = $('audio')
	var $record = $('#record')
	var $stop = $('#stop')

	$record.click(function(){
		if(!audioStream) {
			navigator.getUserMedia(constraints, function(stream){
				if(window.IsChrome) stream = new window.MediaStream(stream.getAudioTracks());
				audioStream = stream

				audio.src = URL.createObjectURL(audioStream);
				audio.play();

				recorder = window.RecordRTC(stream, {type : 'audio'});
				recorder && recorder.startRecording();

				$record.attr('disabled','true');
				$stop.removeAttr('disabled');
			}, function() {alert('Audio loading failed')});
		} else {
			audio.src = URL.createObjectURL(audioStream);
			audio.play();
			recorder && recorder.startRecording();
		}
		});


	$stop.click(function(){
		$stop.attr('disabled','true');
		$record.removeAttr('disabled');
		audio.src = '';
		recorder && recorder.stopRecording(function(url) {
			console.log(url);
		});
	});
});