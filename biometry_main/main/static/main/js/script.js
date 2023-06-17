var counter = 0;
function plus_click(element) {
	counter++;
	element.innerHTML = "Вы нажали на кнопку: " + counter + " раз(-а)";
}

function sample(){
	navigator.mediaDevices.getUserMedia({ audio: true})
        .then(stream => {
        const mediaRecorder = new MediaRecorder(stream);

        document.querySelector('#start').addEventListener('click', function(){
        mediaRecorder.start();
        });
    var audioChunks = [];
    mediaRecorder.addEventListener("dataavailable",function(event) {
        audioChunks.push(event.data);
    });

    mediaRecorder.addEventListener("stop", async function() {
        const audioBlob = new Blob(audioChunks, {
            type: 'audio/wav'
        });
        const audioUrl = URL.createObjectURL(audioBlob);
        var audio = document.createElement('audio');
        audio.src = audioUrl;
        audio.controls = true;
        audio.autoplay = true;
        document.querySelector('#audio').appendChild(audio);

        var csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

        document.querySelector('#do_login').addEventListener('click', function(event){
        	const formData = new FormData();
        	formData.append('login', document.getElementById('user').value);
        	formData.append('password', document.getElementById('pass').value);
        	formData.append('csrfmiddlewaretoken', csrf_token);
        	formData.append('audio', audioBlob);

        	$.ajax({
        		url: 'registration/verification',
        		type: 'POST',
        		data: formData,
        		processData: false,
            	contentType: false,
        		dataType: 'json',
        		success: function(response) {
                    var redirectUrl = response.redirect_url;
                    window.location.href = redirectUrl;
        		},
        		error: function(xhr, status, error) {
            // Обработка ошибки
        		}
    		});
        });
		});
        audioChunks = [];
    document.querySelector('#stop').addEventListener('click', function(){
        mediaRecorder.stop();
    });
    });
};        