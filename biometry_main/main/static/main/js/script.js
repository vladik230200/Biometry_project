var counter = 0;
function plus_click(element) {
	counter++;
	element.innerHTML = "Вы нажали на кнопку: " + counter + " раз(-а)";
}

var audioChunks = [];
var sample_mass_registration = [];
function sample(){
	navigator.mediaDevices.getUserMedia({ audio: true})
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            document.querySelector('#start').addEventListener('click', function(){
                mediaRecorder.start();
            });
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
                audio.autoplay = false;
                document.querySelector('#audio').appendChild(audio);
                sample_mass_registration.push(audioBlob);
                audioChunks = [];
            });

            document.querySelector('#stop').addEventListener('click', function(){
                mediaRecorder.stop();
            });
    });
};

function do_registration(){
        var csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        	const formData = new FormData();
        	formData.append('login', document.getElementById('user').value);
        	formData.append('password', document.getElementById('pass').value);
        	formData.append('csrfmiddlewaretoken', csrf_token);
        	for (var i = 0; i < sample_mass_registration.length; i++) {
                var audio = 'audio' + (i+1);
                formData.append(audio, sample_mass_registration[i]);
            }

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
        };

var sample_mass_login = [];
function sample_login(){
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
        var audioBlob = new Blob(audioChunks, {
            type: 'audio/wav'
        });
        const audioUrl = URL.createObjectURL(audioBlob);
        var audio = document.createElement('audio');
        audio.src = audioUrl;
        audio.controls = true;
        audio.autoplay = true;
        document.querySelector('#audio').appendChild(audio);
        sample_mass_login.push(audioBlob);
		});
        audioChunks = [];
    document.querySelector('#stop').addEventListener('click', function(){
        mediaRecorder.stop();
    });
    });
};
function do_login(){
var csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        	const formData = new FormData();
        	formData.append('login', document.getElementById('user').value);
        	formData.append('password', document.getElementById('pass').value);
        	formData.append('csrfmiddlewaretoken', csrf_token);
        	for (var i = 0; i < sample_mass_login.length; i++) {
                var audio = 'audio' + (i+1);
                formData.append(audio, sample_mass_login[i]);
             }

        	$.ajax({
        		url: 'login/verification/',
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
};

function openPopup() {
    var popup = document.getElementById("popup");
    popup.style.display = "block";
}

function closePopup() {
    var popup = document.getElementById("popup");
    popup.style.display = "none";
}